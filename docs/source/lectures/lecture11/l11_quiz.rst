====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Working
   through this page is good preparation for one. Memorizing the answers
   below is not.

This quiz covers Lecture 11: the modular and the end-to-end driver, and what
end-to-end gains and costs; behavior cloning on one lap of Town01 and why a
clone that looks good on recorded data leaves its lane (compounding error,
causal confusion, averaging); DAgger, recovery data and what they cost; the
other ways to learn a driver; commands for a learned driver at a junction;
TransFuser, UniAD and driving VLA models; open-loop and closed-loop
evaluation; and how to compare a modular stack with an end-to-end driver.
Every question can be answered from the lecture notes, :doc:`l11_lecture`.
This quiz tests only what the deck teaches in class: nothing on this page
needs the lecture's "More detail" boxes.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.
   - The lecture's example is one lap of Town01 (1442.6 m) driven at 8 m/s
     with 20 steps per second, by an expert and by a clone trained on one
     recorded lap, and tested on 20 laps. Numbers that are not the lecture's
     are marked "chosen for this question".


----


Multiple Choice (Questions 1 to 19)
===================================

.. admonition:: Question 1
   :class: hint

   Which description matches the definition of end-to-end driving used in the
   lecture?

   A. A stack in which every part is trained on its own score, and the parts
      pass boxes and poses to each other.

   B. A fully differentiable program that takes raw sensor data as input and
      produces a plan, low-level control actions, or both.

   C. Any stack that uses a neural network in at least one of its parts.

   D. A driver that never uses a map.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The lecture quotes Chen et al.: fully differentiable programs that take raw
   sensor data as input and produce a plan and/or low-level control actions as
   output. Differentiable means the error at the output can train every part
   together. Option A describes your modular stack, and one neural network in
   one part (**C**) does not make a stack end to end. The definition says
   nothing about maps (**D**).


.. admonition:: Question 2
   :class: hint

   Steps 1 to 3 of behavior cloning are the same as training a detector:
   inputs, labels and a loss. What is new in step 4?

   A. The labels come from an expert.

   B. The loss is a squared loss.

   C. The policy's outputs move the AV, and the AV's new position decides the
      next input.

   D. The policy is trained by supervised learning.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   A detector's output never changes its next image. A driving policy's
   output moves the AV, so the AV's new position decides the next input. The
   other three choices describe steps 1 to 3, which a detector shares.


.. admonition:: Question 3
   :class: hint

   A road has a lane 3.6 m wide, and the AV is 1.8 m wide (both chosen for
   this question). How far can the AV's center move from the lane center
   before a wheel leaves the lane?

   A. 0.9 m

   B. 1.8 m

   C. 1.35 m

   D. 0.45 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   A wheel leaves the lane when the AV's center is more than
   (lane width − AV width) / 2 from the lane center: (3.6 − 1.8) / 2 = 0.9 m.
   The lecture's own numbers, a 4.0 m lane and a 2.0 m AV, give 1.0 m.


.. admonition:: Question 4
   :class: hint

   In the lecture's training run 6, the expert steers back 3.44° per meter of
   offset, and the clone's fit gives 0.38° per meter. About how many times too
   weak is the clone's weight on the offset?

   A. 0.38 times

   B. 3 times

   C. 3.44 times

   D. 9 times

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   3.44 / 0.38 = 9.05. Turned around, the clone's weight is 0.38 / 3.44 =
   0.11 of the expert's. The other weights, on the heading and the
   curvature, were close to the expert's.


.. admonition:: Question 5
   :class: hint

   Why is the clone's fitted weight on the offset so small?

   A. The clone was trained on too few pairs.

   B. The expert stays near the center, so the true offset varies by only
      0.15 m, and the detector's noise of 0.35 m hides it: the pairs form a
      flat cloud, and a line fit to it is flat.

   C. Gradient descent stopped too early.

   D. The expert's own rule has a small weight on the offset.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Most of the spread in the offset the clone sees is noise (0.35 / 0.15 =
   2.3 times the true spread), and the expert's steering does not follow
   noise. Training used 3607 pairs and a closed-form solution, with no
   gradient descent (**A**, **C**). The expert's weight is 3.44° per meter
   (**D**).


.. admonition:: Question 6
   :class: hint

   The lecture trains on five expert laps instead of one: the offset weight
   goes from 0.38 to 0.42, and the clone finishes 6 laps instead of 5. What
   does the lecture conclude?

   A. More data fixes the clone.

   B. More data makes the clone worse.

   C. It is not a change we can read, because a new recording alone moves the
      count by several laps.

   D. The clone now matches the expert.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Across ten training runs, behavior cloning finishes 2 to 9 laps of 20, so
   5 to 6 is inside that spread. The extra laps also stay near the center, so
   they add more of the same states.


