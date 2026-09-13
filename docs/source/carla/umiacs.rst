==================================================================
CARLA Setup Guide - UMIACS Nexus (Apptainer)
==================================================================

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Version/Details**
   * - Course
     - ENPM818Z -- On-Road Automated Vehicles
   * - Platform
     - UMIACS Nexus cluster (RHEL 8, SLURM)
   * - CARLA Version
     - 0.9.16
   * - Installation Method
     - Apptainer (SIF container)
   * - Scheduler
     - SLURM

---------------------------------------------------------
Overview
---------------------------------------------------------

This guide runs CARLA 0.9.16 on the **UMIACS Nexus cluster** using Apptainer.
It is an alternative to running CARLA on your own machine, and it exists for
one reason: **Nexus does not permit Docker**, so the
:doc:`Ubuntu 24.04 Docker guide <ubuntu24>` cannot be followed there.

.. important::

   **This page is optional.** If CARLA already runs on your own laptop via the
   :doc:`Ubuntu 22.04 <ubuntu22>` or :doc:`Ubuntu 24.04 <ubuntu24>` guide,
   you do not need Nexus at all. Use this page if you have no NVIDIA GPU of
   your own, or if your GPU is too small for the assignments.

Nexus is a **shared, scheduled, headless** system. That changes three things
about how you work, and every difference on this page follows from them:

.. list-table::
   :widths: 26 74
   :header-rows: 1
   :class: table-hover

   * - **Property**
     - **What it means for you**
   * - Shared
     - You do not own the machine. You ask SLURM for a GPU, wait, and get one
       for a bounded time. Other students are on the same node.
   * - Scheduled
     - Nothing runs on the login node. A CARLA server started outside a job
       allocation will be killed, and you may lose cluster access for it.
   * - Headless
     - There is no screen. No CARLA window, no RViz2, no Pygame viewer. You
       save images and rosbags to disk and copy them back.

.. note::

   **What this page does not change.** The CARLA Python API, the course ROS 2
   bridge, and every assignment are identical on Nexus. Only *starting the
   server* and *getting a GPU* differ.

.. admonition:: What has been tested, and what you must check yourself
   :class: caution

   The container mechanics here were verified end to end on an NVIDIA GPU
   with Apptainer 1.5.3: the CARLA server renders on the GPU from a
   read-only SIF, a non-default RPC port works, a client in the ROS 2
   container reaches a server in the CARLA container over ``localhost``, and
   forcing software rendering reproduces the crash in
   :ref:`umiacs-renderer-crash` exactly.

   **Nexus runs an older Apptainer than that**, and two things depend on the
   specific node you are given: whether ``--nv`` supplies the NVIDIA Vulkan
   driver file automatically, and where that file lives on the host.
   :ref:`umiacs-icd-check` resolves both in one command, and it is the step
   to do first.

---------------------------------------------------------
Part 1: Introduction to UMIACS
---------------------------------------------------------

What UMIACS Is
~~~~~~~~~~~~~~

**UMIACS** is the University of Maryland Institute for Advanced Computer
Studies. It is a research institute, not a piece of software and not a
website. Among other things, it operates computing infrastructure for UMD
researchers and for some courses.

Three names appear constantly and are easy to confuse:

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: table-striped

   * - **Name**
     - **What it actually is**
   * - UMIACS
     - The institute. It sets the policies and runs the hardware.
   * - **Nexus**
     - The **GPU cluster** you will actually use. This is where CARLA runs.
   * - ``wiki.umiacs.umd.edu``
     - UMIACS's documentation site. Authoritative for anything on this page
       that changes.

.. seealso::

   `UMIACS Nexus documentation <https://wiki.umiacs.umd.edu/umiacs/index.php/Nexus>`_

How a Cluster Differs From Your Laptop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On your laptop you open a terminal and run CARLA. On a cluster there are
**two different kinds of machine**, and running the wrong thing on the wrong
one is the most common beginner mistake.

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - **Machine**
     - **Role**
   * - **Submission node**
     - What you SSH into. Named ``nexus<abbreviation>00`` or
       ``...01``. Use it to edit files, clone repositories, and submit jobs.
       It has **no GPU worth using**, and it is shared by everyone.
   * - **Compute node**
     - Where your work actually runs. You never SSH into one directly; SLURM
       places you there when it grants your job. This is where the GPU is,
       and where CARLA must run.

