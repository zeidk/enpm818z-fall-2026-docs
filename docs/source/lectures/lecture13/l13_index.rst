====================================================
L13: System Integration, Safety & Industry Outlook
====================================================

Overview
--------

This concluding lecture ties together the entire ENPM818Z curriculum by
examining how all AV stack components are integrated into a production system,
and then zooming out to the regulatory, ethical, and economic landscape that
will shape the industry through 2030 and beyond. We cover the middleware
infrastructure (ROS 2, DDS) that enables real-time communication between AV
modules, the safety standards (ISO 26262, SOTIF, UNECE GTR January 2026)
that govern deployment, cybersecurity threats and defenses (ISO/SAE 21434),
and the emerging role of V2X connectivity. The lecture concludes with an
honest assessment of where the industry is heading, an exploration of ethics
and liability, guidance on career paths, and a summary of the course.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the architecture of a complete production AV stack and explain
  how perception, prediction, planning, and control modules communicate
  in real time.
- Explain the role of ROS 2 and DDS (Data Distribution Service) in
  autonomous vehicle middleware, including the publish-subscribe paradigm
  and Quality of Service (QoS) settings.
- Define real-time constraints -- latency budgets, scheduling priorities,
  and deadline misses -- and explain their safety implications for ADS.
- Summarize ISO 26262 (functional safety, ASIL levels, V-model), ISO 21448
  (SOTIF), and the UNECE Global Technical Regulation on ADS (January 2026).
- Describe the automotive cybersecurity threat landscape and how ISO/SAE 21434
  and secure communication protocols address it.
- Explain the two dominant V2X standards (DSRC and C-V2X) and how V2X
  enables cooperative perception beyond line-of-sight.
- Assess the current state and near-term trajectory of the global AV
  industry, including the consolidation trend and US vs. China dynamics.
- Discuss the ethical dimensions of autonomous driving -- including the
  trolley problem and liability frameworks -- and identify career pathways
  in the AV industry.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l13_lecture
   l13_quiz
   l13_references


Next Steps
----------

- This is the **final lecture** of ENPM818Z. Your remaining deliverables are:

  - **Final Project** -- A functional ADS pipeline in CARLA demonstrating
    integration of perception, prediction, planning, and control. Submission
    deadline: see course syllabus.
  - **Final Quiz** -- Covering Lectures 11-13 (this quiz).

- Review all lecture materials and your assignment submissions as preparation
  for the final project integration phase.
- Explore career resources: IEEE Intelligent Vehicles Symposium (IV),
  CVPR Autonomous Driving Workshop, and the job boards of Waymo, Mobileye,
  Motional, and NVIDIA DRIVE.