.. admonition:: Question 7
   :class: hint

   Which statement defines open-loop error?

   A. The policy's error on recorded inputs: its outputs are compared with the
      expert's and never move the AV.

   B. The share of the route the AV completes.

   C. The policy's error while it drives.

   D. An error that can only be measured in a simulator.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   Open loop reads recorded inputs and compares the policy's output with the
   expert's, so it needs only a dataset. The share of the route completed
   (**B**) and the error while the policy drives (**C**) are closed-loop
   measures, and a simulator (**D**) is not needed for open loop.


.. admonition:: Question 8
   :class: hint

   The clone's average steering error is 0.44° when the AV is 0.00 to 0.25 m
   from the lane center, and 2.41° when it is 0.75 to 1.00 m from it. How many
   times larger is the second error?

   A. 0.18 times

   B. 2.4 times

   C. 3 times

   D. 5.5 times

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   2.41 / 0.44 = 5.48, about 5.5. The error is largest where the AV is
   farthest from the center, which is where the clone needs to be best.


.. admonition:: Question 9
   :class: hint

   In DAgger, the clone drives a lap. Who gives the labels for the states it
   reached?

   A. The clone itself.

   B. The expert, always, whoever drove.

   C. A person watching the lap, who steers as they see fit.

   D. The driver of that iteration, which is the clone after iteration 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The AV executes the clone's steering, but the data stores what the expert
   would have steered in each state. So the data holds the states the clone
   itself reaches, with the expert's labels.


.. admonition:: Question 10
   :class: hint

   In the lecture's training run 6, the behavior-cloned clone finishes 5 of 20
   test laps. How many does it finish after one DAgger lap?

   A. 9

   B. 12

   C. 16

   D. 20

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   One DAgger lap lifts the clone from 5 to 16 finished laps, and the second
   to 19, where it stays. The expert finishes all 20.


.. admonition:: Question 11
   :class: hint

   Why does a learned driver need the route's command at a junction?

   A. The camera image of a junction does not say which way to go, so without
      a command the clone averages the ways it saw.

   B. The command makes the network train faster.

   C. The command replaces the camera image.

   D. A junction has more lanes than the network can see.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The camera sees the same junction whether the expert went straight or
   turned left. A clone fit to both by least squares steers about the average,
   which fits neither lane. In conditional imitation, the command picks which
   head of the network produces the steering.


.. admonition:: Question 12
   :class: hint

   In TransFuser, which step is not learned by imitation?

   A. The convolution layers that read the camera image.

   B. The attention blocks between the two branches.

   C. The waypoint predictor.

   D. The two PID controllers that turn the waypoints into steering, throttle
      and brake.

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The authors write that they use two PID controllers for lateral and
   longitudinal control, so the last step is not learned. Everything in blue
   in the figure, the convolution layers, the attention blocks and the
   waypoint predictor, is trained by imitation.


.. admonition:: Question 13
   :class: hint

   DriveVLM's vision-language model has an average inference speed of 410 ms
   on the NVIDIA OrinX chip in the car. At the lecture's 8 m/s, how far does
   the AV drive during one answer?

   A. 0.4 m

   B. 0.8 m

   C. 3.3 m

   D. 33 m

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   0.41 × 8 = 3.3 m. The lane keeper steers every 0.05 s, which is 0.4 m
   (**A**), so a slow model needs a fast partner. 0.8 m (**B**) is Alpamayo 1's
   99 ms at 8 m/s, on a different chip.


.. admonition:: Question 14
   :class: hint

   The lecture compares your stack with UniAD, part by part. What does UniAD
   remove?

   A. The tasks, such as tracking and planning.

   B. The hand-designed message between the tasks.

   C. The need for labels.

   D. The planner.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   UniAD keeps your stack's tasks and their names, and puts them in one
   network. What it removes is the hand-designed message between them: learned
   queries take its place. It still needs labels for every module, and it has
   a planner.


