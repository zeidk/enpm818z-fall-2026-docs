==================================================================
Using CARLA from Python
==================================================================

This page applies to **both** platforms -- the native Ubuntu 22.04 install and
the Ubuntu 24.04 Docker image. The CARLA Python API is identical either way;
only the commands for starting the server differ, and those are shown in tabs.

.. admonition:: Pick your platform once
   :class: tip

   The tabs on this page are synchronised. Choose **Native (22.04)** or
   **Docker (24.04)** in any tab-set and every other tab-set on the page
   switches with it.


---------------------------------------------------------
Before You Start
---------------------------------------------------------


Finish the setup guide for your platform first:

- :doc:`Ubuntu 22.04 -- native setup <ubuntu22>`
- :doc:`Ubuntu 24.04 -- Docker setup <ubuntu24>`

Then start the server and confirm it is listening.

.. tab-set::

   .. tab-item:: Native (22.04)
      :sync: native

      .. code-block:: bash

         cd ~/carla/CARLA_0.9.16
         ./CarlaUE4.sh -quality-level=Low -nosound -vulkan

      A CARLA window opens. Wait until the city is visible.

   .. tab-item:: Docker (24.04)
      :sync: docker

      .. code-block:: bash

         carla_basic          # or: docker start carla-server

      It prints ``ready on localhost:2000``. **No window appears** -- the
      container runs headless on purpose. See :ref:`why-headless`.

Check the client library is installed:

.. tab-set::

   .. tab-item:: Native (22.04)
      :sync: native

      .. code-block:: bash

         python3 -c "import carla; print(carla.__version__)"

      It comes from the wheel in ``PythonAPI/carla/dist`` (Step 2 of the
      native guide).

   .. tab-item:: Docker (24.04)
      :sync: docker

      .. code-block:: bash

         python3 -c "import carla; print(carla.__version__)"

      It comes from ``pip3 install carla==0.9.16`` on the **host**, not from
      inside the container.

Either way it should print ``0.9.16``.


---------------------------------------------------------
Get the Demo Scripts
---------------------------------------------------------

The lecture demos and the viewer client live in their **own repository**,
separate from the ROS 2 bridge. Clone it anywhere you like:

.. code-block:: bash

   git clone https://github.com/rubixcubic/enpm818z-fall-2026-carla-python.git
   cd enpm818z-fall-2026-carla-python/lecture2

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: table-hover

   * - **Script**
     - **What it does**
   * - ``spectator_view.py``
     - A window onto the simulation: a passive viewer that attaches a camera and
       renders the frames with Pygame.
   * - ``demo1_connect.py``
     - Connects, loads a town, and inspects the blueprint library.
   * - ``demo2_spawn_suite.py``
     - Spawns an ego vehicle and a five-sensor suite, then reports the rate each
       stream actually delivers -- which is not the rate you configured.
   * - ``demo4_weather.py``
     - Cycles the weather presets and reports mean LiDAR returns and RADAR
       detections per scan for each.
   * - ``lidar_to_camera.py``
     - Projects LiDAR points into the camera image: the whole calibration chain,
       executed once.
   * - ``carla_common.py``
     - Shared helpers -- synchronous-mode setup, actor cleanup on exit, and
       sensor mounts derived from each vehicle's bounding box. Imported by the
       others rather than run directly.

Run them from that directory with the server already up:

.. code-block:: bash

   python3 demo1_connect.py --town Town03

.. note::
   These scripts put the server into **synchronous mode** and destroy every
   actor they created on the way out, including on ``Ctrl+C``. That matters: a
   leaked sensor keeps consuming server resources until the map is reloaded.

   Only one client should own the clock. If a demo script is calling
   ``world.tick()``, do not run a second one that also ticks --
   ``spectator_view.py`` is safe alongside them because it never ticks.

---------------------------------------------------------
Load Town04
---------------------------------------------------------
Load Town04

Download :download:`load_town04.py <scripts/load_town04.py>`. Your browser saves
it to ``~/Downloads`` unless you tell it otherwise.

.. tip::
   If your browser **displays** the script in a new tab instead of saving it,
   right-click the link and choose *Save Link As*. Browsers render ``.py`` as
   plain text, and the download hint is not always honoured. You can also copy
   the code straight from the listing below using the copy button in its
   top-right corner, and paste it into a file named ``load_town04.py``.

Run it **on the host** (not inside the container), with the server running:

.. code-block:: bash

   cd ~/Downloads
   python3 load_town04.py

.. note::
   ``python3 load_town04.py`` looks for the file in your **current directory**.
   Running it from anywhere else gives::

      python3: can't open file '/home/you/load_town04.py': [Errno 2] No such file or directory

   Either ``cd`` to where you saved it first, as above, or give the full path:

   .. code-block:: bash

      python3 ~/Downloads/load_town04.py

.. code-block:: text

   Loading Town04. This can take up to a minute.
   Map:          Carla/Maps/Town04
   Spawn points: 372

