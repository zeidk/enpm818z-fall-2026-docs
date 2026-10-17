#!/usr/bin/env python3
"""Peer evaluation scores from an mbox export.

Parses the email template from the syllabus (one email per student, plain
text body) and produces the score table: received mean R, team mean T,
factor F = R / T clamped to [0.6, 1.1], peer score 40 * F, and the
individual grade 0.6 * team grade + peer score.

    python3 tools/peer_scores.py gp1.mbox --project GP1 \
        --team-grades grades.csv --out results.md

grades.csv has two columns, team and grade (0 to 100), one row per team:

    team,grade
    1,88
    2,82

Flags: incomplete emails (not scored until a complete one arrives), members who
never sent one (peer score forfeited), ratings that diverge by two or more
points, and self-ratings two or more points from the received mean.
Names are matched case-insensitively after collapsing whitespace.
"""

import argparse
import csv
import mailbox
import re
import sys
from collections import defaultdict

CRITERIA = ('Technical contribution', 'Reliability', 'Communication',
            'Understanding', 'Collaboration')
PEER_POINTS = 40.0
TEAM_SHARE = 0.6
CLAMP = (0.6, 1.1)
DIVERGENCE = 2.0

SUBJECT_RE = re.compile(
    r'\[ENPM818Z\]\s*(?P<project>GP\d)\s*peer evaluation\s*-\s*Team\s*(?P<team>\d+)', re.I)
FROM_RE = re.compile(r'^From\s*:\s*(?P<name>.+?)\s*$', re.M | re.I)
BLOCK_RE = re.compile(r'^---\s*(?P<name>.+?)\s*(?P<self>\(self\))?\s*---\s*$', re.M)
RATING_RE = {c: re.compile(rf'^{re.escape(c)}\s*:\s*(?P<v>[1-5](?:\.\d+)?)\s*$', re.M | re.I)
             for c in CRITERIA}
SENTENCE_RE = re.compile(r'^What (?:they|I) contributed\s*:\s*(?P<s>.+?)\s*$', re.M | re.I | re.S)


def key(name):
    return ' '.join(name.split()).lower()


def body_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode(
                    part.get_content_charset() or 'utf-8', 'replace')
        return ''
    return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', 'replace')


def parse_email(msg, project):
    """One email -> (team, rater, {rated: {criterion: value}}, self_ratings, problems)."""
    m = SUBJECT_RE.search(str(msg.get('Subject', '')).replace('\n', ' '))
    if not m or m['project'].upper() != project.upper():
        return None
    team = int(m['team'])
    text = body_text(msg)
    problems = []
    f = FROM_RE.search(text)
    rater = f['name'].strip() if f else str(msg.get('From', 'unknown sender'))
    if not f:
        problems.append('missing "From:" line in the body')
    ratings, self_ratings = {}, None

    blocks = list(BLOCK_RE.finditer(text))
    for i, b in enumerate(blocks):
        chunk = text[b.end(): blocks[i + 1].start() if i + 1 < len(blocks) else len(text)]
        chunk = chunk.split('Anything the instructor should know')[0]
        values = {}
        for c, rx in RATING_RE.items():
            r = rx.search(chunk)
            if r:
                values[c] = float(r['v'])
            else:
                problems.append(f'{b["name"]}: missing "{c}"')
        s = SENTENCE_RE.search(chunk)
        if not s or len(s['s'].split()) < 4:
            problems.append(f'{b["name"]}: missing contribution sentence')
        if b['self'] or key(b['name']) == key(rater):
            self_ratings = values
        else:
            ratings[b['name'].strip()] = values
    if not blocks:
        problems.append('no rating blocks found')
    if self_ratings is None:
        problems.append('missing self block')
    return team, rater, ratings, self_ratings, problems


