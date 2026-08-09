====================================================
Pre-Read: Development Environment
====================================================

.. admonition:: Read this before Lecture 1
   :class: important

   This page is **pre-read material**, not lecture content. It is
   assumed knowledge from ENPM605 and is reproduced here so you can set
   your machine up before the first class. Nothing here is examined
   directly, but every group project depends on it working.

   Work through it, then install CARLA using the
   :doc:`setup guide </carla/carla>`.

Operating System & Software
---------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Component
     - Details
   * - **OS**
     - Ubuntu 22.04 LTS (Jammy) or Ubuntu 24.04 LTS (Noble)
   * - **ROS 2**
     - Humble Hawksbill (22.04) or Jazzy Jalisco (24.04)
   * - **CARLA**
     - 0.9.16 (native on 22.04; Docker on 24.04)
   * - **IDE**
     - Visual Studio Code
   * - **Python**
     - 3.10+ with ``numpy``, ``matplotlib``, ``opencv-python``, ``carla``
   * - **Version Control**
     - Git + GitHub

Version Control (Git & GitHub)
------------------------------

Git is a version control system that tracks changes in your files over time.

.. code-block:: bash

   # Install Git
   sudo apt update && sudo apt install git

   # Configure
   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@umd.edu"

   # Verify
   git config --list

**Essential Git commands:**

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: Daily Commands

      .. code-block:: bash

         git status          # Check status
         git add .           # Stage changes
         git commit -m "msg" # Commit
         git push            # Upload to GitHub
         git pull            # Download updates

   .. grid-item-card:: Branching Commands

      .. code-block:: bash

         git branch          # List branches
         git checkout -b new # Create & switch
         git merge branch    # Merge branch
         git branch -d old   # Delete branch

**GitHub** is a cloud-based platform that hosts Git repositories. Course
materials are available at the course GitHub repository.


Visual Studio Code
------------------

VS Code is a free, open-source code editor available on all platforms. It is
consistently ranked as the most popular code editor in developer surveys.

**Installation:**

.. code-block:: bash

   # Download .deb from https://code.visualstudio.com/download
   cd ~/Downloads
   sudo apt install ./code_<version>_amd64.deb

**Key features:**

- Activity Bar (left side): File explorer, search, source control, extensions.
- Editor: Where you write code.
- Integrated Terminal: For running commands.
- Command Palette: ``Ctrl+Shift+P`` for all VS Code actions.

**Recommended extensions** for this course: Python, Pylance, ROS, YAML,
GitLens, Docker (if using Jazzy setup).

.. tip::

   The ``.vscode`` folder in your project root stores workspace-specific
   settings (``settings.json``, ``launch.json``, ``extensions.json``). These
   override your global VS Code settings.


Programming Guidelines
----------------------

In this course we follow:

- `PEP 8 <https://peps.python.org/pep-0008/>`_ -- Python style guide.
- `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_ -- For any C++ code.

.. warning::

   One way to lose points on assignments is by failing to follow coding guidelines.


Linux Shell Essentials
----------------------

A shell is a program that provides a command-line interface for interacting
with the operating system.

**Common shells:**

- **Bash** (``~/.bashrc``) -- Default for most Linux distributions.
- **Zsh** (``~/.zshrc``) -- Enhanced autocompletion and customization.

**Useful concepts:**

.. tab-set::

   .. tab-item:: Aliases

      Shortcuts that save you from typing long commands:

      .. code-block:: bash

         alias cdd='cd ~/Documents'
         alias sr='source ~/.bashrc'   # or source ~/.zshrc

   .. tab-item:: File Sourcing

      Apply changes to your shell configuration without opening a new terminal:

      .. code-block:: bash

         source ~/.bashrc

   .. tab-item:: Functions

      Reusable blocks of commands:

      .. code-block:: bash

         my_function() {
             echo "Hello from my_function"
             cd ~/catkin_ws && colcon build
         }

.. tip::

   Check your current shell with ``ps -p $$``.