.. admonition:: Question 15
   :class: hint

   NAVSIM scores a plan on real recorded drives, and the planner is queried
   only in the first frame of each scene. What does that mean for compounding
   error?

   A. NAVSIM shows compounding error well, because it uses real data.

   B. The plan never moves the AV, so NAVSIM cannot show compounding error.

   C. NAVSIM is a closed-loop benchmark.

   D. NAVSIM needs CARLA.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The evaluated policy and the environment do not influence each other, and
   the planner is queried only in the first frame of each scene. NAVSIM is a
   middle ground between open loop and closed loop: real sensor data and a
   score that checks the plan, but the plan never moves the AV. Only a closed
   loop shows compounding error. Bench2Drive is the one that runs in CARLA.


.. admonition:: Question 16
   :class: hint

   Which of these is one of the four costs of an end-to-end driver that the lecture
   lists, as opposed to one of its four gains?

   A. One goal for all parts.

   B. It is hard to open: it is a black box.

   C. Less computing, because one shared extractor finds the features once.

   D. It may get better with more data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The four costs are: hard to open (a black box), no proof of safety, rare cases (the
   long tail), and states the expert never showed. The other three choices are
   gains: one goal for all parts, less computing and (possibly) better with more
   data.


.. admonition:: Question 17
   :class: hint

   De Haan et al. trained two clones with the same network on the same driving.
   Clone A sees the windshield and the dashboard. Clone B sees the same image
   with the dashboard masked out. What happened?

   A. Both drive well, because both have low training loss.

   B. Clone A drives better, because it has more information.

   C. Clone A does not drive well and clone B does: A learned to brake only when the brake light on the dashboard is on.

   D. Clone B does not drive well, because it lacks the dashboard.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   This is causal confusion. The brake light is the effect of braking, but clone A
   can reach a low training loss by treating it as the cause. On the road the
   light is not on yet, so A does not brake. The authors write that "access to
   more information can yield worse performance".


.. admonition:: Question 18
   :class: hint

   Which way of learning a driver needs no expert's actions to copy, and learns
   from a reward by trial?

   A. Behavior cloning.

   B. Reinforcement learning.

   C. Cost learning.

   D. DAgger.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Reinforcement learning learns from a reward, by trial. Behavior cloning and
   DAgger copy an expert, and cost learning learns a cost from the expert's
   demonstrations, then drives the cheapest trajectory.


.. admonition:: Question 19
   :class: hint

   NVIDIA's network and ChauffeurNet both train on off-center views that the
   expert never drove. Where does the label of such a view come from?

   A. An expert labels each view after the drive, as in DAgger.

   B. The label comes from geometry: the steering that leads back to the lane.

   C. The clone labels its own views.

   D. The label is random.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   Like DAgger, both add states the expert never drove. Unlike DAgger, no expert
   labels them. NVIDIA labels each view with the steering that returns the car
   "to the desired location and orientation in two seconds", and ChauffeurNet
   jitters the expert's path and draws a smooth path through the moved point.


----


True or False (Questions 20 to 28)
==================================

.. admonition:: Question 20
   :class: hint

   True or false: a clone whose steering is within 0.2° of the human driver's
   on a held-out recorded lap does not need a closed-loop test.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The 0.2° is measured on the human's states only. Once the clone drives, it
   reaches states the recording does not have, where its error is unknown.
   The lecture's clone had 0.37° on recorded data and still finished only 5
   laps of 20.


.. admonition:: Question 21
   :class: hint

   True or false: in all ten training runs, behavior cloning has the lower
   open-loop error than DAgger and also the fewer finished laps.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Behavior cloning fits the expert's own states best. DAgger's fit also
   covers the states where the AV drifts, so on the expert's states alone it
   fits slightly worse (0.47° against 0.37° in run 6) and drives much better
   (19 laps against 5).


.. admonition:: Question 22
   :class: hint

   True or false: the bound of Ross and Bagnell says behavior cloning's total
   cost grows linearly with the length of the drive, :math:`T`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The bound grows quadratically, :math:`O(T^2)`, rather than as
   :math:`O(T)`: one mistake can take the policy off the expert's states, and
   from there it may keep making mistakes for the rest of the drive. The
   lecture also says the bound is a worst case, not a curve our lap must
   follow.


.. admonition:: Question 23
   :class: hint

   True or false: the CARLA Leaderboard, where TransFuser was tested in closed
   loop, has since closed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The lecture says TransFuser was tested closed loop in CARLA, on the CARLA
   Leaderboard, which has since closed.


.. admonition:: Question 24
   :class: hint

   True or false: GP5, the end-to-end project, is part of the group-project
   grade and the final report.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   GP5 is optional and not graded: no points, no bonus, nothing due and
   nothing submitted. It does not count toward the group-project grade or the
   final report.


