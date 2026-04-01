====================================================
L7: Localization & SLAM
====================================================

Overview
--------

Knowing **where the vehicle is** in the world with centimeter-level accuracy
is a prerequisite for safe autonomous driving. This lecture covers the full
spectrum of localization approaches -- from GNSS-based methods to dead
reckoning, probabilistic filters, and map-based scan matching -- before
introducing the Simultaneous Localization and Mapping (SLAM) problem, where
the vehicle must build its own map while localizing within it. You will
examine both the SLAM frontend (scan acquisition, feature extraction, ICP)
and backend (pose graph optimization, loop closure), and survey modern LiDAR
SLAM systems used in production AV stacks.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Formulate the localization problem and describe the coordinate systems and
  transformations used in AV systems.
- Describe GNSS-based localization including GPS, RTK, and PPP, and their
  accuracy limitations.
- Explain wheel odometry, visual odometry, and LiDAR odometry as dead reckoning
  methods, and characterize their drift properties.
- Apply the Extended Kalman Filter and particle filter to probabilistic
  localization with map observations.
- Describe scan matching (ICP and variants) and HD map-based localization.
- Formulate the SLAM problem as simultaneous state estimation and map building.
- Explain the SLAM frontend components: scan acquisition, preprocessing,
  feature extraction, ICP, and keyframe selection.
- Explain the SLAM backend: pose graph construction, optimization, and loop
  closure detection.
- Identify evaluation metrics for SLAM and localization systems.
- Describe modern LiDAR SLAM systems (LOAM, LeGO-LOAM) and their design
  choices.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l7_lecture
   l7_quiz
   l7_references

Next Steps
----------

- The next lecture covers **Motion Planning**: classical planners (A*, RRT,
  lattice planners), trajectory optimization, and diffusion-based planning.
- Install and explore the ``open3d`` Python library for point cloud processing:
  `http://www.open3d.org <http://www.open3d.org>`_.
- Review the LOAM paper: Zhang & Singh (2014) for the foundational LiDAR
  odometry and mapping algorithm.
- Explore the EVO trajectory evaluation tool:
  `https://github.com/MichaelGrupp/evo <https://github.com/MichaelGrupp/evo>`_.
