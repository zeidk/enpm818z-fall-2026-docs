====================================================
GP5: Vision-Language-Action Driving (Optional)
====================================================

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP5 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 12 -- Week 15, concurrent with GP4 and Final Report)
      * - **Weight**
        - Bonus: up to 10 points added to the final project score (100-point scale)
      * - **Lectures**
        - L10 (Trajectory Planning & Control), L11 (Prediction & Decision-Making), L12 (End-to-End Driving & Foundation Models)
      * - **Team Size**
        - Same team as GP1--GP4
      * - **Submission**
        - Canvas + GitHub repository link
      * - **Prerequisites**
        - GP1--GP3 completed. GP4 may be in progress.

.. important::

   GP5 is **entirely optional**. It does not replace any part of GP1--GP4 or
   the Final Report. Teams that complete GP5 receive **up to 10 bonus points**
   on the 100-point project scale, which can compensate for points lost
   elsewhere or push a strong project above the standard ceiling.


Overview
--------

GP5 challenges you to build a **simplified Vision-Language-Action (VLA)
model** that drives a vehicle in CARLA by mapping camera images and
natural language commands directly to driving actions -- bypassing the
modular perception-planning-control pipeline you built in GP1--GP4.

This is cutting-edge technology: VLA models (DriveVLM, NVIDIA Alpamayo,
Wayve LINGO-2) represent the frontier of autonomous driving research,
combining the visual understanding of vision models, the reasoning
capability of language models, and the action generation of control
policies.

Your simplified VLA pipeline:

.. code-block:: text

   ┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐
   │ CARLA Camera │────>│ Vision Encoder   │────>│                   │
   │ (RGB image)  │     │ (frozen CLIP     │     │  Action Decoder   │
   └─────────────┘     │  ViT-B/16)       │     │  (trainable MLP)  │──> [steer, throttle, brake]
                        └──────────────────┘     │                   │
   ┌─────────────┐     ┌──────────────────┐     │                   │
   │ Language     │────>│ Text Encoder     │────>│                   │
   │ Command      │     │ (frozen CLIP     │     └───────────────────┘
   │ (string)     │     │  text encoder)   │
   └─────────────┘     └──────────────────┘

The key insight: by using **pre-trained, frozen encoders** (CLIP) for
both vision and language, the only trainable component is a small action
decoder MLP -- making this feasible on a single GPU in a few hours of
training.


Learning Objectives
-------------------

After completing GP5, you will be able to:

- Collect and curate expert driving demonstrations from CARLA's autopilot.
- Use pre-trained vision-language models (CLIP) as frozen feature extractors
  for autonomous driving.
- Train a behavior cloning model that maps visual features to continuous
  driving actions.
- Add language conditioning to a driving policy, enabling command-following
  behavior (e.g., "turn left at the intersection," "follow the road").
- Compare end-to-end VLA driving against the modular GP1--GP4 pipeline
  on the same evaluation scenarios.
- Analyze failure modes of end-to-end driving and articulate the trade-offs
  between modular and learned approaches.


Provided Resources
------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - File
     - Description
   * - ``collect_expert_data.py``
     - Script to collect labeled driving data from CARLA's autopilot with
       synchronized camera images, vehicle controls, and route commands.
   * - ``vla_dataset.py``
     - PyTorch Dataset class for loading collected driving data with vision
       and language features.
   * - ``vla_model.py``
     - Skeleton VLA model with frozen CLIP encoders and a trainable action
       decoder (students complete the decoder architecture).
   * - ``train_vla.py``
     - Training loop skeleton with logging and checkpointing.
   * - ``vla_node.py``
     - ROS 2 node skeleton that runs the trained VLA model for inference
       and publishes vehicle control commands.
   * - ``evaluate_vla.py``
     - Evaluation script that compares VLA driving against the modular
       pipeline on shared scenarios.


Task 1: Expert Data Collection (20 points)
-------------------------------------------

Collect a diverse driving dataset from CARLA's built-in autopilot.

