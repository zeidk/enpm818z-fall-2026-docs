==================================================================
CARLA Setup Guide - Ubuntu 24.04 (Docker)
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
     - 24.04 (Noble Numbat)
   * - CARLA Version
     - 0.9.16
   * - Installation Method
     - Docker


---------------------------------------------------------
Overview
---------------------------------------------------------


This guide gets a CARLA 0.9.16 server running on Ubuntu 24.04 using Docker. When
you finish it you will have a working server and a Python client that can talk
to it. **It does not cover ROS 2**; that is a separate page.

The CARLA documentation for this course is split into three parts. Read them in
order:

.. list-table::
   :widths: 34 66
   :header-rows: 1
   :class: table-hover

   * - **Page**
     - **What it covers**
   * - **This page** -- Setup
     - Docker, the NVIDIA Container Toolkit, the CARLA image, maps, and starting
       and stopping the server.
   * - :doc:`Using CARLA from Python <carla-python>`
     - Talking to the server from a plain Python script, and watching the
       simulation in a viewer window.
   * - :doc:`ROS 2 Bridge <carla-ros2>`
     - The custom ROS 2 bridge package: building it, running it, and the topics
       it publishes.

**What you will install on this page:**

- Docker Engine and the NVIDIA Container Toolkit
- The CARLA 0.9.16 Docker image
- The CARLA Python client (via pip)

.. note::
   **Why Docker?** CARLA 0.9.16 does not have native support for Ubuntu 24.04.
   Running CARLA inside a Docker container is the supported workaround -- the
   containerized CARLA server interfaces directly with the Python and ROS 2
   environment running on the host system.

---------------------------------------------------------
Terminology
---------------------------------------------------------

.. admonition:: Key Terms

   **Host**
      The physical or virtual machine (your Ubuntu 24.04 system) on which Docker is installed. The host runs the Docker engine and provides the underlying hardware resources -- CPU, GPU, memory, and network -- to containers. In this guide, ROS 2 and the CARLA Python client run directly on the host.

   **Container**
      A lightweight, isolated runtime environment created from a Docker image. A container packages an application and all its dependencies so it runs consistently regardless of the host OS. In this guide, the CARLA server runs inside a container while communicating with the host over the network.

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
     - Ubuntu 24.04 (Noble Numbat)
   * - ROS 2 Distribution
     - Already installed
   * - GPU
     - NVIDIA GPU with the proprietary driver (**required** -- the container renders on the NVIDIA device)
   * - RAM
     - Minimum 8 GB, Recommended 16 GB
   * - Disk Space
     - ~40 GB free (the CARLA image alone unpacks to ~29 GB)
   * - Python
     - 3.12 (comes with Ubuntu 24.04)

Verify Your Ubuntu Version
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsb_release -a

You should see ``Ubuntu 24.04`` in the output.

---------------------------------------------------------
Step 0: Install Docker and the NVIDIA Container Toolkit
---------------------------------------------------------

CARLA runs inside a container that renders on your NVIDIA GPU. That requires two
pieces of host software: **Docker Engine**, and the **NVIDIA Container Toolkit**
that lets a container reach the GPU. A stock Ubuntu 24.04 install has neither.

.. important::
   Skipping this step is the most common way to get stuck. Without the toolkit,
   every ``--gpus all`` command fails with:

   .. code-block:: text

      docker: Error response from daemon: failed to discover GPU vendor from CDI:
      no known GPU vendor found

   Having the NVIDIA *driver* installed is not sufficient. ``nvidia-smi`` can
   work perfectly on the host while Docker still has no way to pass the GPU
   through to a container.

Install Docker Engine
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y docker.io
   sudo systemctl enable --now docker

Add yourself to the ``docker`` group so you do not need ``sudo`` for every
command, then **log out and back in** for the new group to take effect:

.. code-block:: bash

   sudo usermod -aG docker $USER

Verify the NVIDIA Driver
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   nvidia-smi

You should see your GPU, the driver version, and the CUDA version. If the
command is not found, install the proprietary driver first with
``sudo ubuntu-drivers install`` and reboot.

Install the NVIDIA Container Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add NVIDIA's package repository, install the toolkit, register it as a Docker
runtime, and restart the Docker daemon:

.. code-block:: bash

   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
     | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
     | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
     | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker

