====================================================
References
====================================================


.. dropdown:: Standards and Regulations
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: SAE J3016
         :link: https://www.sae.org/standards/content/j3016_202104/
         :class-card: sd-border-secondary

         **Levels of Driving Automation**

         Taxonomy and definitions for terms related to driving automation
         systems for on-road motor vehicles.

      .. grid-item-card:: ISO 26262
         :link: https://www.iso.org/standard/68383.html
         :class-card: sd-border-secondary

         **Functional Safety**

         Road vehicles -- Functional safety standard for electrical and
         electronic systems.

      .. grid-item-card:: ISO 21448 (SOTIF)
         :link: https://www.iso.org/standard/77490.html
         :class-card: sd-border-secondary

         **Safety of the Intended Functionality**

         Addresses safety hazards that occur without a system failure.

      .. grid-item-card:: ISO/SAE 21434
         :link: https://www.iso.org/standard/70918.html
         :class-card: sd-border-secondary

         **Cybersecurity Engineering**

         Road vehicles -- Cybersecurity engineering standard.


.. dropdown:: Government and Policy
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: NHTSA Automated Vehicles
         :link: https://www.nhtsa.gov/technology-innovation/automated-vehicles
         :class-card: sd-border-secondary

         **AV Policy**

         NHTSA's technology and innovation page for automated vehicles.

      .. grid-item-card:: NIST AV Program
         :link: https://www.nist.gov/programs-projects/nist-automated-vehicles-program
         :class-card: sd-border-secondary

         **Measurement Science for AVs**

         NIST research on measurement science for automated vehicles.

      .. grid-item-card:: NIST SP 1900-301 (OES)
         :link: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1900-301.pdf
         :class-card: sd-border-secondary

         **Operating Envelope Specification**

         Griffor, Wollman & Greer (2021). *Automated Driving System Safety
         Measurement Part I: Operating Envelope Specification.* A structured,
         machine-readable description of the driving environment supporting
         calculation-based reasoning about performance.

      .. grid-item-card:: NIST IR 8527
         :link: https://doi.org/10.6028/NIST.IR.8527
         :class-card: sd-border-secondary

         **Standards and Performance Metrics**

         Schlenoff et al. (2024). A map of which standards apply where, and
         which performance metrics go with them. **Free, and the best single
         starting point for the standards landscape.**

      .. grid-item-card:: UNECE WP.29
         :link: https://unece.org/transport/vehicle-regulations/wp29/introduction
         :class-card: sd-border-secondary

         **Vehicle Regulations**

         World Forum for Harmonization of Vehicle Regulations. See also
         `UN Regulation No. 157 (ALKS)
         <https://unece.org/transport/documents/2021/03/standards/un-regulation-no-157-automated-lane-keeping-systems-alks>`_,
         which enabled the first Level 3 highway deployments.


.. dropdown:: Simulation and Tools
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: CARLA Simulator
         :link: https://carla.org/
         :class-card: sd-border-secondary

         **Open-Source AV Simulator**

         Built on Unreal Engine 4 for photorealistic driving simulation.

         +++

         - `Documentation (0.9.16) <https://carla.readthedocs.io/en/0.9.16/>`_
         - `Python API Reference <https://carla.readthedocs.io/en/0.9.16/python_api/>`_
         - `GitHub Repository <https://github.com/carla-simulator/carla>`_

      .. grid-item-card:: Visual Studio Code
         :link: https://code.visualstudio.com/
         :class-card: sd-border-secondary

         **Code Editor**

         Free, open-source editor with Python, ROS 2, and Git support.

      .. grid-item-card:: ROS 2 Humble
         :link: https://docs.ros.org/en/humble/
         :class-card: sd-border-secondary

         **Robotics Middleware**

         ROS 2 Humble Hawksbill documentation and tutorials.

      .. grid-item-card:: ROS 2 Jazzy
         :link: https://docs.ros.org/en/jazzy/
         :class-card: sd-border-secondary

         **Robotics Middleware**

         ROS 2 Jazzy Jalisco documentation and tutorials.


.. dropdown:: Incident Investigations
   :class-container: sd-border-secondary
   :open:

   - **NTSB/HAR-19/03** -- `Collision Between Vehicle Controlled by
     Developmental Automated Driving System and Pedestrian, Tempe, Arizona,
     March 18, 2018 <https://www.ntsb.gov/investigations/accidentreports/reports/har1903.pdf>`_.
     Highway Accident Report, adopted November 2019. Case ID HWY18MH010; the
     full investigation docket, including the Vehicle Automation Report, is
     `here <https://www.ntsb.gov/investigations/Pages/HWY18MH010.aspx>`_.
   - **California DMV** -- `Autonomous vehicle collision and disengagement
     reports <https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/>`_.
     The source of the disengagement figures discussed in the lecture, and a
     good way to see for yourself how loosely the term is defined.
   - **California PUC** -- `Autonomous vehicle programs
     <https://www.cpuc.ca.gov/regulatory-services/licensing/transportation-licensing-and-analysis-branch/autonomous-vehicle-programs>`_.
     Permit suspensions and passenger-service authority, including the record
     of the October 2023 post-collision pullover incident.


.. dropdown:: Industry Reports and Data
   :class-container: sd-border-secondary

   - `WHO Global Status Report on Road Safety 2023 <https://www.who.int/publications/i/item/9789240086517>`_
     -- source of the ~1.19 million annual road deaths figure.
   - `NHTSA Critical Reasons for Crashes <https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/812115>`_
     -- DOT HS 812 115. **Read this one before you quote the 94% figure**:
     it identifies the *last event in the causal chain*, not the cause of the
     crash.

   .. warning::

      Market-size forecasts for this field differ by a factor of ten depending
      on what gets counted, and ride counts and company statuses change
      quarterly. Attach a date to any figure you cite.


.. dropdown:: Textbooks and Surveys
   :class-container: sd-border-secondary

   - Pendleton, S. D. et al. (2017). *Perception, Planning, Control, and Coordination for Autonomous Vehicles.* Machines, 5(1), 6.
   - Yurtsever, E. et al. (2020). *A Survey of Autonomous Driving: Common Practices and Emerging Technologies.* IEEE Access, 8.
   - Kalra, N. & Paddock, S. M. (2016). *Driving to Safety: How Many Miles of Driving Would It Take to Demonstrate Autonomous Vehicle Reliability?* RAND Corporation.


.. dropdown:: Coding Standards
   :class-container: sd-border-secondary

   - `PEP 8 -- Style Guide for Python Code <https://peps.python.org/pep-0008/>`_
   - `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
   - `Git Documentation <https://git-scm.com/doc>`_
