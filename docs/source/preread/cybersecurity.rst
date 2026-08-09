====================================================
Pre-Read: Automotive Cybersecurity
====================================================

.. admonition:: Read this before Lecture 14
   :class: important

   This page is **pre-read material** for L14. Cybersecurity is a full
   discipline in its own right; this page gives you the vocabulary and
   the standard (ISO/SAE 21434) so that the L14 discussion of system
   integration and safety can assume it rather than rebuild it.

   The L14 quiz may reference the attack surfaces and the TARA process
   described here.

Autonomous vehicles are networked computers on wheels -- and therefore
significant cybersecurity targets.

Attack Surfaces
---------------

.. tab-set::

   .. tab-item:: Sensor Spoofing

      - **LiDAR spoofing** -- Firing laser pulses at an AV's LiDAR sensor to
        inject phantom objects or remove real obstacles from the point cloud.
      - **GPS spoofing** -- Broadcasting false GPS signals to mislocalize the
        vehicle.
      - **Camera adversarial attacks** -- Applying specially crafted stickers to
        stop signs or lane markings that fool CNN-based perception.

   .. tab-item:: Communication Attacks

      - **V2X man-in-the-middle** -- Intercepting and modifying V2X messages
        to provide false traffic or hazard information.
      - **CAN bus injection** -- If physical access is obtained, injecting
        malicious CAN messages to override vehicle actuators.
      - **OTA update hijacking** -- Compromising the over-the-air update
        channel to install malicious software.

   .. tab-item:: Backend Attacks

      - **Fleet management server compromise** -- Attacking the cloud servers
        that push map updates or planner versions to the vehicle fleet.
      - **Data poisoning** -- Injecting adversarial data into the fleet's
        training pipeline to degrade the next model version.

ISO/SAE 21434 Framework
------------------------

ISO/SAE 21434 (Road Vehicles -- Cybersecurity Engineering) defines the
processes and requirements for managing cybersecurity throughout the vehicle
lifecycle:

1. **Threat Analysis and Risk Assessment (TARA)** -- Enumerate threat actors,
   attack vectors, and potential impacts. Assign a **CSMS attack feasibility**
   rating and risk level.
2. **Cybersecurity Goals** -- Define cybersecurity requirements for each
   identified risk.
3. **Implementation** -- Apply controls: encryption (TLS 1.3 for V2X),
   code signing (OTA updates), hardware security modules (HSM) for key storage.
4. **Post-deployment monitoring** -- Continuous vulnerability monitoring and
   incident response.

Secure Communication
---------------------

.. code-block:: text

   V2X Message                     Authenticated with:
   ─────────────────────────────────────────────────
   Basic Safety Message (BSM)  → IEEE 1609.2 certificates + ECDSA
   Service Advertisement       → ETSI ITS Security
   OTA Update Payload          → Code signing (RSA-4096 or ECDSA P-384)
   Sensor data (internal LAN)  → TLS 1.3 or DDS-Security


