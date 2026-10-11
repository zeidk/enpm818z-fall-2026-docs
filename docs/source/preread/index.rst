====================================================
Pre-Read Material
====================================================

Some material this course depends on is **assumed knowledge** rather than
lecture content: either it comes from a prerequisite course, or it is a
supporting discipline broad enough that covering it properly would crowd
out the AV material it supports.

That material lives here. **Each page states when to read it.** Most are read
*before* the lecture that assumes them. One is context you will get more from
*after* the lecture, once it has given you something concrete to attach it to.

.. list-table::
   :widths: 30 15 55
   :header-rows: 1
   :class: compact-table

   * - Page
     - When
     - Why it is here
   * - :doc:`Development Environment </preread/dev-environment>`
     - Before L1
     - Ubuntu, ROS 2, Git, VS Code, and shell basics. Assumed from
       ENPM605; every group project depends on it.
   * - :doc:`Simulation for Automated Driving </preread/simulation>`
     - **After L2**
     - Why the industry simulates, what simulation cannot tell you, how it is
       done in production, and the landscape beyond CARLA. Read once L2 has
       shown you a simulator, and before GP1. Returned to in L12.
   * - :doc:`Grading a Detector and a Tracker </preread/detector-grading>`
     - Before GP2
     - IoU, precision and recall, AP, mAP\@0.5 and mAP\@0.5:0.95, ID
       switches and MOTA, one step at a time. Builds on L4.
   * - :doc:`SLAM with a LiDAR </preread/slam-lidar>`
     - After L6
     - The SLAM problem, EKF-SLAM, FastSLAM and grid maps, graph SLAM with
       Gauss-Newton, a LiDAR front end and Scan Context, all measured on the
       L6 drive.
   * - :doc:`Visual SLAM </preread/slam-visual>`
     - After L6
     - Camera model, ORB, stereo depth, PnP tracking, a bag of visual words,
       and a robust back end, on the L6 route recorded with a stereo camera.
   * - :doc:`Automotive Cybersecurity </preread/cybersecurity>`
     - Before L13
     - Attack surfaces, ISO/SAE 21434, and TARA. Supports the L13
       system-integration and safety discussion.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   dev-environment
   simulation
   detector-grading
   slam-lidar
   slam-visual
   cybersecurity
