# Conversation Backup — ENPM818Z Working Notes

**Last updated:** 2026-08-09
**Branch:** `main`
**Purpose:** Snapshot of completed work + open items, so the conversation
can be resumed on another PC without losing context.

The original handoff goal (apply the lecture reorder sketched on the
previous PC) has been **completed in full**. This document now captures
the current state — what was shipped, what's open, and where to look.

---

## Session 2026-08-09 (full lecture review + remediation)

Reviewed all 14 lectures line by line and fixed everything found. Sphinx
build clean (0 warnings) after every change.

**Two course-policy decisions were made and applied everywhere:**

- **Meeting day: Thursdays**, Sep 3 → Dec 10, 2026, with a Week 15
  (Dec 17) final-report window. The `.md`/`.pdf` syllabus previously said
  Mondays and has been rewritten to match the website.
- **Grading: 80% final project (GP1–GP4 + report) / 20% quizzes.**
  **GP5 has been removed from the course** — `gp5.rst` deleted, dropped
  from the toctree, the L12 unlock box replaced with a Summary, and all
  references purged from the syllabus.

**What was fixed:**

- **Stale cross-references** from the reorder, in L1, L2, L7, L8, L9,
  L12, L13, L14 and `l9_references.rst`. The worst were L8's ASCII stack
  diagram and L14's course-summary table, which described a course
  structure that never existed.
- **Math/factual errors**: L5 LSS Lift equation and the Shoot
  definition; L5 PQ→RQ mislabel and ASE; L9 CTRA (velocity term was
  missing entirely); L7 essential-matrix form, Kabsch reflection guard,
  loop-closure overclaim, LOAM units, differential-drive odometry on an
  Ackermann vehicle; L11 continuity and Ziegler-Nichols PD row;
  L14 ASIL PMHF targets and an inverted C0/C3 controllability scale.
- **Code bugs**: the UE→optical axis permutation (L2, L5, L6); CARLA
  0.9.16 semantic tag IDs and depth decoding (L5); L6's "Kalman filter"
  that was actually an exponential moving average; L3 synchronous mode;
  L8 waypoint-graph keying (produced a graph with zero edges) and an
  infinite loop in the route follower; L4 BGR/RGB and the RT-DETR API.
- **Content gaps filled**: IoU/NMS/mAP and 3-D LiDAR detection (L4);
  Hybrid A\* and the Frenet frame (L10); transformer MOT and 3-D
  tracking (L6); a full CARLA hands-on for L7; the open-loop planning
  critique (L12).
- **Structure normalized**: L9–L12's collapsed dropdowns converted to
  open sections (54 total); Summary cards added to the 5 lectures that
  lacked them; L8's quiz rewritten from 10 ad-hoc questions to the
  standard 18 (10 MC / 5 TF / 3 essay).
- **New**: `docs/source/preread/` holding the L1 dev-environment setup
  and the L14 cybersecurity material, both trimmed out of lecture time
  (the long-deferred "L1 trim" and "L14 trim" items).

**Still open:** see the reduced list at the bottom.

---

## Session 2026-08-02 (reorder v2 polish + syllabus)

Uncommitted working-tree changes at time of writing.

- **Quiz migration + rebalance (all quizzes now 18 = 10 MC / 5 TF / 3 essay).**
  Fixed the topical misplacements the reorder left behind, swap-in-place so no
  renumbering was needed:
  - L6 → L5: moved the 7 segmentation questions out of the tracking quiz into
    L5; dropped 7 redundant/temporal BEV-occupancy questions from L5.
  - L3 → L6: moved the BEVFusion question to L6; backfilled L3 with a new
    CV/CTRA + EKF/UKF motion-model question.
  - L9 → L12: moved the 5 imitation-learning questions (behavior cloning,
    DAgger x2, distribution-shift essay, FSM-vs-learned essay) into L12; dropped
    5 redundant E2E questions from L12; backfilled L9 with new prediction
    questions.
  - Authored ~6 new L6 tracking/temporal/fusion questions plus the L3/L9
    backfills. Removed the now-satisfied "follow-up migration" notes.
  - Fixed an answer-key bug in L3 Q9 (inverse-variance weighting: key said B,
    correct answer is D = 10.08 m).
