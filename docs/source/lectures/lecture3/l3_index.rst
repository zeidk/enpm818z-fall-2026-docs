====================================================
L3: Probabilistic State Estimation & Sensor Fusion
====================================================

Overview
--------

**L2 gave you sensors that disagree. This lecture decides what to do
about it.**

Every sensor on the AV reports a different number for the same world, and
none of them is exactly right. The question is not which one to trust. It is
how much to trust each one, and that has an exact answer once you know how
uncertain each sensor is and that its errors have no bias. A **filter** does
this job: it keeps a running estimate of something no sensor gives you
exactly, updates it whenever a measurement arrives, and reports how uncertain
that estimate is right now. A good filter has two jobs: **combine** the
sensors into one answer, and report an uncertainty that can be **trusted**.

The lecture starts with the words the rest of it depends on, worked on six
GNSS readings from an AV parked on a surveyed spot: the road frame and the
**base link**, **uncertainty**, **noise** and **bias**, **variance**,
**standard deviation**, **covariance** and the covariance matrix
:math:`P`. Two receivers with the same :math:`\sigma` show that
:math:`\sigma` cannot see bias.

The **Kalman filter** is then built on one running example: an AV in a
tunnel with no GNSS, predicting from the IMU and updating from a camera that
matches exit signs against the HD map (a **sign match**). A prediction of
50 m with :math:`\sigma = 2` m and a sign match of 53 m with
:math:`\sigma = 1` m blend into 52.4 m with :math:`\sigma = 0.89` m, smaller
than either input. The same idea, written with matrices, gives the state,
the motion model, the measurement model, predict, update and the **Kalman
gain**, with the predict and update numbers taken from the hands-on script.

Next come the **four assumptions** the Kalman filter makes, and what happens
when each one breaks: a model that is not a straight line, a model that
curves too much or exists only as code, and a belief with more than one
peak. Each has an alternative filter. The **extended Kalman filter (EKF)**,
which GP3 uses, is built step by step: the tangent trick, the Jacobians,
:math:`Q_k`, and the catch, **divergence**. The **UKF** and the **particle
filter** are named as the other alternatives in class and worked out in the
appendix.

The last section covers what most people skip: they use the estimate and
ignore the covariance. A filter that is wrong does not crash. It reports a small covariance and keeps running. So the lecture
ends with a test of the filter's own uncertainty: the **normalized
innovation squared (NIS)**, which compares each surprise with the size the
filter predicted for it, and a **chi-square gate** that throws away a
reading that is wildly off.

.. important::

   **This lecture is the other half of L2.** L2 mounted and calibrated the
   sensors so that combining them is possible at all. L3 does the combining,
   with everything you calibrated last week.

.. important::

   **This lecture is for GP3**, whose EKF fuses GNSS fixes with IMU and
   wheel-speed data to estimate the AV's pose.

.. note::

   **Not in this lecture.** Detection is :doc:`L4 <../lecture4/l4_index>`.
   Fusion architectures, learned fusion, data association (deciding which
   measurement belongs to which object) and the Tempe crash (Uber, 2018) are
   L6. Monte Carlo Localization, which is the
   particle filter applied to localization, is
   L7.

.. admonition:: This week
   :class: warning

   - **CARLA cluster accounts** are set up this week.
   - **Teams form** this week.
   - **GP1 is posted** after class. It uses L2's calibration work, not this
     lecture's filter.


Learning Objectives
-------------------

These objectives are on a reading slide in the deck's appendix; they are
not shown in class. By the end of this lecture, you will be able to:

- Define **variance**, **standard deviation** and the **covariance
  matrix** :math:`P`.
- Say why the **Kalman gain** leans toward the more precise source, why the
  result beats **either input**, and on what assumption.
- Write down **predict** and **update**, and say what each term means.
- Name the **four assumptions**, and what the **EKF**, **UKF** and
  **particle filter** each replace.
- Build an **EKF**: :math:`f`, :math:`h`, their Jacobians, and
  :math:`Q_k`.
- Use the **innovation**, **NIS** and a **chi-square gate** to judge a
  running filter, and spot **divergence**.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_appendix
   l3_code
   l3_exercises
   l3_quiz
   l3_references


Next Steps
----------

- In the next lecture we cover **L4: Perception I, Detecting Objects**:

  - From pixels to features: what a CNN computes.
  - Grading a detector: IoU, precision, recall, mAP.
  - One-stage detectors (YOLO) and transformers (DETR, RT-DETR).
  - Two detectors side by side on a CARLA frame.

- **Before next class:**

  - Run the four hands-on scripts (KF, EKF, UKF, PF) and move every slider.
    The UKF and PF hands-on steps are in the appendix.
    **Most important: turn** :math:`Q` **down in** ``kf_tunnel.py`` **until
    the filter fails, and watch the share of time inside** :math:`1\sigma`
    **catch it.**
  - **Read the appendix**: the worked numbers, the UKF and particle filter
    details, and each filter's code.
  - Work through the L3 exercises.
  - **GP1 is posted.** It builds on L2's calibration work rather than on this
    lecture's filter.

- **How the lectures connect.** L1 gave the vocabulary and the failure
  cases. L2 gave the sensors and the geometry connecting them. L3 gave the
  filter that combines them, and the test that shows whether to trust it.
  L4 gives the detector that produces the measurements this filter has been
  assuming.
