====================================================
L3: Probabilistic State Estimation & Fusion
====================================================

Overview
--------

**L2 gave you sensors that disagree. This lecture decides what to do
about it.**

Every sensor on the vehicle reports a different number for the same world,
and none of them is exactly right. The question is not which one to trust.
It is how much to trust each one, and that turns out to have an exact answer
whenever you know how uncertain each sensor is.

The lecture starts by defining the two words the rest of it depends on,
**variance** and **confidence**, because both have a loose everyday meaning
and a strict technical meaning, and the strict ones are used here.

From there it builds upward from one dimension. Two estimates and their
variances give you **inverse-variance weighting**, which is the Kalman
update in one dimension and is the part worth understanding before the
matrix version. Adding a prediction step and more dimensions gives the
**Kalman filter**. Then we relax its assumptions one at a time. Nonlinear
motion gives the **EKF** and the **UKF**, and a belief with several separate
peaks gives the **particle filter**.

The last third is the part most courses skip. A filter that is wrong does
not crash. It reports a small covariance and keeps running. So the lecture
covers how to test whether a filter's reported uncertainty is correct,
using innovations, consistency checks, divergence and gating. It closes on
**data association**, the step that decides which measurement belongs to
which track, and the place where the Tempe crash went wrong.

.. important::

   **This lecture is the other half of L2.** L2 was about placing and
   calibrating sensors so that combining them is possible at all. L3 is the
   how the combining is actually done. Everything you calibrated last week is
   what the filter combines here.

.. note::

   **Deep learning fusion is not in this lecture.** Cross-attention,
   BEVFusion and learned feature level fusion are covered in
   :doc:`L6 <../lecture6/l6_index>`, alongside perception and tracking.
   Monte Carlo Localization, which is the particle filter applied to the
   localization problem, is :doc:`L7 <../lecture7/l7_index>`.

.. admonition:: This week, before the lecture
   :class: warning

   - **Quiz 1** is given at the **start** of class and covers **L1 and L2**.
     Closed notes, about 15 minutes.
   - The **setup milestone** is due. CARLA running, ROS 2 workspace built,
     sensors publishing. Individual, and graded pass or fail.
   - **Teams form**, and **GP1 is posted** after the lecture.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define **variance** and **standard deviation**, explain why the distances
  are squared, and say what a standard deviation tells you about where
  readings land.
- Explain the difference between the loose engineering meaning of
  **confidence** and the strict statistical one, and state what a Kalman
  filter's covariance actually claims.
- Explain why the plain average of two estimates is the wrong answer, and
  compute the **inverse-variance weighted** estimate instead.
- Show that combining two independent estimates gives an uncertainty
  **smaller than either input**, and say which assumption that result
  depends on.
- Compare **early**, **intermediate** and **late** fusion, and say which one
  a given constraint forces on you.
- Write down the Kalman filter's predict and update steps, and say which
  step always grows the covariance and which always shrinks it.
- Explain what the **Kalman gain** does, and predict how it behaves when
  :math:`R \gg P` and when :math:`R \ll P`.
- Name the **four assumptions** that make the Kalman filter optimal, and
  work out which one a given situation breaks.
- Explain how the **EKF** handles a nonlinear model, and describe the
  failure that this introduces.
- Explain how the **UKF** uses sigma points to avoid Jacobians, and say when
  that is worth the extra cost.
- Say when a **particle filter** is the right choice, in terms of the shape
  of the belief rather than how nonlinear the model is.
- Use the **innovation** and a **NIS** check to decide whether a running
  filter can be trusted, and recognise **divergence** when you see it.
- Apply a **chi-square gate** to reject a bad measurement, and explain why
  this answers the GNSS multipath problem left open in L2.
- Set up the **data association** problem and choose between NN, GNN, JPDA
  and MHT for a given scene.
- Describe a **track lifecycle**, meaning birth, confirmation, coasting and
  deletion, and explain why Tempe was a failure of this stage rather than of
  detection.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_exercises
   l3_quiz
   l3_references


Next Steps
----------

- In the next lecture we cover **L4: Perception I, Object Detection from
  YOLO to DETR**:

  - CNN fundamentals and the YOLO family.
  - DETR and detection as set prediction.
  - What convolutional and transformer detectors each cost you.
  - Running a detector as a ROS 2 node.

- This lecture assumed measurements simply arrive. L4 covers where they
  come from: the detector that turns pixels into the boxes this filter
  tracks.
- Complete the L3 exercises. **Exercise 5, the divergence hunt, is the one
  that matters**, and it is the debugging skill GP3 will demand.
- **GP1 is posted this week.** It builds on L2's calibration work, not on
  this lecture's filter.