- **L5/L6 exercises + references.** Moved Segmentation Metrics exercise L6 → L5
  (now L5 Exercise 6); added a Semantic Segmentation references section to L5;
  cleaned the stale note and renumbered L6 exercises.
- **Sphinx build:** clean, 0 warnings, after all changes.
- **Syllabus schedule corrected** against the real UMD Fall 2026 calendar: the
  schedule wrongly had a class on 10/12 (Fall Break) and wrongly marked 11/30 as
  a holiday (Thanksgiving recess is Nov 25 to 29, so 11/30 is a class day). Both
  fixed; lectures L6 to L12 shifted one Monday later; all 14 lectures fit 13
  Mondays + the Dec 11 session. Fixed an en-dash in Course Dates and converted
  the collaboration matrix from unrenderable checkmarks to Yes/No. **PDF
  regenerated** (18 pages, clean).
- **Still open:** L1/L14 trims (see below); housekeeping of untracked files; the
  zeidk vs rubixcubic repo decision; a broader em-dash cleanup (the syllabus and
  schedule titles still use em-dashes, against the no-em-dash preference).

---

## Completed work this session

### 1. Lecture reorder (9 commits, `1be9acf` → `de7e83f`)

Restructured the 14 lectures to fix the two main pedagogical dependency
inversions:

- **KF / EKF math** (was in L6) now precedes **tracking** (L6) and
  **SLAM** (L7).
- **Prediction** (was L11) now precedes **motion planning** (L10).

Final order:

| #   | Topic                                                |
| --- | ---------------------------------------------------- |
| L1  | Course Intro, AV Landscape, Safety, CARLA            |
| L2  | Sensor Technologies & Calibration                    |
| L3  | **Probabilistic State Estimation & Fusion**          |
| L4  | Perception I: Detection (YOLO → DETR)                |
| L5  | Perception II: BEV, Occupancy & Segmentation         |
| L6  | Perception III: Tracking, Temporal & Deep Fusion     |
| L7  | Localization & SLAM                                  |
| L8  | Navigation & Route Planning                          |
| L9  | **Prediction & Behavior Modeling**                   |
| L10 | Motion Planning                                      |
| L11 | Trajectory Generation & Control                      |
| L12 | End-to-End Driving, VLA & Imitation Learning         |
| L13 | World Models & Simulation                            |
| L14 | System Integration, Safety & Industry Outlook        |

Touched: every `lectureN/lN_*.rst`, `lectures/index.rst`,
`syllabus/index.rst`, `assignments/{index,gp1..5}.rst`, plus
`docs/source/conf.py` (temporary `exclude_patterns` entry, reverted at
swap).

Strategy used: built the new structure under
`docs/source/lectures/_new/` first, then swapped in stage 8. Each
intermediate commit kept `main` buildable. See `reorder-plan.md` in this
folder for the full per-stage execution plan.

### 2. Glossary search + tagging (2 commits, `d58ccc3`, `8b3e282`)

- **Ported** the live-search + L1–L14 lecture filter from
  `enpm605-spring-2026-docs` into `docs/source/glossary/glossary.rst`.
  Self-contained HTML/JS block inside `.. only:: html`.
- **Tagged** every existing entry with `:doc:` references to the
  lecture(s) it appears in. 159 lecture-tag refs total, distributed
  L1: 15, L2: 17, L3: 12, L4: 25, L5: 18, L6: 17, L7: 18, L8: 6, L9: 6,
  L10: 10, L11: 9, L12: 10, L13: 9, L14: 17.
- **Added 20 new terms** drawn from the reorganised lectures: ASPP,
  Bayer Pattern, Collision Detection, Cross-Track Error, Data
  Association, Dijkstra, Dilated Convolution, DriveVLM, Focal Loss,
  Foundation Model, Lanelet2, MOTP, Multi-Modal Prediction,
  Nonholonomic Constraint, nuScenes, OpenDRIVE, Pinhole Camera Model,
  Rolling Shutter, Scan Matching, Tracking-by-Detection, Vista.

Final glossary: 157 terms (was 137), 159 lecture tags.

### 3. Sphinx build cleanup