.. danger::

   **Never start CARLA on a submission node.** It is a shared login host with
   no allocated GPU. Starting a game engine on it degrades the machine for
   every other user, and UMIACS staff will notice. Everything in Part 3 runs
   inside a SLURM allocation, on a compute node.

SLURM in Four Commands
~~~~~~~~~~~~~~~~~~~~~~

**SLURM** is the scheduler. You describe the resources you need; it finds a
compute node and gives it to you.

.. list-table::
   :widths: 26 74
   :header-rows: 1
   :class: table-hover

   * - **Command**
     - **What it does**
   * - ``srun --pty ... bash``
     - Requests resources and drops you into an **interactive** shell on a
       compute node. Use this while developing.
   * - ``sbatch script.sh``
     - Submits a **batch** job that runs unattended and writes its output to
       a file. Use this for long runs.
   * - ``squeue --me``
     - Shows your queued and running jobs.
   * - ``scancel <jobid>``
     - Cancels a job.

.. important::

   **Your job ends, and everything in it dies.** When the time limit expires
   or you exit the shell, SLURM kills the CARLA server with it. Anything not
   written to persistent storage is gone. Plan your work in bounded sessions.

Storage
~~~~~~~

.. list-table::
   :widths: 26 26 48
   :header-rows: 1
   :class: table-striped

   * - **Location**
     - **Persists?**
     - **Use it for**
   * - Home directory
     - Yes, backed up
     - Code, scripts, your ROS 2 workspace. **Quota is small** -- never put
       container images here.
   * - ``/fs/nexus-scratch/<user>``
     - Yes, **not** backed up
     - Large files, container images, recorded data. 200 GB by default.
   * - ``/scratch0``
     - **No** -- node-local, purged
     - Fast temporary space *during a job*. It is a different disk on every
       compute node, so do not expect to find yesterday's files.
   * - ``/fs/nexus-containers``
     - Yes, read-only
     - Shared container images maintained by UMIACS.

.. warning::

   **Class accounts do not get network scratch.** If your ENPM818Z account is
   a class account, ``/fs/nexus-scratch/<user>`` will not exist and you have
   only your home directory and node-local ``/scratch0``. This is why
   :ref:`umiacs-shared-sif` matters so much: a 7.7 GB image you cannot store
   is a 7.7 GB image you must not download.

Getting Access
~~~~~~~~~~~~~~

.. important::

   ENPM818Z is offered through Maryland Applied Graduate Engineering, which is
   **not** part of UMIACS. A UMIACS account is not automatic with your UMD
   directory ID.

   Your instructor arranges a **class account** for the course. If you cannot
   log in, that is the first thing to check -- do not assume you have done
   something wrong.

You will need, in this order:

1. A UMIACS class account for ENPM818Z.
2. **GlobalProtect VPN**, connected. Nexus submission nodes are not reachable
   from the open internet.
3. The name of your submission node, from the UMIACS Directory application.

---------------------------------------------------------
Part 2: One-Time Setup
---------------------------------------------------------

Step 1: Log In
~~~~~~~~~~~~~~

Connect the VPN first, then:

.. code-block:: bash

   ssh <your-username>@nexus<abbreviation>00.umiacs.umd.edu

Confirm where you are and that Apptainer exists:

.. code-block:: bash

   hostname
   apptainer --version

.. note::

   Apptainer is already installed cluster-wide. There is **nothing to
   install** and no ``sudo`` anywhere in this guide -- which is precisely why
   Nexus allows it and does not allow Docker.

Step 2: Point Apptainer's Caches at Scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apptainer writes large temporary files while it works. Left alone it puts them
in your home directory and **will blow through your quota**.

Add this to the end of ``~/.bashrc``:

.. code-block:: bash

   # ---------------------------------------------------------------------------
   # Apptainer scratch configuration (ENPM818Z)
   # Keeps multi-GB temporary files out of the home quota.
   # ---------------------------------------------------------------------------
   export APPTAINER_CACHEDIR=/fs/nexus-scratch/$USER/.apptainer/cache
   export APPTAINER_TMPDIR=/fs/nexus-scratch/$USER/.apptainer/tmp
   mkdir -p "$APPTAINER_CACHEDIR" "$APPTAINER_TMPDIR"

Then reload:

.. code-block:: bash

   source ~/.bashrc

.. important::

   **If you are on a class account** and ``/fs/nexus-scratch/$USER`` does not
   exist, substitute ``/scratch0/$USER`` in both lines. Node-local scratch is
   fine for *temporary* files. It is not fine for the image itself.