**Requirements:**

- Collect at least **10,000 frames** across 3+ towns and 3+ weather
  conditions.
- Each frame records: RGB image (front camera), vehicle control
  (steer, throttle, brake), vehicle state (speed, location, heading),
  and a **language command** describing the current driving intent.

**Language command generation:**

Language commands are automatically generated from the ``RoadOption``
annotations of the active route:

.. code-block:: python

   import carla
   from agents.navigation.global_route_planner import GlobalRoutePlanner
   from agents.navigation.basic_agent import BasicAgent

   # Map RoadOption to natural language commands
   COMMAND_MAP = {
       'LANEFOLLOW':      "follow the road",
       'LEFT':            "turn left at the intersection",
       'RIGHT':           "turn right at the intersection",
       'STRAIGHT':        "go straight through the intersection",
       'CHANGELANELEFT':  "change to the left lane",
       'CHANGELANERIGHT': "change to the right lane",
   }

   def collect_frame(vehicle, camera_data, current_road_option):
       """Collect a single training frame."""
       control = vehicle.get_control()
       velocity = vehicle.get_velocity()
       speed = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5

       frame = {
           'image': camera_data,                          # RGB array
           'steer': control.steer,                        # [-1, 1]
           'throttle': control.throttle,                  # [0, 1]
           'brake': control.brake,                        # [0, 1]
           'speed_kmh': speed,
           'command': COMMAND_MAP.get(current_road_option.name,
                                      "follow the road"),
       }
       return frame

**Data diversity requirements:**

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Dimension
     - Minimum Coverage
   * - Towns
     - Town01, Town03, Town04 (residential, urban grid, highway)
   * - Weather
     - ClearNoon, HardRainNoon, ClearSunset (minimum 3)
   * - Commands
     - At least 500 frames each for: follow, turn left, turn right,
       go straight, lane change
   * - Speed range
     - 0--80 km/h (include stopped, urban, and highway speeds)

.. admonition:: Data Quality Tips
   :class: tip

   - **Filter out stopped frames**: If the autopilot is waiting at a red
     light for 30 seconds, you get 900 identical frames. Subsample stopped
     frames to at most 10% of the dataset.
   - **Balance commands**: Left/right turns are rarer than lane following.
     Collect extra data at intersections or oversample turn frames during
     training.
   - **Augment weather**: Vary sun angle, rain intensity, and fog density
     programmatically between collection runs.


Task 2: Build the VLA Model (30 points)
-----------------------------------------

Implement the simplified VLA architecture using pre-trained CLIP encoders.

**Architecture:**

