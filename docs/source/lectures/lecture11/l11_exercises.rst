====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises, built on the Lecture 11 notes, :doc:`l11_lecture`.
They use only what the lecture teaches in class, with new numbers. Exercise 1
compares an open-loop score with a closed-loop one. Exercise 2 asks how a
noisy detector changes what a clone learns. Exercise 3 counts the data of a
DAgger run. Exercise 4 works a junction with a tighter left turn. Exercise 5
turns a model's answer time into meters and checks a comparison for fairness.
Exercise 6 asks how likely a rare event is to appear in driving data.

.. note::

   Every exercise can be done with a calculator.

   **The lecture's example:** one lap of Town01, 8 m/s, 20 steps per second,
   an AV with a 2.9 m wheelbase. Numbers that are not the lecture's are marked
   "chosen for this exercise".


.. dropdown:: Exercise 1. An Open-Loop Score and a Closed-Loop Score
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Put an open-loop error in proportion to the steering a turn needs, and say
   which of two clones to trust.

   .. raw:: html

      <hr>

   **Specification**

   Two clones of the same expert (chosen for this exercise). Clone A has an
   open-loop error of 0.30° on a recorded expert lap, and finishes 7 of 20
   test laps. Clone B has an open-loop error of 0.42° and finishes 18 of 20.
   The sharpest turn of the road has a radius of 12 m, and the AV's wheelbase
   is 2.9 m.

   .. raw:: html

      <hr>

   **Part A. How big is the error?**

   1. How much steering does the AV need in the turn?
   2. What share of that steering is clone A's open-loop error? And clone B's?

   .. raw:: html

      <hr>

   **Part B. Which clone?**

   3. Which clone has the better open-loop score? Which one drives better?
   4. Why can the clone with the better open-loop score drive worse? Use the
      words *open loop*, *closed loop* and *states*.

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: arctan(2.9 / 12) = 13.6°.

      Question 2: clone A: 0.30 / 13.6 = 0.022, about 2%. Clone B:
      0.42 / 13.6 = 0.031, about 3%. Both errors are small next to the
      steering the turn needs.

      Question 3: clone A has the better open-loop score (0.30° against
      0.42°). Clone B drives better: it finishes 18 laps of 20 against 7.

      Question 4: an open-loop score is measured on recorded inputs, which
      are the expert's states, and the clone's output never moves the AV. In
      closed loop the clone's own steering decides the next state. A clone
      can fit the expert's states best and still be weak in the states it
      reaches when it drifts, where the recording has no examples. The
      lecture's behavior cloning clone and DAgger clone are an example: the
      behavior cloning clone had the lower open-loop error in all 10 training
      runs and finished fewer laps in all 10.