.. admonition:: Question 25
   :class: hint

   True or false: your final report evaluates your modular pipeline.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Your final report evaluates your modular pipeline, on the three scenarios
   the instructor provides. End-to-end driving is the optional GP5.


.. admonition:: Question 26
   :class: hint

   True or false: in the lecture's ten training runs, DAgger finishes 19 of
   20 test laps every time, and always misses the same test lap.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   DAgger finishes 19 in every run, and it always misses test lap 8. The
   expert's own largest offset, 0.75 m (the limit is 1.0 m), is on that lap,
   so it is the hardest lap. Behavior cloning, in comparison, finishes 2 to 9
   laps of 20 over the ten runs.


.. admonition:: Question 27
   :class: hint

   True or false: on nuScenes, open loop, a model that uses no camera images can
   have a lower average distance error than models that use cameras.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   AD-MLP plans from the AV's own past motion and the route command, with no
   camera, and has the lowest average distance error in its Table 1: 0.29 m,
   against 1.03 m for UniAD and 0.37 m for VAD-Base. An open-loop score on
   nuScenes does not show that a model sees the road: 73.9% of the nuScenes data
   involve driving straightforwardly.


.. admonition:: Question 28
   :class: hint

   True or false: an event that happens once per billion miles, and 100 million
   miles of driving data (the numbers of Koopman's example), leave about a 90%
   chance that the data holds no example of it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Expected sightings: 100,000,000 / 1,000,000,000 = 0.1. If sightings come
   independently (a Poisson count), the chance of never seeing the event is
   e\ :sup:`-0.1` = 0.90.


----


Short Answer (Questions 29 to 32)
=================================

.. admonition:: Question 29
   :class: hint

   Explain compounding error with the lecture's numbers: where does the
   clone's error grow, and why does that make the AV leave the lane?

.. dropdown:: Answer
   :class-container: sd-border-success

   The clone's steering error depends on how far the AV is from the lane
   center: 0.44° near the center and 2.41° at 0.75 to 1.00 m, 5.5 times
   more. Near the center the clone steers back too little, so a gust or a turn
   pushes it a little farther out. Farther out, its error is larger, so it
   goes farther out again. Each step starts where the last one left the AV, so
   the errors add up instead of averaging out. The training data cannot help
   in those states: the expert's true offset has a standard deviation of
   0.15 m and never passes 0.61 m, while the clone spends 20% of its time
   beyond 0.61 m. See "Why the Clone Fails" in :doc:`l11_lecture`.


.. admonition:: Question 30
   :class: hint

   DAgger raised the lecture's clone from 5 finished laps to 19. Name what
   DAgger costs.

.. dropdown:: Answer
   :class-container: sd-border-success

   Three costs. First, an expert who can label any state. A program that
   reads the simulator's state can, but a human must say what they would
   steer in a state they did not drive, often from a recording. Second, a
   place for a bad clone to drive: the first DAgger lap is driven by the
   behavior-cloned clone, which left its lane on 15 of 20 test laps, so such
   laps belong in a simulator or with a safety driver. Third, a guarantee that
   holds only under conditions, on the expert's ability to recover and on the
   class of policies. See "What DAgger costs" in :doc:`l11_lecture`.


.. admonition:: Question 31
   :class: hint

   A team says its end-to-end model beats a modular stack, based on one run of
   each. Using the lecture's four steps for a fair comparison, say what the
   team must add, and use the lecture's clone as the example for the point
   about runs.

.. dropdown:: Answer
   :class-container: sd-border-success

   The four steps: the same routes and scenarios, none used in training or
   tuning; closed loop, with the same metrics (route completion, collisions,
   red lights); several runs, with the spread reported; and a statement of
   what each driver was given (sensors, the map, the route, privileged
   information). One run each does not give a spread. The lecture's clone
   finished 2 to 9 laps of 20 depending only on the training run, so a single
   run can make a worse design look better. See "A fair comparison, in four
   steps" in :doc:`l11_lecture`.


.. admonition:: Question 32
   :class: hint

   Phil Koopman gives two reasons why testing alone cannot show that a learned
   driver is safe. Give them.

.. dropdown:: Answer
   :class-container: sd-border-success

   Covering every neuron does not help: a chip test can exercise every gate and
   show that it is there, but "if you exercise all the neurons in an artificial
   neural network, it doesn't prove anything". Driving more miles does not help
   either: brute-force testing takes about a billion miles, and the machine
   learning has probably been retrained 100 times in that billion miles, so none
   of it counts. See "Why testing cannot prove safety" in :doc:`l11_lecture`.