.. code-block:: python

   import torch
   import torch.nn as nn
   from transformers import CLIPModel, CLIPProcessor

   class SimpleVLA(nn.Module):
       """
       Simplified Vision-Language-Action model.

       Vision encoder:  CLIP ViT-B/16 (frozen) -> 512-dim feature
       Language encoder: CLIP text encoder (frozen) -> 512-dim feature
       Action decoder:  MLP (trainable) -> [steer, throttle, brake]
       """

       def __init__(self, hidden_dim=256, dropout=0.1):
           super().__init__()

           # Frozen CLIP encoders
           self.clip = CLIPModel.from_pretrained(
               "openai/clip-vit-base-patch16")
           self.processor = CLIPProcessor.from_pretrained(
               "openai/clip-vit-base-patch16")

           # Freeze all CLIP parameters
           for param in self.clip.parameters():
               param.requires_grad = False

           # Trainable action decoder
           # Input: vision_feat (512) + text_feat (512) + speed (1) = 1025
           self.action_decoder = nn.Sequential(
               nn.Linear(1025, hidden_dim),
               nn.ReLU(),
               nn.Dropout(dropout),
               nn.Linear(hidden_dim, hidden_dim),
               nn.ReLU(),
               nn.Dropout(dropout),
               nn.Linear(hidden_dim, 3),  # [steer, throttle, brake]
           )

           # Output activation: steer in [-1,1], throttle/brake in [0,1]
           self.steer_activation = nn.Tanh()
           self.pedal_activation = nn.Sigmoid()

       def forward(self, images, commands, speeds):
           """
           Args:
               images: PIL images or tensors (B,)
               commands: list of strings (B,)
               speeds: tensor (B, 1) normalized speed
           Returns:
               actions: tensor (B, 3) [steer, throttle, brake]
           """
           # Encode vision (frozen)
           with torch.no_grad():
               inputs = self.processor(
                   images=images, text=commands,
                   return_tensors="pt", padding=True
               ).to(next(self.action_decoder.parameters()).device)

               vision_feat = self.clip.get_image_features(
                   pixel_values=inputs['pixel_values'])
               text_feat = self.clip.get_text_features(
                   input_ids=inputs['input_ids'],
                   attention_mask=inputs['attention_mask'])

               # Normalize features (as CLIP does)
               vision_feat = vision_feat / vision_feat.norm(
                   dim=-1, keepdim=True)
               text_feat = text_feat / text_feat.norm(
                   dim=-1, keepdim=True)

           # Concatenate features + speed
           combined = torch.cat([vision_feat, text_feat, speeds], dim=-1)

           # Decode actions
           raw = self.action_decoder(combined)
           steer = self.steer_activation(raw[:, 0:1])
           throttle = self.pedal_activation(raw[:, 1:2])
           brake = self.pedal_activation(raw[:, 2:3])

           return torch.cat([steer, throttle, brake], dim=-1)

**Requirements:**

- Use CLIP ViT-B/16 as the frozen vision and text encoder.
- The action decoder must be a trainable MLP with at least 2 hidden layers.
- Include current speed as an additional input to the decoder (the model
  needs to know how fast it is going to decide throttle/brake).
- Output 3 continuous values: steer :math:`\in [-1, 1]`, throttle
  :math:`\in [0, 1]`, brake :math:`\in [0, 1]`.

**Students must complete:**

1. The ``VLADataset`` class that loads images, commands, and controls from
   the collected data.
2. The training loop with MSE loss on the three action outputs.
3. Hyperparameter tuning: hidden dimension, learning rate, dropout, batch
   size.

.. admonition:: Why Frozen Encoders?
   :class: note

   Fine-tuning CLIP's 150M parameters would require far more data and
   compute than is feasible in a course setting. By freezing the encoders,
   we leverage CLIP's pre-trained visual and language understanding while
   only training ~200K parameters in the action decoder. This is
   trainable on a single GTX 1070 in 2--4 hours.


Task 3: Train and Validate (20 points)
----------------------------------------

**Training protocol:**

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Optimizer**
     - AdamW, learning rate 1e-3, weight decay 1e-4
   * - **Loss**
     - Weighted MSE: :math:`\mathcal{L} = 5.0 \cdot \text{MSE}(\hat{s}, s) + 1.0 \cdot \text{MSE}(\hat{t}, t) + 1.0 \cdot \text{MSE}(\hat{b}, b)`
   * - **Batch size**
     - 64 (adjust for GPU memory)
   * - **Epochs**
     - 50--100
   * - **Split**
     - 80% train, 10% validation, 10% test (split by driving episode, not random frames)
   * - **Early stopping**
     - Patience of 10 epochs on validation loss

.. important::

   Split by **driving episode**, not by random frame. Random splitting
   creates data leakage because consecutive frames are nearly identical.
   Each collection run (a full route in one town/weather) should be
   entirely in train, validation, or test.

**Validation metrics (offline):**

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Metric
     - Target
   * - Steering MAE
     - < 0.08 (on normalized [-1, 1] scale)
   * - Throttle MAE
     - < 0.10
   * - Brake MAE
     - < 0.05 (most frames have brake = 0)

**Ablation study (required):**

Train and evaluate three model variants:

1. **Vision-only**: Remove the text encoder input. Concatenate
   ``[vision_feat, zeros(512), speed]``. This is standard behavior cloning.