It takes optional arguments if you need them:

.. code-block:: bash

   python3 load_town04.py --map Town05        # load a different map
   python3 load_town04.py --host 192.168.1.10 # server on another machine
   python3 load_town04.py --help              # all options

The script:

.. literalinclude:: scripts/load_town04.py
   :language: python
   :linenos:

.. note::
   Two details in the script are worth copying into your own code.

   - ``set_timeout(60.0)``. Loading a map takes far longer than an ordinary API
     call, and the 10 s used in most examples is often not enough on a first
     load.
   - It calls ``get_available_maps()`` **before** ``load_world()``. Asking for a
     map the server does not have otherwise fails as a generic timeout, which
     looks identical to the server being down. Checking first turns that into an
     immediate, specific error.

.. _seeing-the-simulation-ubuntu24:

---------------------------------------------------------
Seeing the Simulation
---------------------------------------------------------


.. tab-set::

   .. tab-item:: Native (22.04)
      :sync: native

      The server opens its own window, so you can watch the simulation there
      directly. The camera follows the *spectator* actor; drag with the mouse
      and move with ``W A S D``.

      You can also use the viewer client below if you would rather follow the
      ego vehicle than fly the spectator around.

   .. tab-item:: Docker (24.04)
      :sync: docker

      A headless server opens no window, so nothing appears when ``carla_basic``
      finishes. To watch the simulation, run the **viewer client** below. It
      renders on your desktop's normal graphics path and never touches Unreal's,
      which is why it works when a windowed server does not -- see
      :ref:`why-headless`.

.. code-block:: bash

   python3 spectator_view.py              # follow the ego vehicle, or spawn one
   python3 spectator_view.py --no-spawn   # only follow, never spawn

.. list-table:: Viewer keys
   :widths: 22 78
   :header-rows: 1
   :class: table-hover

   * - **Key**
     - **Action**
   * - ``TAB``
     - next weather preset
   * - ``C``
     - next camera position
   * - ``R``
     - toggle autopilot
   * - ``ESC`` or ``Q``
     - quit

The viewer is a **passive observer**: it never calls ``world.tick()``. Run it
alongside a demo script that owns the clock, or on its own against a
free-running server.

.. note::
   **Changing the map while the viewer is open is safe.** ``load_world()`` --
   which is what a ``--town`` option calls -- destroys every actor in the world,
   including the viewer's own car and camera, so the window blanks and reloads.
   ``spectator_view.py`` detects that, re-attaches to the new episode and carries
   on. You do not need to restart it.

   Your own scripts are not automatically so forgiving. Anything holding actor
   handles across a ``load_world()`` will find every one of them dead.

---------------------------------------------------------
Troubleshooting
---------------------------------------------------------

Cannot Connect to CARLA
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``Failed to connect to CARLA: timeout``

**Solutions:**

1. Wait for CARLA to fully load (30-60 seconds after window appears)

2. Check CARLA container is running:

   .. code-block:: bash

      docker ps

   You should see output similar to:

   .. code-block:: text

      CONTAINER ID   IMAGE                      STATUS          NAMES
      a1b2c3d4e5f6   carlasim/carla:0.9.16      Up 2 minutes    carla-server

   - If the ``STATUS`` column says ``Up``, the container is running.
   - If the container is not listed, it may have exited. Run ``docker ps -a`` to see all containers
     (including stopped ones). The ``STATUS`` column will show the exit code
     (e.g., ``Exited (1) 30 seconds ago``), which can help diagnose why it stopped.
   - To restart a stopped container: ``docker start carla-server``. The server
     runs detached, so follow its output with ``docker logs -f carla-server``
     rather than attaching with ``-ai``.

3. Verify CARLA is listening on its default port (2000):

   .. code-block:: bash

      netstat -tuln | grep 2000

   Expected output:

   .. code-block:: text

      tcp   0   0   0.0.0.0:2000   0.0.0.0:*   LISTEN

   If there is no output, CARLA has not finished starting yet or crashed during initialization.
   Check the container logs for errors:

   .. code-block:: bash

      docker logs carla-server

4. Verify the CARLA Python client can connect:

   .. code-block:: bash

      python3 -c "import carla; c = carla.Client('localhost', 2000); c.set_timeout(2.0); print(c.get_server_version())"

   This should print the server version (e.g., ``0.9.16``). If it raises a timeout error, CARLA
   is either still loading or the ``--net=host`` flag was not used when starting the container.

---------------------------------------------------------
Next Steps
---------------------------------------------------------


- :doc:`ROS 2 Bridge <carla-ros2>` -- publish CARLA sensor data onto ROS 2
  topics.


---------------------------------------------------------
References
---------------------------------------------------------


- Python API Reference: https://carla.readthedocs.io/en/0.9.16/python_api/
- Blueprint Library: https://carla.readthedocs.io/en/0.9.16/bp_library/
- CARLA Documentation: https://carla.readthedocs.io/en/0.9.16/
