==================================================================
CARLA Setup Guide - Ubuntu 22.04 (Native)
==================================================================

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Version/Details**
   * - Course
     - ENPM818Z -- On-Road Automated Vehicles
   * - Ubuntu Version
     - 22.04 (Jammy Jellyfish)
   * - CARLA Version
     - 0.9.16
   * - Installation Method
     - Native (No Docker)

---------------------------------------------------------
Overview
---------------------------------------------------------

This guide walks you through setting up CARLA 0.9.16 on Ubuntu 22.04 using a **native installation** (no Docker required). You will use a **custom ROS 2 bridge package** that bypasses CARLA's native ROS 2 implementation due to a known bug (see :ref:`known-issue-ubuntu22`).

**What You'll Install:**

- CARLA 0.9.16 standalone application
- CARLA Python API
- Custom ROS 2 bridge package

.. note::
   **Why Native?** Native CARLA installation is simpler than Docker, requires no special configuration, and provides direct access to the Python API. Perfect for development and learning!

---------------------------------------------------------
Prerequisites
---------------------------------------------------------

System Requirements
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Requirement**
   * - Operating System
     - Ubuntu 22.04 (Jammy Jellyfish)
   * - ROS 2 Distribution
     - Already installed
   * - GPU
     - NVIDIA GPU (recommended), AMD/Intel also work
   * - RAM
     - Minimum 8 GB, Recommended 16 GB
   * - Disk Space
     - ~10 GB for CARLA and dependencies
   * - Python
     - 3.10 (comes with Ubuntu 22.04)

Verify Your Ubuntu Version
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsb_release -a

You should see ``Ubuntu 22.04`` in the output.

---------------------------------------------------------
Step 1: Download and Install CARLA 0.9.16
---------------------------------------------------------

Download CARLA
~~~~~~~~~~~~~~

.. code-block:: bash

   # Create directory for CARLA
   mkdir -p ~/carla
   cd ~/carla

   # Download CARLA 0.9.16 (this will take 5-10 minutes)
   wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.16.tar.gz

   # Extract (this will take a few minutes)
   tar -xzf CARLA_0.9.16.tar.gz

   # Verify extraction
   ls -lh CARLA_0.9.16/

You should see directories like ``CarlaUE4/``, ``PythonAPI/``, etc.

Make CARLA Executable
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd CARLA_0.9.16
   chmod +x CarlaUE4.sh

Test CARLA
~~~~~~~~~~

.. code-block:: bash

   # Run CARLA (will take 30-60 seconds to start)
   ./CarlaUE4.sh -quality-level=Low

You should see the CARLA window open with a 3D city environment. Press ``Ctrl+C`` in the terminal to stop CARLA.

.. tip::
   **First Launch:** CARLA's first launch may take longer as it compiles shaders. Subsequent launches will be faster.

---------------------------------------------------------
Step 2: Install CARLA Python API
---------------------------------------------------------

The Python API is already included with CARLA, but we need to install it:

.. code-block:: bash

   # Navigate to Python API directory
   cd ~/carla/CARLA_0.9.16/PythonAPI/carla/dist

   # Find the .whl file for Python 3.10
   ls carla-0.9.16-cp310-cp310-linux_x86_64.whl

   # Install the wheel file
   pip3 install carla-0.9.16-cp310-cp310-linux_x86_64.whl

   # Verify installation
   python3 -c "import carla; print(f'CARLA Python API: {carla.__version__}')"

Expected output: ``CARLA Python API: 0.9.16``

---------------------------------------------------------
Step 3: Install Additional Dependencies
---------------------------------------------------------

.. code-block:: bash

   # Install required Python packages
   pip3 install numpy pygame

   # Verify installations
   python3 -c "import numpy; import pygame; print('Dependencies OK')"

---------------------------------------------------------
Step 3.5: Maps
---------------------------------------------------------

Highway assignments (for example, behavioral planning) use **Town04**, which has
a dedicated multi-lane highway loop. **Town04 already ships with the CARLA
0.9.16 package you extracted in Step 1. You do not need to download anything.**

The package contains these maps:

.. code-block:: text

   Town01   Town01_Opt   Town02     Town02_Opt
   Town03   Town03_Opt   Town04     Town04_Opt
   Town05   Town05_Opt   Town10HD   Town10HD_Opt

The ``_Opt`` variants are *layered* maps whose scenery (parked cars, foliage,
street props) can be toggled at runtime.

.. warning::
   Do **not** download ``AdditionalMaps_0.9.16.tar.gz`` to obtain Town04. That
   archive is a **14.8 GB download**, and it does not contain Town04 -- you
   already have it. Fetch it only if an assignment specifically names Town06,
   Town07, or Town11--Town15; extract it over your ``CARLA_0.9.16`` directory,
   which places the assets directly under ``CarlaUE4/Content/``.