2. **VLA (full)**: Use both vision and language features. This is the
   complete model.
3. **Language-only** (sanity check): Remove the vision encoder. This should
   perform poorly -- confirming that the model actually uses visual input.

Report the validation loss and per-action MAE for all three variants.


Task 4: Deploy as a ROS 2 Node and Drive (20 points)
------------------------------------------------------

Deploy the trained VLA model as a ROS 2 node that replaces the modular
GP4 planner + controller with a single end-to-end driving policy.

.. code-block:: python

   # vla_node.py -- ROS 2 node skeleton

   import rclpy
   from rclpy.node import Node
   from sensor_msgs.msg import Image
   from geometry_msgs.msg import Twist
   from std_msgs.msg import String, Float32
   from cv_bridge import CvBridge
   import torch
   from PIL import Image as PILImage

   class VLANode(Node):
       def __init__(self):
           super().__init__('vla_node')

           # Load trained model
           self.model = SimpleVLA()
           self.model.load_state_dict(
               torch.load('vla_checkpoint.pt', map_location='cpu'))
           self.model.eval()
           self.device = torch.device(
               'cuda' if torch.cuda.is_available() else 'cpu')
           self.model.to(self.device)

           self.bridge = CvBridge()
           self.current_command = "follow the road"
           self.current_speed = 0.0

           # Subscribers
           self.create_subscription(
               Image, '/carla/ego/camera/image', self.image_cb, 10)
           self.create_subscription(
               String, '/navigation/command', self.command_cb, 10)
           self.create_subscription(
               Float32, '/carla/ego/speed', self.speed_cb, 10)

           # Publisher
           self.control_pub = self.create_publisher(
               Twist, '/carla/ego/control', 10)

           self.get_logger().info("VLA node initialized.")

       def command_cb(self, msg):
           self.current_command = msg.data

       def speed_cb(self, msg):
           self.current_speed = msg.data

       def image_cb(self, msg):
           # Convert ROS image to PIL
           cv_image = self.bridge.imgmsg_to_cv2(msg, 'rgb8')
           pil_image = PILImage.fromarray(cv_image)

           # Normalize speed to [0, 1] range (assuming max 100 km/h)
           speed_tensor = torch.tensor(
               [[self.current_speed / 100.0]],
               dtype=torch.float32).to(self.device)

           # Inference
           with torch.no_grad():
               actions = self.model(
                   images=[pil_image],
                   commands=[self.current_command],
                   speeds=speed_tensor)

           steer = actions[0, 0].item()
           throttle = actions[0, 1].item()
           brake = actions[0, 2].item()

           # Publish control
           control_msg = Twist()
           control_msg.angular.z = steer
           control_msg.linear.x = throttle - brake  # net acceleration
           self.control_pub.publish(control_msg)

**Requirements:**

- The VLA node must run at **>= 10 Hz** inference rate.
- Language commands are provided by the navigation module (``/navigation/command``
  topic) based on the active route's ``RoadOption`` annotations.
- Test on the same two GP4 scenarios (``town01_route.yaml`` and
  ``town03_route.yaml``).

.. admonition:: Integration with GP1--GP3
   :class: tip

   The VLA node **replaces** ``planner_node.py``, ``controller_node.py``,
   and ``behavior_node.py`` from GP4. The GP1 sensor nodes and GP2/GP3
   perception nodes can optionally still run (e.g., for collision
   detection or visualization) but are not required for VLA driving.


Task 5: Comparative Evaluation and Report (10 points)
------------------------------------------------------

Compare the VLA driving performance against your modular GP4 pipeline
on identical scenarios.

**Evaluation metrics:**

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * - Metric
     - Modular (GP4)
     - VLA (GP5)
   * - Route completion (%)
     - (your result)
     - (your result)
   * - Collisions
     - (your result)
     - (your result)
   * - Average speed (km/h)
     - (your result)
     - (your result)
   * - Red light violations
     - (your result)
     - (your result)
   * - Inference latency (ms)
     - (your result)
     - (your result)
   * - Comfort (lateral jerk)
     - (your result)
     - (your result)