.. note::
   ``sudo systemctl restart docker`` does not delete your containers or images.

Verify GPU Passthrough
~~~~~~~~~~~~~~~~~~~~~~

Docker should now list ``nvidia`` among its runtimes:

.. code-block:: bash

   docker info | grep -i runtimes

.. code-block:: text

    Runtimes: io.containerd.runc.v2 nvidia runc

Do not continue until ``nvidia`` appears in that list.

---------------------------------------------------------
Step 1: Pull CARLA Docker Image
---------------------------------------------------------

Download the CARLA 0.9.16 Docker image:

.. code-block:: bash

   # Pull CARLA image (this may take 10-15 minutes)
   docker pull carlasim/carla:0.9.16

   # Verify image is downloaded
   docker images | grep carla

Expected output:

.. code-block:: text

   REPOSITORY              TAG       IMAGE ID       CREATED         SIZE
   carlasim/carla          0.9.16    aaf1df227027   11 months ago   29.4GB

The ``IMAGE ID`` will differ if CARLA republishes the tag; the ``SIZE`` should be
close to 29 GB. A much smaller size means the pull was interrupted -- rerun it.

Confirm the container can actually reach the GPU:

.. code-block:: bash

   docker run --rm --gpus all carlasim/carla:0.9.16 nvidia-smi

This must print your GPU. If it instead reports ``failed to discover GPU vendor
from CDI``, the NVIDIA Container Toolkit from Step 0 is not installed or the
Docker daemon was not restarted.

---------------------------------------------------------
Step 2: Install Additional Dependencies
---------------------------------------------------------

.. code-block:: bash

   # Install required Python packages
   pip3 install numpy pygame

   # Install CARLA Python client
   pip3 install carla==0.9.16

   # Verify installations
   python3 -c "import numpy; import pygame; import carla; print('All dependencies OK')"

**Command breakdown:**

- ``pip3 install numpy pygame`` — Installs two Python packages using pip:

  - **NumPy** — A numerical computing library used for array operations, linear algebra, and mathematical transformations. CARLA scripts use NumPy to process sensor data (e.g., converting raw camera/lidar buffers into arrays) and to perform coordinate transformations.
  - **Pygame** — A multimedia library for creating graphical windows and handling keyboard/mouse input. CARLA's example scripts use Pygame to render the simulation camera feed in a display window and to capture user input for manual vehicle control.

- ``pip3 install carla==0.9.16`` — Installs the CARLA Python client library, pinned to version **0.9.16** to match the Docker server image pulled in Step 1. This library provides the Python API (``carla.Client``, ``carla.World``, ``carla.Vehicle``, etc.) that your scripts use to connect to the CARLA server, spawn actors, attach sensors, and control the simulation.

- ``python3 -c "import numpy; import pygame; import carla; print('All dependencies OK')"`` — Runs a one-line Python script that attempts to import all three packages. If any package is missing or improperly installed, Python will raise an ``ImportError`` and you will know which dependency needs to be reinstalled. If all imports succeed, it prints ``All dependencies OK``.

---------------------------------------------------------
Step 3: Maps and the Server
---------------------------------------------------------

Highway assignments (for example, behavioral planning) use **Town04**, which has
a dedicated multi-lane highway loop. **Town04 already ships inside the**
``carlasim/carla:0.9.16`` **image. You do not need to download anything.**

The image contains these maps:

.. code-block:: text

   Town01   Town01_Opt   Town02     Town02_Opt
   Town03   Town03_Opt   Town04     Town04_Opt
   Town05   Town05_Opt   Town10HD   Town10HD_Opt

The ``_Opt`` variants are *layered* maps whose scenery (parked cars, foliage, street props) can be toggled at runtime.

.. warning::
   Do **not** download ``AdditionalMaps_0.9.16.tar.gz`` to obtain Town04. That
   archive is a **14.8 GB download** that expands to roughly the same again
   inside the container, and it does not contain Town04 -- you already have it.
   Only follow :ref:`additional-maps-optional` if an assignment specifically
   names Town06, Town07, or Town11--Town15.

Start the Server
~~~~~~~~~~~~~~~~

Start CARLA **headless**. The server renders directly on the NVIDIA GPU and
needs no X display.

