# Lecture Reorder — Execution Plan

**Date:** 2026-05-25
**Branch target:** new branch `reorder/v2` (off `main`)
**Goal:** Apply the full reorder (Phase 1 + 2 content surgery) sketched in
`conversation-summary.md`. Fix dependency inversions: probabilistic state
estimation before tracking/SLAM, prediction before motion planning.

---

## Mapping: source → destination

Per-lecture mapping showing exactly which content goes where.

| New | Title                                                | Source                                                                                                                                                                                                                                                |
| --- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L1  | Course Intro, AV Landscape, Safety Overview, CARLA  | current L1, **trimmed** (dev environment → pre-read)                                                                                                                                                                                                  |
| L2  | Sensors & Calibration                                | current L2 unchanged                                                                                                                                                                                                                                  |
| L3  | **Probabilistic State Estimation & Fusion**          | current L6 lines 1–563 (Why Fusion, Sensor Relationships, Fusion Architectures, KF, EKF, UKF, PF, Filter Comparison, Data Association, Weighted Averaging) + all 4 KF CARLA tasks                                                                      |
| L4  | Perception I — Detection (YOLO → DETR)               | current L3 unchanged (pure renumber from L3 → L4)                                                                                                                                                                                                     |
| L5  | Perception II — BEV, Occupancy, Segmentation         | current L4 (all BEV/Occupancy content + LSS CARLA tasks) **+ merge** current L5 lines 1–198 (Segmentation, DeepLabv3+, Driveable Surface, Instance/Panoptic) + L5 CARLA Tasks 1–2 (Semantic Seg, Seg Metrics)                                          |
| L6  | Perception III — Tracking, Temporal, Deep Fusion     | current L5 lines 199–end (MOT, SORT, DeepSORT, ByteTrack, Tracking Metrics, Temporal Reasoning, Tracking-by-Detection, Integration) + L5 CARLA Tasks 3–4 (SORT tracker) + current L6 lines 564–605 (Cross-Attention Fusion, BEVFusion)                  |
| L7  | Localization & SLAM                                  | current L7 unchanged (EKF refs now point to new L3)                                                                                                                                                                                                   |
| L8  | HD Maps & Route Planning                             | current L8 unchanged                                                                                                                                                                                                                                  |
| L9  | **Prediction & Behavior Modeling**                   | current L11 lines 1–474 (Why Prediction, Trajectory Prediction Approaches — Physics/Maneuver/Interaction-Aware, Transformer-Based, Multi-Modal, Behavior Planning, State Machine, Rule-Based vs Learned) + Practical Decision-Making + CARLA Exercise |
| L10 | Motion Planning                                      | current L9 unchanged (pure renumber from L9 → L10). Now consumes new L9 predictions.                                                                                                                                                                  |
| L11 | Trajectory Generation & Control                      | current L10 unchanged (pure renumber from L10 → L11)                                                                                                                                                                                                  |
| L12 | End-to-End Driving, VLA & Imitation Learning         | current L12 + **merge in** current L11 lines 475–590 (Imitation Learning, DAgger)                                                                                                                                                                     |
| L13 | World Models & Simulation                            | current L13 unchanged                                                                                                                                                                                                                                 |
| L14 | System Integration, Safety, Industry Outlook         | current L14 (trim if still overloaded; cybersecurity → pre-read candidate)                                                                                                                                                                            |

### Quiz/exercise splits (the painful part)

The lectures that split (current L5, L6, L11) each have quizzes (~18 Q
each) organized by question-type (MC / T-F / Essay), not by topic. Each
question must be classified by topic to assign it to the right new
lecture's quiz:

- **L5 quiz** → split between new L5 (seg questions) and new L6 (tracking/temporal questions)
- **L6 quiz** → split between new L3 (KF/EKF/UKF/PF questions) and new L6 (deep fusion questions, if any)
- **L11 quiz** → split between new L9 (prediction/behavior questions) and new L12 (imitation learning questions)

Exercises in those three lectures must be similarly classified by topic.
L5 exercises (5 dropdowns) already mix seg + KF — Exercise 2 is "Kalman
Filter Tracking," which after reorder is no longer awkward since KF is
prereq from new L3.

### Files affected outside `lectures/`

- `docs/source/syllabus/index.rst` — table lists L1–L14 with titles, needs full rewrite
- `docs/source/assignments/index.rst` — lecture ranges per GP need updating:
  - GP1: L1–L2 → still L1–L2 (Intro + Sensors)
  - GP2: L3–L5 → now L3–L5 (State Estimation + Detection + BEV/Seg) — content shifts
  - GP3: L6–L8 → still L6–L8 (Tracking/DeepFusion + Loc/SLAM + Maps)
  - GP4: L9–L11 → now L9–L11 (Prediction + Motion Planning + Trajectory/Control)