**Report (3--5 pages, added to the Final Report as an appendix):**

1. **Architecture diagram** of the VLA model with encoder/decoder details.
2. **Training curves** (train/val loss over epochs) for all three ablation
   variants.
3. **Quantitative comparison** table (above) with analysis.
4. **Qualitative analysis**: Describe at least 3 failure modes of the VLA
   model. For each, explain: (a) what happened, (b) why the modular
   pipeline handles it better (or worse), and (c) what would be needed to
   fix it.
5. **Command-following demonstration**: Show that the VLA model responds
   differently to different language commands at the same intersection
   (e.g., "turn left" vs. "go straight").
6. **Reflection**: In your team's assessment, which approach (modular vs.
   VLA) is more promising for production autonomous driving, and why?

.. important::

   The goal is **not** to beat the modular pipeline. The VLA model will
   likely perform worse on structured metrics (especially traffic rule
   compliance). The goal is to understand the trade-offs, failure modes,
   and potential of end-to-end driving -- and to gain hands-on experience
   with a technology that is actively reshaping the industry.


Grading Rubric
--------------

.. list-table::
   :widths: 50 10
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
   * - Task 1: Data collection (10K+ frames, diversity requirements met)
     - 2
   * - Task 2: VLA model implementation (architecture, training loop)
     - 3
   * - Task 3: Training + ablation study (3 variants, metrics reported)
     - 2
   * - Task 4: ROS 2 deployment (>= 10 Hz, drives both scenarios)
     - 2
   * - Task 5: Comparative evaluation and report
     - 1
   * - **Total (bonus)**
     - **10**

.. note::

   Partial credit is awarded. A team that collects good data and trains
   the model but cannot achieve stable driving still earns credit for
   Tasks 1--3. The evaluation in Task 5 can discuss failures honestly --
   insightful failure analysis is valued.


Suggested Timeline
------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - Week
     - Milestone
   * - Week 12
     - Collect expert data (10K+ frames). Set up CLIP encoders and
       dataset loader. Begin training the vision-only baseline.
   * - Week 13
     - Complete VLA model with language conditioning. Train all three
       ablation variants. Validate offline metrics.
   * - Week 14--15
     - Deploy as ROS 2 node. Run evaluation scenarios. Complete
       comparative analysis and report appendix.


Technical Requirements
----------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Component
     - Requirement
   * - GPU
     - NVIDIA GPU with >= 6 GB VRAM (GTX 1060+). CLIP ViT-B/16 inference
       requires ~2 GB; training the decoder adds ~1 GB.
   * - Python packages
     - ``torch >= 2.0``, ``transformers >= 4.30``, ``Pillow``,
       ``opencv-python``, ``numpy``
   * - Disk space
     - ~5 GB for 10K frames (640x480 JPEG) + model checkpoints
   * - Training time
     - 2--4 hours on a GTX 1070 for 100 epochs with batch size 64

.. tip::

   If your team has limited GPU resources, use Google Colab (free tier
   provides a T4 GPU) for training. Data collection and ROS 2 deployment
   must be done locally with CARLA.


Further Reading
---------------

- **DriveVLM** (Tian et al., 2024) -- Autonomous driving with large
  vision-language models for scene understanding and planning.
- **NVIDIA Alpamayo** -- VLA model for autonomous driving combining visual
  perception, language reasoning, and action generation.
- **Wayve LINGO-2** (2024) -- Vision-language-action model for driving with
  natural language explanations of driving decisions.
- **RT-2** (Brohan et al., 2023) -- Robotics Transformer 2: vision-language-
  action model originally for manipulation, demonstrating the VLA paradigm.
- **CLIP** (Radford et al., 2021) -- Learning transferable visual models
  from natural language supervision. Foundation for the frozen encoders
  used in this assignment.