.. _umiacs-shared-sif:

Step 3: Get the Container Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A container image in Apptainer is a **single file** ending in ``.sif``. You
need two:

.. list-table::
   :widths: 22 16 62
   :header-rows: 1
   :class: table-hover

   * - **Image**
     - **Size**
     - **What it is for**
   * - ``carla_0.9.16.sif``
     - ~7.7 GB
     - The CARLA **server**. Needs the GPU. Nothing else runs here.
   * - ``ros_jazzy.sif``
     - ~274 MB
     - ROS 2 Jazzy, **and** the home of every Python client you write --
       see the warning in :ref:`umiacs-python-client`.

**The CARLA image first.**

.. tab-set::

   .. tab-item:: Shared image (preferred)
      :sync: shared

      If UMIACS is hosting the course image, use it directly. Nothing to
      download, nothing counted against your quota:

      .. code-block:: bash

         ls -lh /fs/nexus-containers/enpm818z/

      Set a variable you will reuse all semester. Put it in ``~/.bashrc``:

      .. code-block:: bash

         export CARLA_SIF=/fs/nexus-containers/enpm818z/carla_0.9.16.sif

   .. tab-item:: Build your own
      :sync: own

      .. warning::

         This needs roughly **40 GB of free temporary space** and takes
         10--30 minutes. Do it only if no shared image is available, and
         **never on a class account** with no network scratch.

      .. code-block:: bash

         cd /fs/nexus-scratch/$USER
         apptainer pull carla_0.9.16.sif docker://carlasim/carla:0.9.16
         export CARLA_SIF=/fs/nexus-scratch/$USER/carla_0.9.16.sif

**Then the ROS 2 image.** It is small, so pulling your own costs little:

.. tab-set::

   .. tab-item:: Shared image (preferred)
      :sync: shared

      .. code-block:: bash

         export ROS_SIF=/fs/nexus-containers/enpm818z/ros_jazzy.sif

   .. tab-item:: Pull your own
      :sync: own

      .. code-block:: bash

         cd /fs/nexus-scratch/$USER      # or /scratch0/$USER on a class account
         apptainer pull ros_jazzy.sif docker://ros:jazzy-ros-base
         export ROS_SIF=/fs/nexus-scratch/$USER/ros_jazzy.sif

Put both ``export`` lines in ``~/.bashrc`` so they survive between sessions.

.. note::

   You cannot *build* an image from a definition file on UMIACS -- that needs
   administrative rights. Pulling a published image into a SIF, as above, is
   permitted. See the
   `UMIACS Apptainer page <https://wiki.umiacs.umd.edu/umiacs/index.php/Apptainer>`_.

.. _umiacs-icd-check:

Step 4: Confirm the GPU Renderer (do this once)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the **single most important check on this page**, and skipping it
produces the most confusing failure in the whole guide.

CARLA renders with **Vulkan**. For Vulkan to reach the NVIDIA GPU, the
container needs a small file called an **ICD** (Installable Client Driver)
that tells it where the NVIDIA driver is. The CARLA image ships ICDs for
Intel, AMD and a *software* renderer, but **not** for NVIDIA -- that one has
to come from the host.

Newer Apptainer supplies it automatically with ``--nv``. Older Apptainer does
**not**. Find out which you have.

Get a GPU for a moment (see :ref:`umiacs-request-gpu` for what the flags
mean):

.. code-block:: bash

   srun --pty --gres=gpu:rtxa5000:1 --cpus-per-task=4 --mem=16gb --time=00:15:00 bash

Then, on the compute node:

.. code-block:: bash

   apptainer exec --nv $CARLA_SIF ls /usr/share/vulkan/icd.d/

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - **If the output contains** ``nvidia_icd.json``
     - **If it does not**
   * - Your Apptainer injects it for you. Use **Recipe A** below.
     - You must bind it in yourself. Use **Recipe B** below.

Also find where the ICD lives on the host, because the path differs between
Linux distributions:

.. code-block:: bash

   ls /usr/share/vulkan/icd.d/nvidia_icd.json /etc/vulkan/icd.d/nvidia_icd.json 2>/dev/null

Write down whichever path exists. You will need it for Recipe B.

.. tip::

   **Recipe B is safe on both.** If you would rather not think about it, use
   Recipe B always -- binding an ICD that is already there changes nothing,
   and it additionally silences a harmless ``MESA: warning`` line.

---------------------------------------------------------
Part 3: Running CARLA
---------------------------------------------------------

