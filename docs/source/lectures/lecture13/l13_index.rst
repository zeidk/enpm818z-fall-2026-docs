=========================================================
L13: Simulation, Scenario-Based Testing & World Models
=========================================================

Overview
--------

You have spent twelve weeks building a driving system. This lecture is about
the question nobody can avoid at the end: **how would you know whether it is
any good?**

You cannot answer it by driving. Demonstrating statistically that a vehicle is
as safe as a human would take hundreds of millions of miles, and roughly 11
billion to show it is 20% safer -- and every software release resets the
argument, because the thing you measured is no longer the thing you are
shipping. So the industry tests **scenarios** instead, which means someone has
to decide which scenarios, write them down, run them, and score them.

The lecture covers the functional / logical / concrete scenario layering and
the parameter explosion it implies; where scenarios come from (the ODD, SOTIF
triggering conditions, field data, and re-simulation of recorded drives); the
ASAM interchange formats and the ISO 34500 series that now govern this work;
the test pyramid from MIL and SIL through HIL and VIL to proving ground and
public road; and the distinction that decides whether any result means
anything -- whether the loop is **open** or **closed**.

It then takes apart the metric your own project is graded with, the CARLA
leaderboard driving score, and uses its history as a lesson in metric design:
the penalty was once exponential, agents learned that a short clean run beat a
long competent one, and version 2.1 changed the formula specifically to remove
that incentive.

**World models close the lecture, framed as the newest answer to the same
problem rather than as a separate topic** -- which is how Wayve themselves
frame them. GAIA-1 (2023) asked whether generative driving video was possible
at all; GAIA-3 (December 2025, 15B parameters) was pitched explicitly at
*evaluation and validation*; GAIA-4 (August 2026) closed the loop. In three
years the stated purpose migrated from generation to validation.

.. note::

   **This lecture makes the final report writable.** L1 promised that Stage 4
   of the ADS pipeline is *"scenario-based simulation, then closed course, then
   supervised on-road testing"*, and that the test scenarios come **from the
   ODD**. The final report is graded as a miniature of that stage: unseen
   scenarios, real numbers, and an honest account of what broke. This is where
   that loop closes.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why distance-based testing cannot support a safety claim, and why
  scenario-based testing replaced it.
- Distinguish :term:`Functional Scenario`, :term:`Logical Scenario` and
  :term:`Concrete Scenario`, and explain why one functional scenario implies
  thousands of concrete ones.
- Choose between grid sweep, random sampling, criticality-guided search and
  adversarial generation, and justify the choice for a given test budget.
- Derive a scenario set from an ODD and from SOTIF triggering conditions, and
  state what your ODD lets you decline to test.
- Describe the roles of ASAM :term:`OpenDRIVE` and :term:`OpenSCENARIO`, and
  the scope of the ISO 34500 series (:term:`ISO 34502`).
- Place a test at the correct level of the :term:`Test Pyramid` and say what
  that level cannot catch.
- Distinguish :term:`Open-Loop Evaluation` from :term:`Closed-Loop Evaluation`,
  and explain why :term:`Re-simulation` is a regression test rather than a
  validation.
- Compute and interpret the CARLA :term:`Driving Score`, and explain what
  :term:`Route Completion` alone conceals.
- Given a proposed metric, describe the cheapest agent that scores well on it.
- Explain what a world model is, what action-conditioning buys, and why
  physics-based simulators remain necessary for ground truth and
  repeatability.
- Describe the "world on rails" limitation and name an interaction it cannot
  evaluate.

.. admonition:: Materials in revision
   :class: note

   The lecture notes, exercises, quiz and references for this lecture are
   being revised against the current slide deck and are not published yet.
   This page will link to them once they are ready.

.. warning::

   **The world-model section dates fast.** Every claim in it is stamped, and
   GAIA-4 landed five weeks before this course began. Re-check the model
   generations, dates and parameter counts before each offering; the slide
   deck marks that section ``REFRESH``.


Next Steps
----------

- The next lecture covers **L14: System Integration, Safety & Industry
  Outlook**:

  - The full production stack, ROS 2 and DDS, and real-time latency budgets.
  - ISO 26262, ISO 21448 (SOTIF) and the UNECE regulation -- **where tonight's
    scenario framework stops being an engineering choice and becomes a
    regulatory requirement**.
  - Cybersecurity, V2X, ethics and liability, and the industry outlook.

- **For your final report**, three things follow directly from this lecture:

  - State which row of the test pyramid your numbers come from. It is SIL.
  - Report the :term:`Failure Boundary`, not the pass rate. A 100% pass rate
    usually means the scenarios were too easy.
  - For every metric you quote, say what behaviour would maximise it.

- Read the `CARLA Leaderboard evaluation rules
  <https://leaderboard.carla.org/evaluation_v2_1/>`_ -- you are graded with
  these, so read them once properly.
- Skim `ASAM OpenSCENARIO
  <https://www.asam.net/standards/detail/openscenario/>`_ to see what a
  scenario looks like written down.
- Optional, for the world-model half: the `Vista paper
  <https://arxiv.org/abs/2405.17398>`_ (NeurIPS 2024) and the `NVIDIA Cosmos
  technical report <https://arxiv.org/abs/2501.03575>`_.
