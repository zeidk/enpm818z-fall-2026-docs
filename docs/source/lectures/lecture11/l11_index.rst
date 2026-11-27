============================================================
L11: End-to-End Driving, VLA & Imitation Learning
============================================================

Overview
--------

Every earlier lecture built a driver from parts that people design, tune and
test one at a time: the stack of GP1 to GP4. This lecture builds a driver that
**learns from an expert**, and then asks how to compare the two.

The lecture follows one example, small enough to measure: one lap of CARLA's
Town01 (1442.6 m) at 8 m/s, an expert that keeps the AV in its lane, and a
clone that learns to copy a recording of the expert and then drives alone. The
clone sees what a noisy lane detector reports. No CARLA server is needed:
everything runs in numpy on a laptop.

- **Introduction.** A modular driver, built from parts that people design,
  against an end-to-end driver, one neural network trained from data, and
  which companies use which design. Four gains of end-to-end, and the running
  example.
- **Imitation learning.** Behavior cloning, supervised learning on the
  expert's recorded drive. The clone's steering differs from the expert's by
  0.37° on average, which is 2% of the 16.5° a sharp turn needs, yet it
  finishes only 5 of 20 test laps. Why: compounding error (its error grows
  from 0.44° near the lane center to 2.41° near its edge, in states the
  recording never showed), causal confusion, and averaging at a junction. Its
  weight on the offset is 9 times too weak (0.38 against 3.44° per meter),
  because the detector's noise of 0.35 m hides an offset that varies by only
  0.15 m. The fixes: DAgger (19 of 20 laps in all ten training runs, at the
  cost of an expert that can label any state and a safe place for a bad clone
  to drive), recovery data, a privileged teacher, and the route's command. Two other ways to learn from the same
  demonstrations: cost learning and a model of the world.
- **Reinforcement learning.** Learning from a reward, by trial, with no expert
  to copy, placed beside imitation.
- **Inside the networks.** TransFuser (camera and LiDAR fused by attention,
  then waypoints), UniAD (the stack's modules inside one network), and
  vision-language-action models, whose answers take about 0.4 s: 3.3 m driven
  at 8 m/s.
- **Scoring a driver.** The clone with the better open-loop score (0.37°
  against 0.47°) finishes fewer laps (5 against 19). NVIDIA's closed loop on
  recorded video, two benchmarks (NAVSIM and Bench2Drive), and the way GP4
  scores your own stack in closed loop.
- **Modular or end-to-end?** What end-to-end costs, the two designs side by
  side, four steps to compare them fairly, and GP5, an optional end-to-end
  project.


Learning Objectives
-------------------

After this lecture, you can:

- **Compare** a **modular** driver with an **end-to-end** driver, and say which
  companies use which.
- Train a network by **behavior cloning**, which is supervised learning on an
  expert's driving, then score it, see why it fails and fix it. That means:
  fit the clone to one recorded lap; score it on recorded data (**open
  loop**) and by letting it drive (**closed loop**); explain its failures with
  **compounding error**, **causal confusion** and **averaging**; and name the
  fixes, mainly **DAgger** and the route's **command** at a junction.
- Place cost learning and a model of the world beside behavior cloning, and
  **reinforcement learning**, learning from a reward with no expert to copy,
  beside imitation.
- Read published drivers such as **TransFuser** and **UniAD**, and driving
  **VLA models**.
- Tell **open-loop** from **closed-loop** evaluation, and read the benchmarks
  that score drivers in closed loop.
- Weigh what end-to-end costs, and compare the two kinds of driver fairly.


Lecture Materials
-----------------

- :doc:`l11_lecture`: the notes, following the slides shown in class.
  Material cut from class sits in closed "More detail" boxes, right after the
  part it explains. The hands-on commands are in the part "Hands-on code" of
  "Imitation Learning".
- :doc:`l11_interactive`: the slides as a web page you can try.
- :doc:`l11_exercises`: six take-home exercises, not graded: an open-loop
  score against a closed-loop one, noise and the offset weight, the data of a
  DAgger run, a junction with a tighter left turn, a slow model with a fair
  comparison, and a rare event in the driving data.
- :doc:`l11_quiz` and :doc:`l11_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_interactive
   l11_exercises
   l11_quiz
   l11_references


Next Steps
----------

- **Next class, L12: Simulation, Scenario-Based Testing & World Models
  (Thursday, December 10).** Where closed-loop tests like today's come from,
  and how to choose them. Quiz 5 is that day.
- **GP4 and the final report** were posted on November 19. GP4 is due on
  December 10, at L12. The final report is due on December 17.
- **Before then:** run the five hands-on parts (``road``, ``bc``, ``shift``,
  ``dagger`` and ``eval``) in the ``lecture11`` folder of the course's Python
  repo. GP5 is optional.