.. _umiacs-request-gpu:

Step 5: Request a GPU
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   srun --pty --gres=gpu:rtxa5000:1 --cpus-per-task=4 --mem=16gb --time=02:00:00 bash

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: table-hover

   * - **Flag**
     - **Why**
   * - ``--pty ... bash``
     - Interactive shell on the compute node.
   * - ``--gres=gpu:rtxa5000:1``
     - One GPU, **of a named type**. See the warning below -- this is not
       optional advice.
   * - ``--cpus-per-task=4``
     - Unreal is multi-threaded. Four is the default QoS maximum.
   * - ``--mem=16gb``
     - CARLA is comfortable here. The default QoS allows up to 32 GB.
   * - ``--time=02:00:00``
     - Two hours. Ask for what you need; shorter jobs schedule sooner.

.. warning::

   **Ask for an RTX-class GPU by name.** Nexus has both RTX cards
   (``rtxa4000``, ``rtxa5000``, ``rtxa6000``, ``rtx3090``, ``l40s``,
   ``rtx6000ada``) and datacenter cards (``a100``, ``h100-sxm``,
   ``h200-sxm``).

   The RTX cards have full graphics engines and run CARLA well. The
   datacenter cards are built for compute, and Unreal's offscreen renderer
   is **not** something they are designed for. A bare ``--gres=gpu:1`` may
   hand you an A100 and a failure that looks like a CARLA bug.

Confirm you landed somewhere with a GPU:

.. code-block:: bash

   hostname
   nvidia-smi

.. note::

   ``show_nodes`` lists which node types are currently free. If
   ``rtxa5000`` is busy, any other RTX name in the list above is fine.

Step 6: Start the Server
~~~~~~~~~~~~~~~~~~~~~~~~

CARLA must run **headless**. There is no display on a compute node, and
``-RenderOffScreen`` skips X entirely and renders straight on the NVIDIA
device.

.. tab-set::

   .. tab-item:: Recipe A -- ICD present
      :sync: recipeA

      .. code-block:: bash

         apptainer exec --nv --cleanenv $CARLA_SIF \
           bash -c "cd /workspace && ./CarlaUE4.sh \
                    -RenderOffScreen -vulkan -nosound \
                    -quality-level=Epic -carla-rpc-port=2000"

   .. tab-item:: Recipe B -- bind the ICD (always safe)
      :sync: recipeB

      .. code-block:: bash

         ICD=/usr/share/vulkan/icd.d/nvidia_icd.json   # path from Step 4

         apptainer exec --nv --cleanenv \
           --bind $ICD:$ICD --env VK_ICD_FILENAMES=$ICD \
           $CARLA_SIF \
           bash -c "cd /workspace && ./CarlaUE4.sh \
                    -RenderOffScreen -vulkan -nosound \
                    -quality-level=Epic -carla-rpc-port=2000"

.. important::

   ``--cleanenv`` is not cosmetic. Without it Apptainer passes your shell's
   environment into the container, including ``DISPLAY``. Unreal then tries
   to use a display that is not there, takes the software-rendering path, and
   **segfaults while loading a map** -- see :ref:`umiacs-renderer-crash`.

   Docker isolates the environment by default; Apptainer does not. This flag
   restores that behaviour.

**Nothing appears on screen, and nothing is wrong.** The server prints startup
text and then sits there. Give it 30--60 seconds.

.. note::

   You will see this line even on a completely successful start:

   .. code-block:: text

      chmod: changing permissions of
      '/workspace/CarlaUE4/Binaries/Linux/CarlaUE4-Linux-Shipping':
      Read-only file system

   ``CarlaUE4.sh`` tries to mark a binary executable that already is. A SIF is
   read-only, so the attempt fails harmlessly. **Ignore it.**

Running the Server in the Background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The command above occupies your terminal. To keep working in the same job,
send it to the background and log it:

.. code-block:: bash

   apptainer exec --nv --cleanenv $CARLA_SIF \
     bash -c "cd /workspace && ./CarlaUE4.sh -RenderOffScreen -vulkan -nosound \
              -quality-level=Epic -carla-rpc-port=2000" \
     > $HOME/carla_server.log 2>&1 &

Wait until it genuinely answers, rather than guessing:

.. code-block:: bash

   until ss -ltn | grep -q ':2000 '; do sleep 2; done; echo "port open"

