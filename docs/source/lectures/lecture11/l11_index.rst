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

- **Behavior cloning.** Supervised learning on the expert's recorded drive.
  The clone's steering differs from the expert's by 0.37° on average, which
  is 2% of the 16.5° a sharp turn needs, yet it finishes only 5 of 20 test
  laps.
- **Compounding error.** The clone's error grows from 0.44° near the lane
  center to 2.41° near its edge, in states the recording never showed: 20% of
  its time is beyond the 0.61 m the expert ever reached. Its weight on the
  offset is 9 times too weak (0.38 against 3.44° per meter), because the
  detector's noise of 0.35 m hides an offset that varies by only 0.15 m.
- **DAgger.** The clone drives, the expert labels every state it reaches, and
  the clone is refit on all the data. One DAgger lap lifts it from 5 to 16
  finished laps, and it reaches 19 in all ten training runs. It costs an
  expert that can label any state, a safe place for a bad clone to drive, and
  a guarantee that holds only under conditions.
- **Commands.** At a junction the image does not say which way to go, and a
  clone fit to both ways steers about the average, which fits neither lane. A
  command from the route picks one head of the network.
- **Architectures and VLA models.** TransFuser (camera and LiDAR fused by
  attention, then waypoints), UniAD (the stack's modules inside one network),
  and vision-language-action models, whose answers take about 0.4 s: 3.3 m
  driven at 8 m/s.
- **Evaluation.** The clone with the better open-loop score (0.37° against
  0.47°) finishes fewer laps (5 against 19). Two benchmarks, NAVSIM and
  Bench2Drive, and the way GP4 scores your own stack in closed loop.
- **Modular or end-to-end.** The two designs side by side, four steps to
  compare them fairly, and GP5, an optional end-to-end project.


Learning Objectives
-------------------

After this lecture, you can:

- Write **behavior cloning** as supervised learning and fit a small policy.
- Explain, with measured numbers, why a clone with a small error on the
  expert's data leaves its lane: **compounding error**.
- Run **DAgger**'s loop and say what it costs.
- Say why a learned driver needs the route's **command** at a junction.
- Place **TransFuser**, **UniAD** and driving **VLA models**: inputs, outputs,
  what is learned.
- Tell an **open-loop** result from a **closed-loop** one.
- Compare a **modular** stack with an **end-to-end** driver fairly.


Lecture Materials
-----------------

- :doc:`l11_lecture`: the notes, following the slides shown in class.
  Material cut from class sits in closed "More detail" boxes, right after the
  part it explains. The hands-on commands are in the section "Hands-on: clone
  the expert, then run DAgger".
- :doc:`l11_exercises`: five take-home exercises, not graded: an open-loop
  score against a closed-loop one, noise and the offset weight, the data of a
  DAgger run, a junction with a tighter left turn, and a slow model with a
  fair comparison.
- :doc:`l11_quiz` and :doc:`l11_references`.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
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
