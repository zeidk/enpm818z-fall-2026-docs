====================================================
Exercises
====================================================

This page contains five take-home exercises that reinforce the concepts
from Lecture 12. Exercises cover end-to-end architectures, behavior
cloning, and attention visualization.


.. dropdown:: Exercise 1 -- Modular vs. End-to-End Trade-Offs
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Develop a nuanced understanding of when modular and end-to-end
   pipelines each have the advantage.


   .. raw:: html

      <hr>


   **Specification**

   For each criterion below, indicate whether **modular** or **E2E**
   has the advantage and write a 1--2 sentence justification.

   .. list-table::
      :widths: 40 15 45
      :header-rows: 1
      :class: compact-table

      * - Criterion
        - Advantage
        - Justification
      * - Debugging a false detection
        -
        -
      * - Handling a never-before-seen object
        -
        -
      * - Optimizing full-system performance jointly
        -
        -
      * - Satisfying safety certification (ISO 26262)
        -
        -
      * - Development speed with a small team (< 5 engineers)
        -
        -
      * - Leveraging billions of driving miles
        -
        -

   **Deliverable**

   Completed table with clear justifications.


.. dropdown:: Exercise 2 -- Information Loss at Module Boundaries
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Identify what information is discarded in a modular pipeline and
   reason about safety implications.


   .. raw:: html

      <hr>


   **Specification**

   In a modular pipeline, perception outputs bounding boxes
   ``(class, x, y, z, w, h, l, confidence)`` to the planner.

   1. Name **three types of information** present in the raw sensor
      data that are **lost** by the time the planner receives bounding
      boxes. Be specific.
   2. For each type of lost information, describe a **concrete driving
      scenario** where it would be safety-critical.
   3. Explain how **UniAD's architecture** (query-based unified
      decoder) addresses the information loss problem.
   4. What is the **trade-off** of passing richer intermediate
      representations (e.g., BEV feature maps) instead of bounding
      boxes? Consider compute cost, bandwidth, and interpretability.

   **Deliverable**

   Written answers (one paragraph per question).


.. dropdown:: Exercise 3 -- Behavior Cloning Data Collection
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Collect and analyze a small expert driving dataset from CARLA's
   autopilot for behavior cloning.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``collect_bc_data.py`` that performs the following:

   1. Spawn an ego vehicle with autopilot enabled and an RGB camera
      (640 × 480) in Town01.
   2. Record **500 frames** at 10 Hz. For each frame, save:

      - RGB image to disk.
      - Vehicle controls: ``steer``, ``throttle``, ``brake``.
      - Vehicle speed (m/s).
      - Frame index and timestamp.

   3. Save the metadata to a CSV file.
   4. After collection, compute and print:

      - **Distribution of steering angles** (histogram with 20 bins).
      - **Fraction of stopped frames** (speed < 0.5 m/s).
      - **Min/max/mean speed**.

   **Written analysis**

   - Is the steering distribution balanced or skewed? What problem
     does skew cause for training?
   - Why should stopped frames be subsampled?
   - Why should train/validation splits be done **by episode** rather
     than by random frame?

   **Deliverable**

   The script, CSV file, steering histogram, and written analysis.


.. dropdown:: Exercise 4 -- Simple Steering Network
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Train a minimal behavior cloning model to predict steering angle
   from camera images and test it in CARLA.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``steer_net.py`` that implements the following:

   1. Define a simple network using a pre-trained ResNet-18 backbone
      with the final FC layer replaced to output a **single steering
      value**:

      .. code-block:: python

         import torch.nn as nn
         from torchvision import models

         class SteerNet(nn.Module):
             def __init__(self):
                 super().__init__()
                 self.backbone = models.resnet18(pretrained=True)
                 self.backbone.fc = nn.Linear(512, 1)

             def forward(self, x):
                 return self.backbone(x)

   2. Load the dataset from Exercise 3. Resize images to 224 × 224,
      normalize using ImageNet statistics.
   3. Split **80/20 by episode** into train/validation sets.
   4. Train for **20 epochs** with MSE loss and Adam optimizer
      (lr = 1e-4). Plot train and validation loss.
   5. Report **MAE** (mean absolute error) for steering on the
      validation set.

   **Written analysis**

   Deploy the model in CARLA (feed camera images, apply predicted
   steering). Does the vehicle stay in lane? For how many seconds?
   Relate any failures to the distribution shift problem from L11.

   **Deliverable**

   The script, training loss plot, MAE value, and written analysis.


.. dropdown:: Exercise 5 -- Attention Visualization
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Visualize what a vision transformer attends to in driving images
   and reason about task relevance.


   .. raw:: html

      <hr>


   **Specification**

   Create the file ``attention_viz.py`` that performs the following:

   1. Load a pre-trained **CLIP ViT-B/16** model.
   2. Capture two CARLA driving images:

      - One under ``ClearNoon``.
      - One under ``HardRainNoon``.

   3. Pass each image through the model and extract **attention
      weights** from the last transformer layer.
   4. Reshape the CLS token's attention over patches to a 2D grid
      and overlay it as a heatmap on the original image.
   5. Save both visualizations side-by-side.

   **Written analysis**

   - Does the model attend to **task-relevant regions** (road,
     vehicles, traffic signs)?
   - How does the attention pattern change between clear and rainy
     conditions?
   - What does this tell you about using pre-trained vision models
     for driving?

   **Deliverable**

   The script, side-by-side attention heatmap image, and written
   analysis (5--8 sentences).