.. important::

   **The port opens before the map has loaded.** A client that connects the
   instant it sees port 2000 can appear to hang. Wait for a call that needs
   the level to be up:

   .. code-block:: bash

      python3 -c "
      import carla
      c = carla.Client('localhost', 2000); c.set_timeout(60.0)
      print('ready:', c.get_world().get_map().name)"

Stopping the Server
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pkill -f CarlaUE4-Linux-Shipping

Exiting your ``srun`` shell stops it too, along with everything else in the
job.

.. _umiacs-ports:

Sharing a Node: Change Your Port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several students may land on the same compute node. CARLA defaults to port
**2000**, and the second person to start gets a failure that does not say
"port in use".

.. code-block:: bash

   # pick a port from your job id, so it is yours and reproducible
   export CARLA_PORT=$(( 2000 + (SLURM_JOB_ID % 400) * 10 ))
   echo "using port $CARLA_PORT"

Pass ``-carla-rpc-port=$CARLA_PORT`` when starting the server, and use the
same number in every client.

.. warning::

   CARLA uses **three consecutive ports**: the RPC port you choose, plus the
   next two. Space your choices at least 10 apart, as above.

.. _umiacs-python-client:

---------------------------------------------------------
Part 4: The Python Client
---------------------------------------------------------

The client is an ordinary Python program. On Nexus it runs **on the same
compute node** as the server, inside the same job.

.. danger::

   **Run your Python clients inside the ROS 2 container, not on the Nexus
   host.**

   The CARLA 0.9.16 client is published only as wheels for **Python 3.10,
   3.11 and 3.12**:

   .. code-block:: text

      carla-0.9.16-cp310-cp310-manylinux_2_31_x86_64.whl
      carla-0.9.16-cp311-cp311-manylinux_2_31_x86_64.whl
      carla-0.9.16-cp312-cp312-manylinux_2_31_x86_64.whl

   Nexus compute nodes run RHEL 8, whose system Python is **3.6**. There is
   no wheel for it, so ``pip3 install carla`` on the host fails or installs
   nothing usable.

.. important::

   **The CARLA container cannot run the client either.** Its own Python is
   3.8, and it ships only the cp310/cp311/cp312 wheels above, so
   ``import carla`` inside it fails with ``ModuleNotFoundError``. The image
   is a *server*; treat it as one.

   The ROS 2 Jazzy container has **Python 3.12**, so it is the right home for
   every client you write -- whether or not that client uses ROS.

Install the Client Library
~~~~~~~~~~~~~~~~~~~~~~~~~~

Set up the ROS 2 container first (:ref:`umiacs-ros-image`), then install the
client into your home directory from inside it:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc \
     'pip3 install --user --break-system-packages carla==0.9.16 numpy'

.. note::

   Both flags are load-bearing.

   - ``--user`` installs into ``~/.local``, which is your home directory and
     is visible from every compute node. The container itself is read-only.
   - ``--break-system-packages`` is required because the container is built
     on Ubuntu 24.04, which marks its system Python as externally managed
     (:pep:`668`). The flag is safe here: you are writing to your own home,
     not to the container.

Verify it:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc \
     'python3 -c "import carla; print(\"carla client OK\")"'

.. warning::

   **Do not test with** ``carla.__version__``. The 0.9.16 wheel does not
   define it, and the attempt raises ``AttributeError`` even on a perfectly
   good install. If you want the version, ask a running server:

   .. code-block:: python

      client.get_client_version()
      client.get_server_version()

Get the Course Scripts
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd ~
   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git

The scripts are described in :doc:`Using CARLA from Python <carla-python>`.
They are identical here; only the way the server was started differs.

Run One
~~~~~~~

With the server running in the background of your job, run the client through
the ROS container:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc '
     cd ~/enpm818z-fall-2026-carla-python/lecture2
     python3 demo1_connect.py --town Town03
   '

.. tip::

   That wrapper gets long. Put it in ``~/bin/carla-py`` once:

   .. code-block:: bash

      #!/bin/bash
      # carla-py <script.py> [args...]  -- run a CARLA client in the ROS container
      exec apptainer exec --cleanenv "$ROS_SIF" bash -lc \
           "cd \"$PWD\" && python3 $*"

   Then ``chmod +x ~/bin/carla-py`` and simply run
   ``carla-py demo1_connect.py --town Town03``.

.. danger::

   **Do not run** ``spectator_view.py`` **on Nexus.** It opens a Pygame
   window, and there is no display. It will fail, and on some nodes it fails
   slowly.

   Everything visual on a cluster works the same way: **write a file, then
   copy it back.** See :ref:`umiacs-getting-results`.