Confirm the Maps
~~~~~~~~~~~~~~~~

Start CARLA in one terminal, then in a second terminal ask the server what it
has:

.. code-block:: bash

   python3 -c "
   import carla
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   for m in sorted(client.get_available_maps()):
       print('  -', m.split('/')[-1])
   "

---------------------------------------------------------
Troubleshooting
---------------------------------------------------------

CARLA Won't Start
~~~~~~~~~~~~~~~~~

**Symptom:** Black screen or crash on launch

**Solutions:**

1. Check graphics drivers:

   .. code-block:: bash

      nvidia-smi

2. Try OpenGL instead of Vulkan:

   .. code-block:: bash

      cd ~/carla/CARLA_0.9.16
      ./CarlaUE4.sh -opengl -quality-level=Low

3. Check system requirements are met (8 GB RAM minimum)

Cannot Connect to CARLA
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``Failed to connect to CARLA: timeout``

**Solutions:**

1. Wait for CARLA to fully load (30-60 seconds after window appears)

2. Check CARLA is running:

   .. code-block:: bash

      ps aux | grep CarlaUE4
      netstat -tuln | grep 2000

3. Verify Python API:

   .. code-block:: bash

      python3 -c "import carla; c = carla.Client('localhost', 2000); c.set_timeout(5.0); print(c.get_server_version())"

Python API Import Error
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``ModuleNotFoundError: No module named 'carla'``

**Solutions:**

1. Re-install CARLA Python API:

   .. code-block:: bash

      cd ~/carla/CARLA_0.9.16/PythonAPI/carla/dist
      pip3 install --force-reinstall carla-0.9.16-cp310-cp310-linux_x86_64.whl

2. Verify installation:

   .. code-block:: bash

      python3 -c "import carla; print(carla.__file__)"

---------------------------------------------------------
Performance Optimization
---------------------------------------------------------

For Better Performance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Lower graphics quality
   ./CarlaUE4.sh -quality-level=Low -nosound -vulkan

   # Reduce camera resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=640 -p image_height:=480

   # Run headless (no graphics window)
   ./CarlaUE4.sh -RenderOffScreen -quality-level=Low

For Better Quality
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher graphics
   ./CarlaUE4.sh -quality-level=Epic -vulkan

   # Higher resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=1920 -p image_height:=1080

CARLA Command-Line Options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Option**
     - **Description**
   * - ``-quality-level=Low``
     - Low graphics quality (fastest)
   * - ``-quality-level=Epic``
     - Highest graphics quality
   * - ``-nosound``
     - Disable audio (reduces CPU usage)
   * - ``-vulkan``
     - Use Vulkan renderer (NVIDIA preferred)
   * - ``-opengl``
     - Use OpenGL (fallback for compatibility)
   * - ``-RenderOffScreen``
     - Headless mode (no window)
   * - ``-windowed``
     - Run in window (not fullscreen)
   * - ``-ResX=1280 -ResY=720``
     - Set window resolution

---------------------------------------------------------
Comparison with Ubuntu 24.04 Setup
---------------------------------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Aspect**
     - **Ubuntu 22.04 (This Guide)**
     - **Ubuntu 24.04**
   * - Ubuntu Version
     - 22.04 (Jammy)
     - 24.04 (Noble)
   * - Python Version
     - 3.10
     - 3.12
   * - Installation
     - Native (tar.gz)
     - Docker
   * - Setup Complexity
     - Simpler
     - More complex (Docker config)
   * - GPU Setup
     - Direct
     - Requires nvidia-docker
   * - Functionality
     - Identical
     - Identical

Both setups use the same ROS 2 package and provide identical functionality.

---------------------------------------------------------
Next Steps
---------------------------------------------------------

With CARLA installed and running, continue to:

- :doc:`Using CARLA from Python <carla-python>` -- write scripts that connect to
  the server, load maps, and watch the simulation.
- :doc:`CARLA ROS 2 Bridge <carla-ros2>` -- build and run the course's ROS 2
  bridge package.

Both pages cover this platform and Ubuntu 24.04, with the differences shown in
tabs.

---------------------------------------------------------
References
---------------------------------------------------------

- CARLA Documentation: https://carla.readthedocs.io/en/0.9.16/
- CARLA Downloads: https://github.com/carla-simulator/carla/releases/tag/0.9.16
- Python API Reference: https://carla.readthedocs.io/en/0.9.16/python_api/
- GitHub Issue (Double Slash Bug): https://github.com/carla-simulator/carla/issues/9278