- `docs/source/assignments/gp{1..5}.rst` — each lists specific lecture numbers as prereqs; need per-file updates
- `docs/source/changelog/changelog.rst` — historical; **leave alone**

---

## Execution strategy

### Strategy: temp-folder swap (avoids rename collisions)

Renaming `lecture11/` → `lecture9/` would overwrite the existing
`lecture9/`. To avoid collisions, build the new structure under a
parallel folder name, then swap at the end.

**Step 1 — Create branch and stage area**
- `git checkout -b reorder/v2`
- Create `docs/source/lectures/_new/` as the staging area for new lecture folders

**Step 2 — Build each new lecture folder in `_new/`**
For each new lecture N:
- Create `_new/lectureN/l N_lecture.rst`, `l N_index.rst`, `l N_exercises.rst`, `l N_quiz.rst`, `l N_references.rst`
- Populate from source(s) per mapping table above
- For lectures with internal numeric refs (e.g. `Lecture 5` mentions in body text), update them to the new numbering

**Step 3 — Swap**
- `git rm -r` old `lecture1/`–`lecture14/` folders
- `git mv _new/lectureN/ lectureN/` for each N
- Remove `_new/` directory

**Step 4 — Update index/syllabus/assignments**
- Rewrite `docs/source/lectures/index.rst` schedule table + toctree
- Rewrite `docs/source/syllabus/index.rst` lecture list
- Rewrite `docs/source/assignments/index.rst` ranges
- Update each `gp{1..5}.rst` prereq list

**Step 5 — Build verification**
- Run Sphinx build (likely `make html` in `docs/`)
- Fix any broken refs/headings

### Per-lecture work breakdown (rough size)

Small (renumber + internal-ref-update only):
- L2, L4 (from L3), L7, L8, L10 (from L9), L11 (from L10), L13

Medium (single-source content + numeric ref updates):
- L1 (trim dev env), L14 (light trim)

Large (content extraction/merge + quiz split):
- L3 (from L6 — extract classical fusion + filters)
- L5 (merge L4 + L5 seg half)
- L6 (merge L5 tracking half + L6 deep fusion half) — note: this lecture will be **light** at ~320 lines; consider growing it
- L9 (from L11 prediction half)
- L12 (from L12 + L11 IL half)

### Risks / open questions

1. **New L6 will be short** (~320 lines lecture content + 2 CARLA tasks). Options: (a) leave thin, (b) move some Temporal Reasoning depth here, (c) add a transformer-based MOT section (e.g. MOTR). Recommend (a) for v1, address in a follow-up.
2. **Quiz question topic classification** is ~50 manual decisions across 3 split quizzes. Risk: misclassification puts a question in the wrong lecture's quiz.
3. **Body text numeric references** ("as we saw in Lecture 5...") must be updated. Each lecture body to be `grep`'d for `Lecture \d+` after content moves.
4. **CARLA exercise chain integrity** — the proposed new chain (L2 multi-sensor rig → L3 KF → L4 YOLO/DETR → L5 BEV+Seg → L6 SORT+KF → L7 SLAM → L8 routing → L9 predictor → L10 planner → L11 controller → L12 BC). Verify each new lecture's CARLA tasks fit this chain without rework.

---

## Decisions (2026-05-25)

- **Branch:** work directly on `main` (user override). Mitigation: commit
  after each stage (8–12 commits expected) so any step is revertable.
- **Staging:** build new structure under `docs/source/lectures/_new/`,
  not referenced from any toctree until the swap commit. Main stays
  buildable between intermediate commits.
- **New L6 thinness:** grow with deeper Temporal Reasoning (video
  transformers, optical flow, motion priors).
- **L1/L14 trims:** deferred to a follow-up PR. Both ride through this
  reorder unchanged.

## Execution order

1. Scaffold `_new/` with 14 folder skeletons
2. Pure copies: new L1, L2, L7, L8, L13, L14 (= unchanged from old)
3. Renumber-and-copy: new L4 (=old L3), new L10 (=old L9), new L11 (=old L10)
4. Extract: new L3 (from old L6 lines 1–563 + KF CARLA tasks + KF quiz/exercise questions)
5. Merge: new L5 (= old L4 + seg half of old L5)
6. Merge+grow: new L6 (= tracking half of old L5 + deep fusion of old L6 + new Temporal Reasoning depth)
7. Extract: new L9 (from old L11 prediction half)
8. Merge: new L12 (= old L12 + IL half of old L11)
9. Swap: `git rm` old `lectureN/`, `git mv _new/lectureN ../lectureN`
10. Update `lectures/index.rst`, `syllabus/index.rst`, `assignments/*.rst`
11. Sphinx build verification