Adapting a Script to a Non-Default Port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Course scripts assume port 2000. If you changed it (:ref:`umiacs-ports`),
pass the port through:

.. code-block:: python

   import os, carla
   port = int(os.environ.get("CARLA_PORT", 2000))
   client = carla.Client("localhost", port)
   client.set_timeout(60.0)

.. _umiacs-getting-results:

Getting Results Off the Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save images, plots and bags to disk, then from **your laptop**:

.. code-block:: bash

   scp <user>@nexus<abbreviation>00.umiacs.umd.edu:~/results/overlay.png .

.. tip::

   For the L2 LiDAR-to-camera exercise this is the natural workflow anyway:
   the deliverable is three saved overlay images and their point counts, not
   a live window.

---------------------------------------------------------
Part 5: ROS 2
---------------------------------------------------------

.. important::

   **Nexus has no ROS 2**, and you cannot install it -- that would need root.
   The course bridge therefore runs in a **second container**, alongside the
   CARLA one.

   This is the one place where the Nexus workflow is genuinely more involved
   than the laptop workflow.

Why Two Containers Work Together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apptainer does **not** isolate the network by default. Both containers share
the compute node's network stack, so the bridge reaches the CARLA server at
``localhost:2000`` exactly as it would on your laptop.

.. code-block:: text

   compute node
   ├── container 1: CARLA server      listening on localhost:2000
   └── container 2: ROS 2 + bridge    connects to localhost:2000
                                      publishes /carla/... topics

.. _umiacs-ros-image:

Step 1: Confirm You Have the ROS 2 Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You acquired it in :ref:`umiacs-shared-sif`. Check the variable is set:

.. code-block:: bash

   echo "$ROS_SIF"
   apptainer exec --cleanenv $ROS_SIF bash -lc \
     'source /opt/ros/jazzy/setup.bash && echo "ROS_DISTRO=$ROS_DISTRO"'

It should print ``ROS_DISTRO=jazzy``.

Step 2: Build the Bridge Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The container is read-only, but your **home directory is not** -- Apptainer
binds it in automatically. So the workspace lives in your home and builds
normally.

On the submission node:

.. code-block:: bash

   mkdir -p ~/enpm818z_ws/src
   cd ~/enpm818z_ws/src
   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-ros.git

Then build **inside** the ROS container:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc '
     source /opt/ros/jazzy/setup.bash
     pip3 install --user --break-system-packages carla==0.9.16 numpy
     cd ~/enpm818z_ws
     colcon build --symlink-install
   '

.. note::

   ``bash -lc`` and the explicit ``source`` matter. ``--cleanenv`` gives you a
   clean environment, so nothing is sourced for you. Every ROS command in a
   container needs its own ``source /opt/ros/jazzy/setup.bash``.

Step 3: Run the Bridge
~~~~~~~~~~~~~~~~~~~~~~

With CARLA already running in the background of your job:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc '
     source /opt/ros/jazzy/setup.bash
     source ~/enpm818z_ws/install/setup.bash
     export ROS_DOMAIN_ID=42
     ros2 launch l2_carla_demo demo.launch.py
   '

In another shell **on the same compute node**:

.. code-block:: bash

   apptainer exec --cleanenv $ROS_SIF bash -lc '
     source /opt/ros/jazzy/setup.bash
     source ~/enpm818z_ws/install/setup.bash
     export ROS_DOMAIN_ID=42
     ros2 topic list
     ros2 topic hz /carla/ego_vehicle/rgb_front/image
   '

.. warning::

   **Set** ``ROS_DOMAIN_ID`` **and make it yours.** Nexus compute nodes are
   shared. Two students using the default domain on one node will discover
   each other's topics and be very confused. Pick a number and use it
   consistently -- your SLURM job id modulo 200 works well.

.. danger::

   **RViz2 will not work on Nexus.** It needs a display, and there is not
   one. Record instead, and inspect the bag on your own machine:

   .. code-block:: bash

      ros2 bag record -o ~/results/run1 /carla/ego_vehicle/rgb_front/image

   Then ``scp`` the bag back and open it locally, where you do have RViz2.

.. seealso::

   The bridge itself, its topics and its parameters are documented on the
   :doc:`ROS 2 Bridge <carla-ros2>` page. Everything there applies unchanged;
   only the ``apptainer exec ... source ...`` wrapper is new.

