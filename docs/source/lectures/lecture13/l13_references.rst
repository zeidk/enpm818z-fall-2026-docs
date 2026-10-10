====================================================
References
====================================================


.. dropdown:: Safety Standards
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ISO 26262
         :link: https://www.iso.org/standard/68383.html
         :class-card: sd-border-secondary

         **Road Vehicles -- Functional Safety**

         The primary standard for functional safety in automotive electrical
         and electronic systems. Defines ASIL levels A-D and the V-model
         development process.

      .. grid-item-card:: ISO 21448 (SOTIF)
         :link: https://www.iso.org/standard/77490.html
         :class-card: sd-border-secondary

         **Safety of the Intended Functionality**

         Addresses safety hazards from performance limitations of intended
         functions, including sensor limitations and algorithmic failure modes.

      .. grid-item-card:: ISO/SAE 21434
         :link: https://www.iso.org/standard/70918.html
         :class-card: sd-border-secondary

         **Road Vehicles -- Cybersecurity Engineering**

         Joint ISO/SAE standard for automotive cybersecurity, including TARA
         methodology and security lifecycle requirements.

      .. grid-item-card:: UNECE GTR on ADS
         :link: https://unece.org/transport/vehicle-regulations
         :class-card: sd-border-secondary

         **UNECE Global Technical Regulation**

         The first international safety framework for ADS (approved January
         2026). Safety case approach for demonstrating ADS acceptability.


.. dropdown:: Middleware and Communication
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: ROS 2 Documentation
         :link: https://docs.ros.org/en/humble/
         :class-card: sd-border-secondary

         **ROS 2 Humble Hawksbill**

         Official ROS 2 documentation including DDS configuration, QoS
         policies, real-time executor, and security (SROS 2).

      .. grid-item-card:: DDS Standard (OMG)
         :link: https://www.omg.org/spec/DDS/
         :class-card: sd-border-secondary

         **Data Distribution Service (DDS)**

         OASIS/OMG standard for real-time publish-subscribe middleware.
         Foundational to ROS 2 communication.

      .. grid-item-card:: DDS-Security
         :link: https://www.omg.org/spec/DDS-SECURITY/
         :class-card: sd-border-secondary

         **DDS Security Specification**

         Security plugin specification for DDS, enabling authentication,
         encryption, and access control in ROS 2 (SROS 2).

      .. grid-item-card:: ROS 2 Real-Time Guide
         :link: https://docs.ros.org/en/humble/Guides/Real-Time-Programming.html
         :class-card: sd-border-secondary

         **Real-Time Programming with ROS 2**

         Official guide on scheduling, memory management, and latency
         optimization for real-time AV applications.


.. dropdown:: V2X and Connectivity
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: 3GPP C-V2X (LTE-V / NR-V2X)
         :link: https://www.3gpp.org/technologies/keywords-acronyms/103-v2x
         :class-card: sd-border-secondary

         **Cellular V2X Standards**

         3GPP specifications for LTE-V2X (Release 14) and 5G NR-V2X
         (Release 16). Technical foundation of C-V2X communication.

      .. grid-item-card:: IEEE 802.11p / DSRC
         :link: https://standards.ieee.org/ieee/802.11p/3953/
         :class-card: sd-border-secondary

         **Dedicated Short-Range Communications**

         IEEE 802.11p standard for DSRC V2X communication in the 5.9 GHz
         band. Being phased out in the US in favor of C-V2X.

      .. grid-item-card:: ETSI ITS Standards
         :link: https://www.etsi.org/technologies/automotive-intelligent-transport/
         :class-card: sd-border-secondary

         **Intelligent Transport Systems (Europe)**

         ETSI standards for V2X in Europe, including cooperative awareness
         messages (CAM) and decentralized environmental notification messages
         (DENM).

   - Wang, Z. et al. (2020). *V2VNet: Vehicle-to-Vehicle Communication for
     Joint Perception and Prediction.* ECCV 2020. Seminal cooperative
     perception paper using V2X for joint detection and forecasting.
   - Xu, R. et al. (2022). *OPV2V: An Open Benchmark Dataset and Fusion
     Pipeline for Perception with Vehicle-to-Vehicle Communication.* ICRA
     2022.


.. dropdown:: Industry Reports and Outlook
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Waymo Safety Report
         :link: https://waymo.com/safety/
         :class-card: sd-border-secondary

         **Waymo Safety**

         Waymo's public safety documentation, including crash statistics,
         safety methodology, and ODD descriptions.

      .. grid-item-card:: NHTSA AV Policy
         :link: https://www.nhtsa.gov/technology-innovation/automated-vehicles
         :class-card: sd-border-secondary

         **NHTSA Automated Vehicles**

         US federal policy for ADS, including Standing General Order on
         crash reporting and technology innovation resources.

   - RAND Corporation (2020). *Measuring Automated Vehicle Safety.*
     Methodology for assessing AV safety performance.
   - McKinsey & Company (2023). *Autonomous Driving's Future.*
     Industry outlook and economics of robotaxi services.
   - IEEE Spectrum (2025). *The State of Self-Driving Cars in 2026.*
     Annual industry survey of deployment status, technology trends, and
     regulatory developments.


.. dropdown:: Ethics and Liability
   :class-container: sd-border-secondary

   - Awad, E. et al. (2018). *The Moral Machine Experiment.* Nature, 563,
     59-64. Cross-cultural study of ethical preferences in AV decision-making
     scenarios across 2.3 million participants in 233 countries.
   - Bonnefon, J. F. et al. (2016). *The Social Dilemma of Autonomous
     Vehicles.* Science, 352(6293), 1573-1576.
   - Geistfeld, M. A. (2017). *A Roadmap for Autonomous Vehicles: State
     Tort Liability, Automobile Insurance, and Federal Safety Regulation.*
     California Law Review, 105(6).
   - German Road Traffic Act (StVG) Amendment (2021). First national
     legislation placing liability on ADS operator for Level 4 incidents.


.. dropdown:: Career Resources
   :class-container: sd-border-secondary

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: IEEE IV Symposium
         :link: https://ieee-iv.org/
         :class-card: sd-border-secondary

         **IEEE Intelligent Vehicles Symposium**

         Premier academic venue for autonomous driving research. Good
         source for internship and job connections.

      .. grid-item-card:: CVPR AV Workshop
         :link: https://cvpr.thecvf.com/
         :class-card: sd-border-secondary

         **CVPR Autonomous Driving Workshop**

         Annual workshop at CVPR showcasing the latest perception and
         planning research from industry and academia.

      .. grid-item-card:: Waymo Careers
         :link: https://waymo.com/careers/
         :class-card: sd-border-secondary

         **Waymo**

         Roles in perception, prediction, planning, systems, and
         software infrastructure across the full ADS stack.

      .. grid-item-card:: NVIDIA DRIVE Careers
         :link: https://www.nvidia.com/en-us/self-driving-cars/
         :class-card: sd-border-secondary

         **NVIDIA Autonomous Vehicles**

         Roles spanning hardware (SoC), software (DRIVE platform),
         world models (Cosmos), and AV tooling.