.. dropdown:: Exercise 2. Noise and the Offset Weight
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare the noise of a detector with the spread of the true offset, and say
   what each case does to the clone's weight on the offset.

   .. raw:: html

      <hr>

   **Specification**

   A different recording of the expert (chosen for this exercise): the true
   offset in the training data has a standard deviation of 0.20 m. Case 1:
   the lane detector adds noise of 0.50 m. Case 2: the detector adds noise of
   0.10 m. In the lecture, the spread was 0.15 m and the noise 0.35 m.

   .. raw:: html

      <hr>

   **Part A. The ratio**

   1. In case 1, how many times larger is the noise than the true spread? In
      case 2?
   2. In the lecture, the same ratio was 0.35 / 0.15. What is it?

   .. raw:: html

      <hr>

   **Part B. What the clone learns**

   3. In which case does most of the spread in "offset seen" come from noise?
      What does the cloud of recorded pairs look like then (offset seen
      against the expert's steering), and what is the fitted weight on the
      offset: close to the expert's or much smaller?
   4. In case 1, you record five expert laps instead of one. Does the weight
      get close to the expert's? Why or why not?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4.

   .. dropdown:: Guidance
      :color: success

      Question 1: case 1: 0.50 / 0.20 = 2.5 times. Case 2: 0.10 / 0.20 = 0.5,
      so the noise is half the spread.

      Question 2: 0.35 / 0.15 = 2.3.

      Question 3: in case 1. The expert's steering follows the true offset
      and not the noise, so the recorded pairs form a flat cloud, and a line
      fit to a flat cloud is flat: the weight on the offset is much smaller
      than the expert's. In case 2 the true offset is most of what the
      detector reports, so the pairs follow the expert's rule more closely
      and the weight is closer to the expert's. The lecture's quieter detector
      (0.117 m, a third of the noise) gave a weight of 1.85° per meter
      against the 0.38 of the noisy one, and the clone finished all 20 laps.

      Question 4: no. The extra laps stay near the center too, so they add
      more of the same states, with the same noise. In the lecture, five
      laps moved the weight from 0.38 to 0.42 and the laps finished from 5
      to 6, a change that is smaller than the spread between training runs
      (2 to 9 laps).


.. dropdown:: Exercise 3. Counting the Data of a DAgger Run
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Count the labeled states of a DAgger run, say who drives and who labels in
   each iteration, and find how much of the data lies off center.

   .. raw:: html

      <hr>

   **Specification**

   A road with a lap of 1200 m (chosen for this exercise), driven at 8 m/s
   with 20 steps per second. The run has 5 iterations: iteration 1 is the
   expert's lap (behavior cloning), iterations 2 to 5 are DAgger laps. Every
   lap is driven to the end. Use the lecture's choice of :math:`\beta`.

   .. raw:: html

      <hr>

   **Part A. Counting**

   1. How many steps does one lap have?
   2. How many labeled states does the data hold after iteration 5?

   .. raw:: html

      <hr>

   **Part B. Who does what**

   3. Who drives in iteration 1? Who drives in iteration 3?
   4. In iteration 3, whose steering does the AV execute, and whose steering
      is stored as the label?

   .. raw:: html

      <hr>

   **Part C. Off center**

   5. In the expert's lap, 2% of the steps are more than 0.5 m from the lane
      center. In each DAgger lap, 12% are (both chosen for this exercise).
      What share of all the data after iteration 5 is beyond 0.5 m?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 5, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: 1200 / 8 = 150 s, and 150 × 20 = 3000 steps.

      Question 2: 5 laps × 3000 = 15,000 labeled states.

      Question 3: in iteration 1, :math:`\beta_1 = 1`: the expert drives,
      which is behavior cloning. In iteration 3, :math:`\beta_3 = 0`: the
      newest clone drives alone.

      Question 4: the AV executes the clone's steering. The label is always
      the expert's: what the expert would have steered in that state.

      Question 5: the expert's lap: 0.02 × 3000 = 60 steps. Each DAgger lap:
      0.12 × 3000 = 360 steps, and four laps give 1440. Together 60 + 1440 =
      1500 steps, and 1500 / 15,000 = 0.10, so 10% of the data. In the
      lecture the same share went from 2.0% of the expert's lap to 10.8% of
      all the data.


.. dropdown:: Exercise 4. A Junction With a Tighter Left Turn
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Repeat the lecture's junction argument with new numbers, and say what the
   route's command changes.

   .. raw:: html

      <hr>

   **Specification**

   A junction where the left turn has a radius of 8.0 m (chosen for this
   exercise). The wheelbase is 2.9 m. The recording holds expert drives both
   ways, half going straight and half turning left, and the camera sees the
   same junction each time.

   .. raw:: html

      <hr>

   **Part A. The average clone**

   1. What does the expert steer going straight? And turning left?
   2. A clone fit to both by least squares gives about the average. What is
      that steering?
   3. The average steering makes a circle of radius :math:`2.9 / \tan(\delta)`.
      What is the radius? How many times larger is it than the left turn's
      radius?

   .. raw:: html

      <hr>

   **Part B. The command**

   4. A conditional imitation network has four heads: follow lane, left,
      straight and right. The route says "left" at this junction. Which head
      produces the steering, and what do the other three heads do?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: straight: 0°. Left: arctan(2.9 / 8.0) = 19.9°.

      Question 2: the average of 0° and 19.9° is 19.93 / 2 = 9.96°, about 10°.

      Question 3: 2.9 / tan(9.96°) = 16.5 m. That is 16.5 / 8.0 = 2.1 times
      the left turn's radius, so the AV turns too wide for the left lane. It
      does not follow the straight lane either: the camera image alone does
      not say which way to go.

      Question 4: the left head produces the steering. The command acts as a
      switch, so the other three heads are not connected to the output at
      that moment.


.. dropdown:: Exercise 5. A Slow Model, and a Fair Comparison
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Turn a model's answer time into meters driven, and find what is unfair in
   a comparison.

   .. raw:: html

      <hr>

   **Specification**

   A vision-language model that needs 0.25 s per answer (chosen for this
   exercise), in an AV that drives at 12 m/s (chosen for this exercise). A
   lane keeper in the same AV steers every 0.05 s.

   .. raw:: html

      <hr>

   **Part A. Meters per answer**

   1. How far does the AV drive during one answer of the model?
   2. How far does it drive between two steering commands of the lane keeper?
   3. Why does DriveVLM-Dual hand its trajectory to a classical planner?

   .. raw:: html

      <hr>

   **Part B. A fair comparison**

   Team A reports the score of its modular pipeline from one run, on the
   route it used to tune its controller gains, with the true pose from the
   simulator. Team B reports an end-to-end model's score from ten runs, on
   routes the model never saw in training, with camera images only. Both are
   closed-loop scores.

   4. The lecture gives four steps for a fair comparison. Which of the four
      does Team A's report break? Say why for each.

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 4.

   .. dropdown:: Guidance
      :color: success

      Question 1: 0.25 × 12 = 3.0 m.

      Question 2: 0.05 × 12 = 0.6 m.

      Question 3: a slow model gives a new answer only every 3.0 m, while the
      AV needs a command every 0.6 m. DriveVLM-Dual hands the trajectory to a
      classical planner, which refines it at a high rate.

      Question 4: three of the four steps are broken.

      - **Same routes and scenarios, none used in training or tuning:** broken.
        Team A tuned its gains on the route it reports.
      - **Closed loop, with the same metrics:** not broken. Both scores are
        closed loop. (The question does not say whether the metrics match, so
        Team A should say which ones it used.)
      - **Several runs, and report the spread:** broken. Team A reports one
        run.
      - **Say what each one was given:** broken. Team A used the true pose,
        which is privileged information, and Team B used camera images only.


.. dropdown:: Exercise 6. A Rare Event in the Driving Data
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work out the chance that a rare event has no example in the training data,
   and say why a heavy tail makes this a problem for a learned driver.

   .. raw:: html

      <hr>

   **Specification**

   An event happens once per 500 million miles of driving (chosen for this
   exercise). A company has 250 million miles of driving data. Treat the
   sightings as independent, as a Poisson count, as the lecture does.

   .. raw:: html

      <hr>

   **Part A. The chance of no example**

   1. How many sightings does the data hold on average?
   2. What is the chance that the data holds no example of the event? Use
      :math:`e^{-x}`, where :math:`x` is your answer to question 1.

   .. raw:: html

      <hr>

   **Part B. Many events**

   3. In Koopman's words, a long tail is rare events, and a heavy tail is "a
      lot of things". Why does fixing one rare event not solve the problem
      when there are a billion different ones?

   .. raw:: html

      <hr>

   **Deliverable**

   The answers to questions 1 to 3, each with its arithmetic.

   .. dropdown:: Guidance
      :color: success

      Question 1: 250,000,000 / 500,000,000 = 0.5 sightings.

      Question 2: :math:`e^{-0.5}` = 0.61. The data holds no example of the
      event with a chance of about 61%.

      Question 3: each of the billion events is rare, so each is likely to
      have few examples or none in the data, as in question 2. Fixing one
      event leaves the others. In Koopman's words, if you have a billion of
      them "you're going to see one every mile. And if you fix it, that
      doesn't help you".