def mean(vals):
    return sum(vals) / len(vals) if vals else float('nan')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('mbox')
    ap.add_argument('--project', required=True, help='e.g. GP1')
    ap.add_argument('--team-grades', help='CSV with columns team,grade')
    ap.add_argument('--weight', type=float, default=1.0,
                    help='scale factor for the final column, e.g. 0.15 for GP1')
    ap.add_argument('--out', help='write the Markdown report here too')
    args = ap.parse_args(argv)

    team_grade = {}
    if args.team_grades:
        with open(args.team_grades) as f:
            for row in csv.DictReader(f):
                team_grade[int(row['team'])] = float(row['grade'])

    # team -> rater -> rated -> mean over criteria
    given = defaultdict(dict)
    selfs = defaultdict(dict)
    raw = defaultdict(lambda: defaultdict(dict))   # team -> rated -> rater -> mean
    display = {}
    returned, seen = [], defaultdict(list)

    for msg in mailbox.mbox(args.mbox):
        parsed = parse_email(msg, args.project)
        if parsed is None:
            continue
        team, rater, ratings, self_ratings, problems = parsed
        display[key(rater)] = rater
        if problems:
            returned.append((team, rater, problems))
            continue
        if key(rater) in seen[team]:
            continue                         # keep the first complete email
        seen[team].append(key(rater))
        for rated, values in ratings.items():
            display.setdefault(key(rated), rated)
            given[team][(key(rater), key(rated))] = mean(values.values())
            raw[team][key(rated)][key(rater)] = mean(values.values())
        selfs[team][key(rater)] = mean(self_ratings.values())

    lines = [f'# {args.project} peer evaluation scores', '']
    for team in sorted(raw):
        members = sorted(set(raw[team]) | set(seen[team]))
        R = {m: mean(raw[team][m].values()) for m in members if raw[team][m]}
        T = mean(R.values())
        lines += [f'## Team {team}', '',
                  f'Team mean T = {T:.2f}'
                  + (f', team grade = {team_grade[team]:.1f}' if team in team_grade else ''),
                  '',
                  '| Student | R | F | Peer (40) | Team (60%) | Individual | Scaled | Flags |',
                  '|---|---|---|---|---|---|---|---|']
        for m in members:
            flags = []
            if m not in seen[team]:
                flags.append('NO SUBMISSION: peer score forfeited')
            r = R.get(m, float('nan'))
            # Round F to two decimals first, as the syllabus example does.
            F = round(min(max(r / T, CLAMP[0]), CLAMP[1]), 2) if r == r else float('nan')
            peer = min(PEER_POINTS * F, PEER_POINTS) if m in seen[team] and F == F else 0.0
            recv = raw[team][m]
            if len(recv) >= 2 and max(recv.values()) - min(recv.values()) >= DIVERGENCE:
                flags.append(f'divergent ratings ({", ".join(f"{display[k]} {v:.1f}" for k, v in recv.items())})')
            if m in selfs[team] and r == r and abs(selfs[team][m] - r) >= DIVERGENCE:
                flags.append(f'self {selfs[team][m]:.1f} vs received {r:.1f}')
            if team in team_grade:
                team_part = TEAM_SHARE * team_grade[team]
                indiv = team_part + peer
                lines.append(f'| {display[m]} | {r:.2f} | {F:.2f} | {peer:.1f} | {team_part:.1f} '
                             f'| **{indiv:.1f}** | {indiv * args.weight:.1f} | {"; ".join(flags)} |')
            else:
                lines.append(f'| {display[m]} | {r:.2f} | {F:.2f} | {peer:.1f} | - | - | - | {"; ".join(flags)} |')
        lines.append('')

    if returned:
        lines += ['## Incomplete emails (not scored)', '']
        for team, rater, problems in returned:
            lines.append(f'- Team {team}, {rater}: ' + '; '.join(problems))
        lines.append('')

    report = '\n'.join(lines)
    print(report)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(report)
    return 0


if __name__ == '__main__':
    sys.exit(main())