---------------------------------------------------------
Part 6: Batch Jobs
---------------------------------------------------------

Interactive jobs are for development. For anything long -- collecting a
dataset, sweeping weather presets -- submit a batch job and let it run
without you.

Save as ``~/carla_job.sh``:

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=carla
   #SBATCH --gres=gpu:rtxa5000:1
   #SBATCH --cpus-per-task=4
   #SBATCH --mem=16gb
   #SBATCH --time=02:00:00
   #SBATCH --output=%x-%j.out

   set -euo pipefail

   CARLA_SIF=/fs/nexus-containers/enpm818z/carla_0.9.16.sif
   ROS_SIF=/fs/nexus-containers/enpm818z/ros_jazzy.sif
   PORT=$(( 2000 + (SLURM_JOB_ID % 400) * 10 ))
   echo "node=$(hostname) port=$PORT"

   # start the server
   apptainer exec --nv --cleanenv "$CARLA_SIF" \
     bash -c "cd /workspace && ./CarlaUE4.sh -RenderOffScreen -vulkan -nosound \
              -quality-level=Epic -carla-rpc-port=$PORT" &
   SERVER=$!

   # wait for the level to load, not merely for the port to open
   for i in $(seq 1 60); do
       apptainer exec --cleanenv "$ROS_SIF" python3 -c "
   import carla
   c = carla.Client('localhost', $PORT); c.set_timeout(5.0)
   c.get_world().get_map()" 2>/dev/null && break
       sleep 5
   done

   # do the work -- clients run in the ROS container (Python 3.12)
   apptainer exec --cleanenv "$ROS_SIF" bash -lc "
     cd ~/enpm818z-fall-2026-carla-python/lecture2
     CARLA_PORT=$PORT python3 demo4_weather.py --contact-sheet ~/results/weather.png
   "

   kill $SERVER

Submit and watch it:

.. code-block:: bash

   mkdir -p ~/results
   sbatch ~/carla_job.sh
   squeue --me
   tail -f carla-<jobid>.out

.. tip::

   ``set -euo pipefail`` makes the job **fail loudly**. Without it, a broken
   step is skipped silently and the job reports success having produced
   nothing.

---------------------------------------------------------
Troubleshooting
---------------------------------------------------------

.. _umiacs-renderer-crash:

The Client Times Out and the Server Has Died
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom.** The client connects, ``get_available_maps()`` works, and then
``load_world()`` fails:

.. code-block:: text

   RuntimeError: time-out of 120000ms while waiting for the simulator,
   make sure the simulator is ready and connected to localhost:2000

**Look at the server log, not the client error.** The client is wrong about
what happened:

.. code-block:: text

   WARNING: lavapipe is not a conformant vulkan implementation, testing use only.
   LowLevelFatalError [File:Unknown] [Line: 1214]
   GameThread timed out waiting for RenderThread after 60.00 secs
   Signal 11 caught.
   CommonUnixCrashHandler: Signal=11
   Segmentation fault (core dumped)

**Cause.** Vulkan never reached the NVIDIA GPU, so Unreal fell back to
``lavapipe``, the software rasterizer, which cannot sustain the render thread.
The server **segfaulted during the map load**; it did not run slowly.

**Fixes, in order of likelihood:**

1. You are missing the NVIDIA ICD. Use **Recipe B** (:ref:`umiacs-icd-check`).
2. You omitted ``--cleanenv``, so ``DISPLAY`` leaked in.
3. You omitted ``--nv``. Without it the container cannot see the GPU at all.
4. You were given a datacenter GPU. Check ``nvidia-smi``; re-request with an
   RTX name.

.. important::

   The word ``lavapipe`` or ``llvmpipe`` anywhere in the log means software
   rendering, which always means one of the four causes above.

``CUDA_ERROR_NO_DEVICE`` or ``nvidia-smi`` Fails in the Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You forgot ``--nv``, or you are not in a GPU allocation. Check both:

.. code-block:: bash

   echo "$SLURM_JOB_ID"      # empty means you are on the submission node
   nvidia-smi                 # must list a GPU on the host first

Port Already in Use
~~~~~~~~~~~~~~~~~~~

Another student on your node is using it. Change yours
(:ref:`umiacs-ports`). To see what is taken:

.. code-block:: bash

   ss -ltn | grep -E ':(20[0-9][0-9]) '

Disk Quota Exceeded
~~~~~~~~~~~~~~~~~~~