.. important::
   ``docker run`` **creates** a container and works only once. Every time after
   that it fails with ``Conflict. The container name "/carla-server" is already
   in use``. Once the container exists, you start it with ``docker start``.

   Use this command every time and you never have to remember which case you are
   in -- it starts the existing container, or creates one if there is none:

   .. code-block:: bash

      docker start carla-server 2>/dev/null || \
      docker run -d --name carla-server \
        --privileged \
        --gpus all \
        --net=host \
        carlasim/carla:0.9.16 \
        /bin/bash CarlaUE4.sh -RenderOffScreen -nosound

The two halves separately, if you prefer to know which one you are running.
**First time only**, to create the container:

.. code-block:: bash

   docker run -d --name carla-server \
     --privileged \
     --gpus all \
     --net=host \
     carlasim/carla:0.9.16 \
     /bin/bash CarlaUE4.sh -RenderOffScreen -nosound

**Every subsequent session**, to start the container you already have:

.. code-block:: bash

   docker start carla-server

.. important::
   Passing ``-e DISPLAY=$DISPLAY`` and mounting ``/tmp/.X11-unix`` is **not**
   the right way to start this container, even though it looks like the obvious
   one. It fails in two distinct ways on a typical laptop:

   - If your session is on ``:1`` rather than ``:0``, or on Wayland, the
     container gets a display that does not exist and exits immediately with
     status 1, logging nothing past ``Disabling core dumps.``
   - Even with the right display number, X rejects the container unless your
     host UID happens to be 1000 (the container's ``carla`` user). The log then
     reads ``Authorization required, but no authorization protocol specified``.

   ``-RenderOffScreen`` avoids both. See :ref:`why-headless` for why a windowed
   server also segfaults partway through loading a map.

Give the server 30--60 seconds to initialize. Confirm it is up:

.. code-block:: bash

   docker ps --filter "name=carla-server"

The ``STATUS`` column must read ``Up``. If the container is missing, it exited
-- run ``docker ps -a`` for the exit code and ``docker logs carla-server`` for
the reason.

If the container is missing from ``docker ps`` but **is** listed by
``docker ps -a``, it exited rather than never starting. Two common exit codes:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - **Exit code**
     - **Meaning**
   * - ``Exited (1)``
     - CARLA failed at startup. Almost always a display problem -- see the
       ``important`` box above. Check ``docker logs carla-server``.
   * - ``Exited (137)``
     - The process was killed (SIGKILL). **This is normal after a clean
       stop**: CARLA does not handle ``SIGTERM``, so ``docker stop`` waits its
       grace period and then kills it. You also get 137 if you attached with
       ``docker start -ai`` and interrupted it. Either way, just start it
       again.

.. warning::
   Do not start the server with ``docker start -ai``. That attaches your
   terminal to the server process, so closing the terminal or pressing Ctrl-C
   kills CARLA. Start it detached and read its output separately:

   .. code-block:: bash

      docker logs -f carla-server    # Ctrl-C stops following, not the server

Confirm the Maps
~~~~~~~~~~~~~~~~

In a second terminal, ask the server what it has:

.. code-block:: bash

   python3 -c "
   import carla
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   for m in sorted(client.get_available_maps()):
       print('  -', m.split('/')[-1])
   "

Expected output:

.. code-block:: text

     - Town01
     - Town01_Opt
     - Town02
     - Town02_Opt
     - Town03
     - Town03_Opt
     - Town04
     - Town04_Opt
     - Town05
     - Town05_Opt
     - Town10HD
     - Town10HD_Opt


.. seealso::
   To **load** a specific map from a script, see
   :doc:`Using CARLA from Python <carla-python>`.


.. _additional-maps-optional:

Optional: Additional Maps (Town06, Town07, Town11--Town15)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
   **This costs about 30 GB of disk.** The archive is 14.8 GB on the host and
   expands to roughly the same again inside the container's writable layer,
   which the container then carries permanently. Skip this section unless you
   actually need one of these maps.

**Terminal 1 (host)** -- download the archive:

.. code-block:: bash

   cd ~/Downloads
   wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.16.tar.gz

**Terminal 1 (host)** -- copy it into the container. The container does *not*
need to be running; ``docker cp`` works on a stopped container too:

.. code-block:: bash

   docker cp ~/Downloads/AdditionalMaps_0.9.16.tar.gz carla-server:/workspace/

**Terminal 1 (host)** -- start the container and open a root shell inside it:

.. code-block:: bash

   docker start carla-server
   docker exec -it --user root carla-server bash

**Inside the container** -- extract the archive at ``/workspace``:

.. code-block:: bash

   cd /workspace
   tar -xzf AdditionalMaps_0.9.16.tar.gz
   rm AdditionalMaps_0.9.16.tar.gz
   exit

.. note::
   **Do not run** ``./ImportAssets.sh``. That script cooks raw assets dropped
   into ``/workspace/Import/``, and this archive is not packaged that way -- its
   top-level directory is ``CarlaUE4/Content/``, so ``tar`` already places the
   maps exactly where the server reads them. ``Import/`` is empty both before
   and after, so ``ImportAssets.sh`` would simply do nothing.

**Terminal 1 (host)** -- restart the server so it rescans its content:

.. code-block:: bash

   docker restart carla-server

.. danger::
   **Never** ``docker rm carla-server`` after importing maps. The imported maps
   live only in that container's writable layer -- they are not part of the
   image. Removing the container and running ``docker run`` again gives you a
   fresh container from the base image and silently discards the whole ~15 GB
   import, with no error to tell you it happened. Use ``docker start`` or
   ``docker restart`` to bring an existing container back.

Query the server again to confirm the import worked:

.. code-block:: bash

   python3 -c "
   import carla
   client = carla.Client('localhost', 2000)
   client.set_timeout(10.0)
   for m in sorted(client.get_available_maps()):
       print('  -', m.split('/')[-1])
   "

The list should now also include ``Town06``, ``Town07``, ``Town11``, ``Town12``,
``Town13`` and ``Town15``, alongside the maps that shipped with the image. If it
looks unchanged, the server was not restarted after the extraction -- run
``docker restart carla-server`` and query again.

Stop the Server
~~~~~~~~~~~~~~~

Steps 3 and 4 do not need CARLA running, so shut it down before moving on:

.. code-block:: bash

   docker stop carla-server

Confirm it stopped:

.. code-block:: bash

   docker ps --filter "name=carla-server"

The listing should now be empty. That is expected -- ``docker ps`` shows only
*running* containers. Your container still exists; ``docker ps -a`` will show it
in the ``Exited`` state, ready to start again.

.. important::
   ``docker stop`` is not ``docker rm``.

   - ``docker stop carla-server`` halts the server and **keeps** the container,
     including any maps you imported into it. This is what you want between
     work sessions.
   - ``docker rm carla-server`` **deletes** the container and everything in its
     writable layer. Only do this when you are finished with CARLA -- see
     :ref:`removing-carla`.

Restart it whenever you need it again:

.. code-block:: bash

   docker start carla-server

---------------------------------------------------------
Step 4: Shell Helpers for the Server
---------------------------------------------------------


Typing the full ``docker`` commands every session gets old quickly. These shell
functions wrap them. They deal **only** with the server, and need no ROS 2 --
the ROS 2 environment is configured separately, on the
:doc:`ROS 2 Bridge <carla-ros2>` page.

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: table-hover

   * - **Command**
     - **What it does**
   * - ``carla_basic [quality]``
     - Starts the server and blocks until it actually accepts connections.
       Reuses the existing container, so imported maps survive. Quality applies
       only when the container is first created; defaults to ``Epic``, pass
       ``Low`` on a weaker GPU.
   * - ``carla_basic -f [quality]``
     - Recreates the container from scratch first. Use this to change the
       quality level. **Discards imported additional maps.**
   * - ``carla_log``
     - Follows the server's output. This is where a crash explains itself.
   * - ``carla_stop`` / ``carla_kill``
     - Stops the server, keeping the container and anything imported into it.
   * - ``carla_rm``
     - Deletes the container. See :ref:`removing-carla`.

.. note::
   These instructions assume **bash**. If your terminal runs **zsh** (check with
   ``echo $SHELL``), use ``~/.zshrc`` everywhere ``~/.bashrc`` appears below,
   and reload with ``source ~/.zshrc``. The functions work unchanged in both
   shells. Editing the wrong file is a quiet failure: nothing errors, the
   ``carla_*`` commands simply never appear.

Open your ``~/.bashrc`` in an editor:

.. code-block:: bash

   nano ~/.bashrc

Add the following at the **end** of that file:

.. code-block:: bash

   # ---------------------------------------------------------------------------
   # CARLA server helpers (ENPM818Z) -- no ROS 2 required
   #
   #   carla_basic [quality]     start the server, wait until it is ready
   #   carla_basic -f [quality]  recreate the container first
   #   carla_log                 follow the server's output
   #   carla_stop / carla_kill   stop the server, keep the container
   #   carla_rm                  delete the container
   # ---------------------------------------------------------------------------
   carla_basic() {
       # -f recreates the container, which is the only way to change the
       # quality level. It also discards any additional maps imported into it.
       if [ "$1" = "-f" ]; then
           docker rm -f carla-server >/dev/null 2>&1
           shift
       fi

       if [ -n "$(docker ps -aq -f name='^carla-server$')" ]; then
           # Reuse the existing container so imported maps survive.
           docker start carla-server >/dev/null || return 1
       else
           docker run -d --name carla-server \
               --runtime=nvidia \
               --gpus all \
               --net=host \
               -v /dev/shm:/dev/shm \
               -e NVIDIA_VISIBLE_DEVICES=all \
               -e NVIDIA_DRIVER_CAPABILITIES=all \
               carlasim/carla:0.9.16 \
               /bin/bash -c "./CarlaUE4.sh -RenderOffScreen -vulkan -nosound -quality-level=${1:-Epic}" >/dev/null || return 1
       fi

       # The container can die during startup. Say so, and show why,
       # instead of waiting for a port that will never open.
       printf 'starting CARLA'
       while ! ss -ltn 2>/dev/null | grep -q ':2000 '; do
           if [ -z "$(docker ps -q -f name=carla-server)" ]; then
               printf '\nthe server died before it accepted connections. Its output:\n'
               docker logs carla-server 2>&1 | tail -20
               return 1
           fi
           printf '.'
           sleep 2
       done

       # The RPC port opens before the level has finished loading, so a
       # client that connects the moment it sees the port can sit there
       # waiting. Wait for a call that needs the level to be up.
       printf ' level'
       while ! python3 -c "import carla; c=carla.Client('localhost',2000); c.set_timeout(5.0); c.get_world().get_map()" >/dev/null 2>&1; do
           printf '.'
           sleep 2
       done
       printf '\nready on localhost:2000\n'
   }

   carla_stop() {
       if [ -n "$(docker ps -q -f name=carla-server)" ]; then
           docker stop carla-server >/dev/null && echo "CARLA stopped (container kept)"
       else
           echo "CARLA is not running"
       fi
       return 0
   }

   carla_rm() {
       docker rm -f carla-server >/dev/null 2>&1 && echo "carla-server removed" \
           || echo "no carla-server container"
       return 0
   }

   alias carla_kill='carla_stop'
   alias carla_log='docker logs -f carla-server'

Save and reload:

.. code-block:: bash

   source ~/.bashrc

Typical session:

.. code-block:: text

   $ carla_basic
   starting CARLA.. level.
   ready on localhost:2000

   # No window appears. The server is headless -- this is expected.

   $ python3 load_town04.py
   Loading Town04. This can take up to a minute.
   Map:          Carla/Maps/Town04
   Spawn points: 372

   $ carla_stop
   CARLA stopped (container kept)

.. important::
   **Nothing appears on screen when** ``carla_basic`` **finishes, and nothing is
   wrong.** The server runs with ``-RenderOffScreen`` and never opens a window
   of its own -- see :ref:`why-headless`. To watch the simulation, run a viewer
   client; see :ref:`seeing-the-simulation-ubuntu24`.


Why It Waits Twice
~~~~~~~~~~~~~~~~~~

``carla_basic`` prints ``starting CARLA..`` and then ``level.`` because those
are two different conditions:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - **Wait**
     - **What it means**
   * - port 2000 listening
     - The RPC server is up. It is **not** yet able to answer questions about
       the world.
   * - ``get_world().get_map()`` succeeds
     - The level has finished loading. Only now is a client guaranteed a
       prompt answer.

A client that connects on the first condition alone can appear to hang for a
long time with nothing to explain it.

Why the Container Is Not Removed Automatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is no ``--rm`` in the ``docker run`` command, on purpose. When the server
crashes, its output is the only thing that says why, and ``--rm`` deletes the
container and its logs the instant it dies. Instead, ``carla_basic`` removes any
previous container by name before starting a new one, so nothing accumulates,
and ``carla_log`` or ``docker logs carla`` still works after a crash.

``carla_stop`` removes every container built from a CARLA image, not just the
one named ``carla``. A crashed container stays in the list in the exited state
while still holding its name, and containers started by an older alias sit there
under generated names such as ``modest_montalcini``.

.. _why-headless:

Why the Server Runs Headless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The launch command contains ``-RenderOffScreen`` and passes **no** ``DISPLAY``
and **no** X11 socket. That is deliberate, and it is the difference between a
server that works and one that crashes.

.. danger::
   **Symptom.** The client connects, ``get_available_maps()`` succeeds, and
   then ``load_world()`` times out. The container is gone, and
   ``docker ps -a`` shows it **Exited (139)**, which is a segmentation fault.

   **Cause.** ``docker logs`` shows the real reason:

   .. code-block:: text

      MESA: warning: Driver does not support the 0xa788 PCI ID.
      Signal 11 caught.
      CommonUnixCrashHandler: Signal=11

   That PCI ID is an **Intel integrated GPU**. On a laptop with switchable
   graphics, the X server usually runs on the integrated chip, so giving the
   container a ``DISPLAY`` sends Unreal down the Mesa software path instead of
   onto the NVIDIA GPU, and it segfaults partway through loading a map.

   **Fix.** ``-RenderOffScreen`` skips X entirely and renders directly on the
   NVIDIA device. Note that the client-side error, a timeout, points at the
   wrong thing completely: the server did not run slowly, it died.

.. tip::
   Forcing NVIDIA offload (``__NV_PRIME_RENDER_OFFLOAD=1``,
   ``__VK_LAYER_NV_optimus=NVIDIA_only``) does remove the Mesa warning, but the
   windowed server still segfaults on the map load. Headless is not a
   workaround here, it is the configuration that works.

---------------------------------------------------------
Troubleshooting
---------------------------------------------------------


This page covers problems with Docker and the server itself. For client
problems see :doc:`carla-python`; for ROS 2 see :doc:`carla-ros2`.


CARLA Won't Start
~~~~~~~~~~~~~~~~~

**Symptom:** ``docker: Error response from daemon...``

**Solutions:**

1. Verify Docker is running:

   .. code-block:: bash

      sudo systemctl status docker
      sudo systemctl start docker

2. Check GPU access from inside a container:

   .. code-block:: bash

      docker run --rm --gpus all carlasim/carla:0.9.16 nvidia-smi

   If this reports ``failed to discover GPU vendor from CDI: no known GPU vendor
   found``, the NVIDIA Container Toolkit is missing. Go back to Step 0.

3. Confirm Docker registered the ``nvidia`` runtime:

   .. code-block:: bash

      docker info | grep -i runtimes

   ``nvidia`` must appear in the list. If you just installed the toolkit and it
   does not, you likely skipped ``sudo systemctl restart docker``.

XDG_RUNTIME_DIR Errors on Startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** CARLA container starts but prints repeated errors:

.. code-block:: text

   error: XDG_RUNTIME_DIR not set in the environment.

**Explanation:** ``XDG_RUNTIME_DIR`` is a Linux environment variable that points to a per-user
directory (typically ``/run/user/<UID>``) used by display servers and Wayland/X11 compositors to
store runtime sockets. When Docker runs the CARLA process inside the container, this variable is
not set by default, so libraries that look for it (e.g., Vulkan, SDL, PulseAudio) emit these warnings.

**These errors are harmless** — CARLA still runs and renders correctly. The headless
launch command in Step 2.5 does not set ``XDG_RUNTIME_DIR`` at all, and does not need to. If you
want to silence the warning, set it to a writable path inside the container:

.. code-block:: bash

   docker run -d --name carla-server \
     --privileged \
     --gpus all \
     --net=host \
     -e XDG_RUNTIME_DIR=/tmp/runtime-carla \
     carlasim/carla:0.9.16 \
     /bin/bash CarlaUE4.sh -RenderOffScreen -nosound

.. warning::
   Do not "fix" this by adding ``-e DISPLAY=$DISPLAY`` and an X11 socket mount.
   On a Wayland session (the default on Ubuntu 24.04), on a display other than
   ``:0``, or with a host UID other than 1000, that turns a harmless warning into
   a container that exits immediately. See :ref:`why-headless`.

---------------------------------------------------------
Performance Optimization
---------------------------------------------------------

For Better Performance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Reduce camera resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=640 -p image_height:=360

   # Fewer LiDAR beams
   ros2 run l2_carla_demo carla_bridge --ros-args -p lidar_channels:=16

``carla_basic`` takes the graphics quality as an argument, so no editing is
needed: ``carla_basic Low``.

For Better Quality
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Higher resolution
   ros2 run l2_carla_demo carla_bridge \
       --ros-args -p image_width:=1920 -p image_height:=1080

``Epic`` is already the default for ``carla_basic``.

.. _removing-carla:

---------------------------------------------------------
Removing CARLA and Reclaiming Disk Space
---------------------------------------------------------

The CARLA image is about 29 GB, and a container that has actually been run adds
a writable layer of its own -- often another 15--19 GB once Unreal has written
its shader caches and the NVIDIA libraries have been injected into it. Check
what Docker is currently holding:

.. code-block:: bash

   docker system df

.. code-block:: text

   TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
   Images          2         2         29.45GB   0B (0%)
   Containers      2         1         18.93GB   4.096kB (0%)
   Local Volumes   0         0         0B        0B
   Build Cache     0         0         0B        0B

.. important::
   **Order matters.** Docker refuses to delete an image while any container
   still references it, even a stopped one. Remove the container first, then the
   image. The other way round fails with a ``conflict: unable to remove
   repository reference`` error naming the container that still holds it.

Step 1: Remove the Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   docker stop carla-server
   docker rm carla-server

.. danger::
   If you installed the optional additional maps
   (:ref:`additional-maps-optional`), this deletes them. They live in the
   container's writable layer, **not** in the image, so you would have to
   redownload and reimport roughly 30 GB to get them back. Docker gives no
   warning when you do this.

Earlier failed attempts often leave extra containers behind. List every
container built from the CARLA image:

.. code-block:: bash

   docker ps -a --filter ancestor=carlasim/carla:0.9.16

If that lists anything you still want gone, remove them all at once:

.. code-block:: bash

   docker ps -aq --filter ancestor=carlasim/carla:0.9.16 | xargs -r docker rm -f

.. note::
   The ``-r`` matters. Without it, ``xargs`` still runs ``docker rm -f`` when
   the list is empty and you get ``docker: 'docker rm' requires at least 1
   argument``. That message means there was nothing left to remove -- the
   cleanup already succeeded -- but it reads like a failure. The older
   ``docker rm -f $(...)`` form has the same problem and should be avoided.

Step 2: Remove the Image
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   docker rmi carlasim/carla:0.9.16

Confirm it is gone -- this should print nothing:

.. code-block:: bash

   docker images | grep carla

.. note::
   Redownloading the image later takes 10--15 minutes on a fast connection. If
   you are only short of space temporarily, removing the **container** (Step 1)
   frees most of the space while keeping the image, so you can pick up again
   with a single ``docker run``.

Step 3: Optional Host Cleanup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Python client and the maps archive live on the host, outside Docker:

.. code-block:: bash

   pip3 uninstall carla
   rm -f ~/Downloads/AdditionalMaps_0.9.16.tar.gz

.. warning::
   You may see ``docker system prune -a`` suggested online. It removes **every**
   unused image and stopped container on the machine, not just CARLA's. Prefer
   the targeted commands above unless you genuinely want to clear everything.

---------------------------------------------------------
Comparison with Ubuntu 22.04 Setup
---------------------------------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - **Aspect**
     - **Ubuntu 22.04**
     - **Ubuntu 24.04 (This Guide)**
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


With the server running, continue to:

- :doc:`Using CARLA from Python <carla-python>` -- write scripts that connect to
  the server, load maps, and watch the simulation.
- :doc:`CARLA ROS 2 Bridge <carla-ros2>` -- build and run the course's ROS 2
  bridge package.

Both pages cover this platform and the native Ubuntu 22.04 install, with the
differences shown in tabs.


---------------------------------------------------------
References
---------------------------------------------------------


- CARLA Documentation: https://carla.readthedocs.io/en/0.9.16/
- CARLA Downloads: https://github.com/carla-simulator/carla/releases/tag/0.9.16
- Docker Documentation: https://docs.docker.com/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