Fixed the one lingering build warning — the duplicate
`carla.readthedocs.io` named-target in
`docs/source/lectures/lecture8/l8_references.rst`. Switched both
references from named (`` `text <url>`_ ``) to anonymous
(`` `text <url>`__ ``). Bundled into the syllabus commit (`e0ecd73`).

`sphinx-build -b html docs/source docs/_build/html` now produces a
clean build with **zero warnings**.

### 4. Canvas course homepage rewrite

User pasted the Canvas DesignPlus HTML; I returned an updated version
with:

- Code-repo URL typo fix: `enpm818z-spring-2026-code` →
  `enpm818z-fall-2026-code`.
- Rewritten 3-paragraph Course Overview that explicitly mentions the
  new lecture progression (state-estimation foundation, modern stack,
  end-to-end, world models, safety standards).
- 7 reorganised Course Outcomes that map cleanly onto the new lecture
  order.

Not committed (lives in Canvas, not the repo).

### 5. Syllabus markdown (commit `e0ecd73`)

Created `SYLLABUS-ENPM818Z-Fall2026.md` at the repo root, modeled on
the MAGE template used by `ENPM818T 2601 Accessible Syllabus.pdf`.

Course-specific decisions baked in:

- Grade breakdown: GPs 70% / Quizzes 25% / Participation 5%, with GP5
  as up to +10% bonus. Different from ENPM818T's 55/40/5 — easy to
  swap if needed.
- Fall 2026 schedule: Aug 31 → Dec 11, 2026 Mondays, skipping Labor
  Day (Sep 7) and Thanksgiving-week Monday (Nov 30). 14 lectures in
  14 actual meetings. **Dates need confirming against the real UMD
  Fall 2026 calendar.**
- Single instructor (no co-instructor listed).

Convertible to .docx / .pdf via pandoc:
```
pandoc SYLLABUS-ENPM818Z-Fall2026.md \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Serif" -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -o SYLLABUS-ENPM818Z-Fall2026.pdf
```
(`SYLLABUS-ENPM818Z-Fall2026.pdf` is generated but currently untracked.)

### 6. Multiple-GitHub-account setup (local only, not in repo)

Configured the workstation for two GitHub identities — local files
only, nothing committed:

- `~/.ssh/config`: `github.com` → `zeidk` (NIST work, default);
  `github-umd` host alias → `rubixcubic` (UMD).
- Renamed the existing key to `~/.ssh/id_ed25519_zeidk`; generated a
  new `~/.ssh/id_ed25519_rubixcubic`.
- `~/.gitconfig`: default identity `Zeid Kootbally /
  zeid.kootbally@nist.gov`, with `includeIf` pointing repos under
  `~/github/docs/` at `~/.gitconfig-umd` (which sets
  `zeidk@umd.edu`).
- Wrote `MULTIPLE-GITHUB-ACCOUNTS.md` at the repo root as a reference
  guide. Currently untracked.

Verified: `git config user.email` returns `zeidk@umd.edu` inside this
repo and `zeid.kootbally@nist.gov` outside `~/github/docs/`.

---

## Current repo state

```
Branch:          main
Latest commit:   3f5a960  updates
Working tree:    extensive uncommitted changes from the 2026-08-09
                 lecture review (all 14 lectures, syllabus, assignments,
                 new preread/ directory, gp5.rst deleted)
Untracked:       - MULTIPLE-GITHUB-ACCOUNTS.md      (dev-setup notes)
                 - SYLLABUS-ENPM818Z-Fall2026.pdf   (pandoc output,
                   regenerated 2026-08-09 for the Thursday schedule)
                 - docs/source/preread/             (new)
Sphinx build:    clean (0 warnings)
```

Commit chain since resume (in chronological order, oldest first):

```
1be9acf  reorder: stage 1 - scaffold _new/ + copy unchanged lectures
7c2c96d  reorder: stage 2 - renumber L3->L4, L9->L10, L10->L11
88800cd  reorder: stage 3 - extract new L3 (State Estimation) from old L6
127185a  reorder: stage 4 - merge new L5 (BEV + Occupancy + Segmentation)
e6eb2df  reorder: stage 5 - merge new L6 (Tracking, Temporal & Deep Fusion)
a12b1dc  reorder: stage 6 - extract new L9 (Prediction & Behavior Modeling)
15c5d42  reorder: stage 7 - merge new L12 (E2E + VLA + Imitation Learning)
f5f9ff2  reorder: stage 8+9 - swap _new/ into place, update lectures/index.rst
de7e83f  reorder: stage 10 - update syllabus + assignments for new order
d58ccc3  glossary: port live search + lecture filter from enpm605
8b3e282  glossary: tag existing entries + add 20 new terms from lectures
e0ecd73  added syllabus MD
```