Almost always Apptainer's cache in your home directory. Confirm Step 2 is in
effect and clear the cache:

.. code-block:: bash

   echo "$APPTAINER_CACHEDIR"     # must not be under your home
   apptainer cache clean --force
   du -sh ~/.apptainer 2>/dev/null

ROS 2 Topics Do Not Appear
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - **Check**
     - **Why**
   * - Same ``ROS_DOMAIN_ID`` in both shells?
     - Different domains cannot see each other.
   * - Same compute node?
     - Two SLURM jobs are two different machines.
   * - Did you source both setup files?
     - ``--cleanenv`` means nothing is sourced automatically.
   * - Is CARLA actually up?
     - The bridge starts happily and publishes nothing.

My Job Disappeared
~~~~~~~~~~~~~~~~~~

It hit its time limit. Check with:

.. code-block:: bash

   sacct -j <jobid> --format=JobID,State,Elapsed,ExitCode

``TIMEOUT`` means exactly that. Request more time, or split the work.

---------------------------------------------------------
Comparison With the Laptop Setups
---------------------------------------------------------

.. list-table::
   :widths: 24 25 25 26
   :header-rows: 1
   :class: compact-table

   * - **Aspect**
     - **Ubuntu 22.04**
     - **Ubuntu 24.04**
     - **UMIACS Nexus**
   * - Method
     - Native
     - Docker
     - Apptainer
   * - Root needed
     - For install
     - For install
     - **Never**
   * - GPU access
     - Direct
     - NVIDIA Container Toolkit
     - ``--nv``
   * - Server start
     - ``./CarlaUE4.sh``
     - ``carla_basic``
     - ``srun`` then ``apptainer exec``
   * - Persists between sessions
     - Yes
     - Yes, in the container
     - **No** -- the job ends
   * - Display
     - Window
     - Headless
     - Headless, and no RViz2 either
   * - ROS 2
     - On the host
     - On the host
     - **Second container**
   * - Extra maps
     - Extract in place
     - ``docker cp``
     - Bind-mount from home

.. note::

   **The assignments do not change.** Every deliverable in ENPM818Z can be
   produced on any of the three. Nexus buys you a large GPU at the cost of a
   scheduler and no screen.

---------------------------------------------------------
Optional: Additional Maps
---------------------------------------------------------

Town06, Town07 and Town11--Town15 are not in the image. Unlike the Docker
setup, you do **not** copy them into the container -- you extract them in
your own storage and bind them in.

.. code-block:: bash

   cd /fs/nexus-scratch/$USER
   wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.16.tar.gz
   mkdir -p extra && tar -xzf AdditionalMaps_0.9.16.tar.gz -C extra

Then add a bind to every launch:

.. code-block:: bash

   apptainer exec --nv --cleanenv \
     --bind /fs/nexus-scratch/$USER/extra/CarlaUE4/Content:/workspace/CarlaUE4/Content \
     $CARLA_SIF \
     bash -c "cd /workspace && ./CarlaUE4.sh -RenderOffScreen -vulkan -nosound"

.. tip::

   This is **better** than the Docker approach. There, the maps live in a
   container layer that ``docker rm`` silently destroys. Here they are
   ordinary files in your own storage, and the image stays untouched.

.. warning::

   The archive is **14.8 GB**. Skip this unless an assignment names one of
   those towns.

---------------------------------------------------------
Next Steps
---------------------------------------------------------

- :doc:`Using CARLA from Python <carla-python>` -- the API and the course
  demo scripts.
- :doc:`CARLA ROS 2 Bridge <carla-ros2>` -- the bridge package and its
  topics.

---------------------------------------------------------
References
---------------------------------------------------------

- `UMIACS Nexus <https://wiki.umiacs.umd.edu/umiacs/index.php/Nexus>`_
- `UMIACS Apptainer <https://wiki.umiacs.umd.edu/umiacs/index.php/Apptainer>`_
- `UMIACS Nexus GPUs <https://wiki.umiacs.umd.edu/umiacs/index.php/Nexus/GPUs>`_
- `UMIACS SLURM <https://wiki.umiacs.umd.edu/umiacs/index.php/SLURM>`_
- `UMIACS Class Accounts <https://wiki.umiacs.umd.edu/umiacs/index.php/ClassAccounts>`_
- `Apptainer documentation <https://apptainer.org/docs/user/main/>`_
- `CARLA 0.9.16 documentation <https://carla.readthedocs.io/en/0.9.16/>`_