---

## Open items / future work

### Reorder polish

**All items in this section are now done** — quiz migration, L5
segmentation exercise and references, L6 Exercise 1, L6 temporal
reasoning (transformer MOT added), the L1 dev-environment trim, and the
L14 cybersecurity trim. The last two moved to `docs/source/preread/`.

### Needs your verification

These were flagged during the 2026-08-09 review as claims I could not
confirm. They are written conservatively in the lectures now, but should
be checked against primary sources before teaching:

- **L12 UniAD metrics.** The planning L2 figures were badly wrong
  (0.25 m at 3 s, when the paper reports ~1.65 m). Replaced with
  approximate values and a warning; verify against the paper.
- **L13 GAIA generation.** The lecture previously described a
  "GAIA-3, 15B parameters, December 2025" that I could not verify.
  Rewritten around GAIA-1 and GAIA-2 only. If GAIA-3 exists, add it.
- **L1 Tesla robotaxi supervision status** in Austin — changes often.
- **L5 CARLA semantic tag IDs.** Corrected to the CityScapes-aligned
  scheme (Road=1, Car=14), but confirm against the CARLA docs for the
  exact version students install.
- **L10 diffusion planner** step counts and benchmarks.

### GitHub workflow

- **Repo location decision.** This repo is currently
  `git@github.com:zeidk/enpm818z-fall-2026-docs.git`. With the new
  multi-account setup, UMD work is meant to live on `rubixcubic`.
  Either transfer the repo on GitHub (Settings → Transfer ownership)
  and `git remote set-url origin
  git@github-umd:rubixcubic/enpm818z-fall-2026-docs.git`, or
  consciously decide to leave UMD course material on the `zeidk`
  account.
- **GitHub Pages deployment.** Optional: replace Read the Docs with a
  GitHub Actions workflow that builds Sphinx and deploys to
  `<account>.github.io/enpm818z-fall-2026-docs/`. Sample workflow
  walked through in chat but not yet committed.

### Syllabus

- **Verify Fall 2026 dates** against the actual UMD academic calendar.
- **Pandoc reference-doc.** If a UMD/MAGE Word template is available,
  `pandoc --reference-doc=umd-reference.docx` will make the converted
  .docx look closer to the official syllabus style.

---

## Files of interest

| File                                        | Purpose                                         |
| ------------------------------------------- | ----------------------------------------------- |
| `conversation-backup/conversation-summary.md` | This file. Current state + open items.        |
| `conversation-backup/reorder-plan.md`         | Historical: detailed plan executed in stages 1–11. |
| `conversation-backup/session-56b8bf30.jsonl`  | Raw transcript from the *original* PC, before resume. |
| `conversation-backup/README.md`               | Resume-on-another-PC instructions.            |
| `SYLLABUS-ENPM818Z-Fall2026.md`               | Repo root. Markdown syllabus, convert via pandoc. |
| `MULTIPLE-GITHUB-ACCOUNTS.md`                 | Repo root. Dev-setup guide. Probably belongs outside the repo. |
| `docs/source/lectures/`                       | All 14 lecture folders, post-reorder.         |
| `docs/source/glossary/glossary.rst`           | 157 terms with live search + lecture filter.  |
| `docs/source/conf.py`                         | Sphinx config. `exclude_patterns = []`.       |

---

## Cleanup

Once the resume model isn't needed any longer, remove this folder:

```
git rm -rf conversation-backup
git commit -m "remove conversation backup"
```

Same for `MULTIPLE-GITHUB-ACCOUNTS.md` if you'd prefer it not live in
the course repo:

```
git rm MULTIPLE-GITHUB-ACCOUNTS.md   # only if it was ever committed
# or
mv MULTIPLE-GITHUB-ACCOUNTS.md ~/notes/
```
