====================================================
Going Further
====================================================

.. admonition:: Reading material, not covered in class
   :class: note

   This page is the written version of the deck's appendix. It is **reading
   material**: we do not present it in class, and it is **not on the quiz**.

   Each section picks up a topic from the :doc:`lecture <l4_lecture>` and
   works it out with more numbers or more steps. The sections follow the
   deck's order. Read the one you need, when you need it.

The running example is the lecture's: ``bus.jpg``, the sample image that
ships with the Ultralytics library, :math:`810 \times 1080` pixels. Sizes on
this page are always width by height. A city bus is parked at the curb, and
people walk past it. The person we follow is **the man in the light-colored
jacket**. YOLOv8s finds him with the box from (49.9, 401.8) to
(244.5, 901.8), in image pixels. Our two models are **YOLOv8s** (YOLO, "you
only look once", version 8, size s for small) and **RT-DETR-L** (Real-Time
DEtection TRansformer, size L for large).

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Section**
     - **What it adds to the lecture**
   * - `CNN Fundamentals`_
     - The convolutional network from a single neuron up: convolution,
       activation, pooling, batch normalization, training, and fine-tuning.
   * - `Decoding a YOLO Cell`_
     - The man's box decoded by hand from one grid cell of YOLOv8s.
   * - `AP in Detail`_
     - How the COCO evaluation code marks each box right or wrong, and how it
       turns the ranked list into one number.
   * - `Detectors on an AV`_
     - Which detector goes with which sensor, what three companies publish
       about their sensors, and the YOLO model sizes.
   * - `More on Transformers`_
     - Vectors you can add, and how much of the image one CNN layer and one
       transformer layer each read.


CNN Fundamentals
----------------

This section covers the material from ENPM673 that the lecture assumes, from
the ground up. It is for anyone who has not taken ENPM673 or wants a
refresher. A **convolutional neural network (CNN)** is a network built
mostly from convolutions, the operation defined below. Every example uses
our bus image or YOLOv8s, so the numbers connect to the lecture.

The section continues three parts of the :doc:`lecture <l4_lecture>`:
**Perception** (a network and its weights), **Object Detection** (how a
detector is trained) and **From Pixels to Features** (layers and the CNN).
It has five parts:

1. A neuron, and why a plain network does not scale to images.
2. Convolution: one filter, many channels, stride and padding.
3. Activation, pooling, batch normalization and receptive field.
4. Training: loss, gradient descent, softmax and cross-entropy.
5. Generalization, classic architectures and fine-tuning.

One Neuron
~~~~~~~~~~

The lecture called each model a **network**, short for neural network: a
function with adjustable numbers, its **weights**, set by training on
examples. Every network is built from one small piece, the neuron.

.. admonition:: Definition: neuron
   :class: note

   A weighted sum of its inputs, plus a **bias**, passed through an
   **activation** function :math:`\sigma`:

   .. math::

      y = \sigma(w_1 x_1 + w_2 x_2 + \dots + b)

Here :math:`x_1, x_2, \dots` are the inputs, :math:`w_1, w_2, \dots` the
weights, :math:`b` the bias (one extra number added to the sum) and
:math:`y` the output.

Take the dark-blue pixel of the bus from the lecture's From Pixels to
Features section. Its red, green and blue values are
:math:`(R, G, B) = (20, 83, 152)`. The weights and bias are chosen for this
example: :math:`w = (0.5, -0.2, 0.1)` and :math:`b = -5`.

1. Weighted sum: half of the red, minus a fifth of the green, plus a tenth
   of the blue.

   .. math::

      0.5 \times 20 - 0.2 \times 83 + 0.1 \times 152 = 10 - 16.6 + 15.2 = 8.6

2. Add the bias: :math:`8.6 - 5 = 3.6`.
3. Apply the activation. Here it is **ReLU** (rectified linear unit): keep
   positive numbers, turn negative ones into zero. So
   :math:`\max(0, 3.6) = 3.6`, and the neuron outputs **3.6**.

A network is thousands of these neurons. **Training** means finding the
weights and biases that make the final outputs useful.

Why Not Connect Every Pixel to Every Neuron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A plain network connects every input to every neuron. For images, that does
not scale. The detector sees our image at 480 pixels wide and 640 high, with
3 colors:

.. math::

   480 \times 640 \times 3 = 921{,}600 \text{ inputs}

One neuron connected to all of them needs 921,600 weights. Compare two ways
to build a first layer with 32 outputs:

.. list-table::
   :widths: 55 45
   :header-rows: 1
   :class: compact-table

   * - **First layer, 32 outputs**
     - **Weights**
   * - Every pixel to each of 32 neurons
     - :math:`921{,}600 \times 32 = 29{,}491{,}200`
   * - YOLOv8s: 32 filters of :math:`3 \times 3 \times 3` (measured)
     - :math:`32 \times 27 =` **864**

The plain layer needs 29.5 million weights for one layer. It would also have
to learn separately that an edge on the left of the image is the same thing
as an edge on the right. YOLOv8s's real first layer, measured, has 32
filters, each 3 by 3 pixels by 3 colors, so 27 weights each and 864 in
total.

.. important::

   Two ideas cut the count. Each output looks at a **small window** only.
   And the **same** filter is reused at every position, so an edge detector
   learned once works everywhere in the image. That sliding is convolution.

Convolution
~~~~~~~~~~~

Every CNN is built on one operation, the convolution.

.. admonition:: Definition: convolution
   :class: note

   Slide a small grid of weights, the **filter**, over the input. At each
   position, multiply cell by cell and add. Each position gives one output
   number.

.. figure:: /_static/images/L4/conv_grid.png
   :alt: A 5 by 5 input grid labeled input 5 x 5, with its top-left 3 by 3 window shaded green and outlined. An arrow leads to a 3 by 3 grid labeled output 3 x 3, whose top-left cell is shaded green.
   :width: 55%
   :align: center

   A :math:`3 \times 3` filter on a :math:`5 \times 5` input. The filter
   over the top-left corner (green) gives the top-left output number
   (green).

Lay the 3 by 3 filter over the top-left corner of the input, the green
square. Multiply each input number by the weight on top of it and add all
nine products. That sum is one output number, the green cell on the right.
Then slide the filter one step and repeat, over every position. A 3 by 3
filter fits in three positions across a 5-wide input, and three down, so the
output is 3 by 3.

The edge filter in the lecture, right column minus left column, is this
operation with weights of -1, 0 and +1. A network learns its filter weights
instead of having them written by hand.

.. note::

   If you know signal processing: strictly, this operation is
   **cross-correlation**. Mathematical convolution flips the filter first.
   Deep learning calls it convolution anyway. Since the weights are learned,
   the flip makes no difference.

Several Input Channels
~~~~~~~~~~~~~~~~~~~~~~

An image has three colors, so every filter has to handle several input
**channels** at once. A channel is one 2-D grid of numbers: the red values,
say, or one feature map.

- A filter spans **all** input channels. On a color image, a 3 by 3 filter
  is really :math:`3 \times 3 \times 3`: 27 weights. It still gives one
  number per position, a sum over all three colors.
- :math:`C_\text{out}` filters give :math:`C_\text{out}` output channels.
  With 32 filters you get the 32 channels of the next feature map.

With kernel size :math:`k` (the filter is :math:`k` by :math:`k`),
:math:`C_\text{in}` input channels and :math:`C_\text{out}` output channels,
the number of weights in one layer is

.. math::

   k \times k \times C_\text{in} \times C_\text{out}

Measured on YOLOv8s:

- Layer 0 takes 3 colors to 32 channels:
  :math:`3 \times 3 \times 3 \times 32 = 864` weights.
- Layer 1 takes those 32 channels to 64:
  :math:`3 \times 3 \times 32 \times 64 = 18{,}432` weights.
- The whole model has **11,166,560** numbers to learn. That matches the 11.2
  million on the Ultralytics page.

Stride, Padding and Output Size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A convolution also changes the size of its output. Two settings decide by
how much.

- The **stride** :math:`s` is how far the filter moves at each step. Stride
  2 skips every other position, so the output is half the size.
- The **padding** :math:`p` is a border of zeros around the input, so the
  filter can also be centered on the edge pixels.

With input size "in" and kernel size :math:`k`, the output size along one
direction is

.. math::

   \text{out} = \left\lfloor \frac{\text{in} + 2p - k}{s} \right\rfloor + 1

where :math:`\lfloor \cdot \rfloor` means "round down".

1. YOLOv8s layer 0 (measured): :math:`k = 3`, :math:`s = 2`, :math:`p = 1`.
2. Height: :math:`640 + 2 - 3 = 639`. Divided by 2 that is 319.5, rounded
   down 319. Plus one: **320**.
3. Width: :math:`\lfloor (480 + 2 - 3) / 2 \rfloor + 1 = 239 + 1 =`
   **240**.

So the output is :math:`240 \times 320`: the stride-2 map in the lecture.
YOLOv8s has five of these stride-2 layers, and :math:`2^5 = 32`. Then
:math:`480 / 32 = 15` and :math:`640 / 32 = 20`, which gives the
:math:`15 \times 20` grid at stride 32.

Why a Network Needs an Activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stacked convolutions are only more powerful than one if something sits
between them: the activation.

.. important::

   **Without an activation, depth adds nothing.** A layer computes weighted
   sums. A second layer computes weighted sums of those, which is again one
   weighted sum of the inputs. Stack a hundred layers and you still have one
   weighted sum.

.. figure:: /_static/images/L4/activations.png
   :alt: Two curves of output against input, for inputs from -5 to 5. ReLU, max(0, x), solid blue: zero for every negative input, then a straight line equal to the input. SiLU, x / (1 + e^(-x)), dashed orange: close to ReLU, but smooth near zero and slightly below zero for negative inputs, lowest near -1.3.
   :width: 60%
   :align: center

   Two activations. **ReLU** (solid blue) is flat at zero, then a straight
   line. **SiLU** (dashed orange) is smooth near zero and slightly negative
   for negative inputs.

- **ReLU** is the simplest fix: keep positive numbers, turn negative ones
  into zero. The two edge responses from the lecture were 414.7 at the edge
  of a white letter and -9.0 on the flat roof of the bus. ReLU turns them
  into 414.7 and 0: "edge here" and "nothing here".
- **SiLU** (sigmoid linear unit) is what YOLOv8 uses, checked in the model.
  It is a smooth version of ReLU that lets small negative values through:

  .. math::

     \text{SiLU}(x) = \frac{x}{1 + e^{-x}}, \qquad \text{SiLU}(-1) = -0.269

Pooling
~~~~~~~

Feature maps shrink as a network goes deeper. Pooling is one way to shrink
them.

.. admonition:: Definition: max pooling
   :class: note

   Keep only the largest value in each window. With :math:`2 \times 2`
   windows, each 2 by 2 block becomes its maximum, so the size halves.

Take the red channel of the 4 by 4 patch from the lecture, the patch where
the white lettering starts on the side of the bus, and pool it with 2 by 2
windows:

.. math::

   \begin{bmatrix} 20 & 44 & 0 & 177 \\ 47 & 19 & 16 & 186 \\
                   0 & 73 & 14 & 216 \\ 0 & 51 & 32 & 214 \end{bmatrix}
   \;\rightarrow\;
   \begin{bmatrix} 47 & 186 \\ 73 & 216 \end{bmatrix}

The top-left block holds 20, 44, 47 and 19, and the largest is 47. The
top-right block gives 186, the bottom-left 73 and the bottom-right 216. The
4 by 4 becomes 2 by 2.

After an edge filter, a big number means "edge here". Pooling keeps "there
is an edge in this area" and drops its exact pixel. That makes the network
less sensitive to small shifts.

Many older networks pool after every few layers. YOLOv8 shrinks its maps
with stride-2 convolutions instead. It uses max pooling in only one block
near the end of its **backbone** (the part that turns the image into feature
maps). That block is called SPPF, and its windows are 5 by 5, measured in
the model.

Receptive Field: How Much One Cell Sees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each cell of a deep feature map depends on a patch of the input image, and
that patch grows with depth.

.. admonition:: Definition: receptive field
   :class: note

   The patch of the **input** image that can affect one cell of a feature
   map.

A single 3 by 3 layer sees 3 by 3 pixels. Each new layer adds its kernel
size minus one, :math:`k - 1`, times the total stride of the layers
**before** it. The reason: each step of the new filter jumps that many input
pixels. Through YOLOv8s's five stride-2, :math:`3 \times 3` layers
(measured), :math:`k - 1 = 2`:

.. list-table::
   :widths: 28 12 15 15 15 15
   :header-rows: 1
   :class: compact-table

   * - **Layer**
     - **1**
     - **2**
     - **3**
     - **4**
     - **5**
   * - Total stride after it
     - 2
     - 4
     - 8
     - 16
     - 32
   * - Receptive field (pixels)
     - 3
     - :math:`3 + 2 \times 2 = 7`
     - :math:`7 + 2 \times 4 = 15`
     - :math:`15 + 2 \times 8 = 31`
     - :math:`31 + 2 \times 16 =` **63**

This counts only those five layers. The blocks between them widen the field
further. So a cell of the stride-32 map sees **at least** 63 by 63 pixels,
enough for a whole person at a distance. That is why deeper layers respond
to larger things, the pattern the lecture showed.

Batch Normalization
~~~~~~~~~~~~~~~~~~~

Deep stacks train badly when each layer's inputs drift around. Batch
normalization keeps them in a steady range.

For each channel, it looks at that channel's values over a **batch**, the
group of images processed together in one training step. It subtracts their
mean and divides by their standard deviation. Then it scales and shifts the
result by two numbers it learns. Every layer then receives inputs in a
steady range, whatever the layers before it did, so training is faster and
more stable.

The numbers are chosen for this example: one channel's values over a batch
are :math:`(2, 4, 6, 8)`.

1. The mean is 5. The squared distances from it are 9, 1, 1 and 9, so

   .. math::

      \text{variance} = \frac{9 + 1 + 1 + 9}{4} = 5, \qquad
      \text{standard deviation} = \sqrt{5} = 2.236

2. Normalized: :math:`\frac{2 - 5}{2.236} = -1.342`, then -0.447, 0.447 and
   1.342.

In YOLOv8s, every block called "Conv" is exactly three steps: convolution,
then batch normalization, then SiLU (checked in the model).

Learning the Weights: Gradient Descent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A network starts with random weights, and training has to find good ones.
It takes three pieces.

1. A **loss** :math:`L` measures how wrong the output is.
2. The **gradient** :math:`\partial L / \partial w` says, for each weight,
   how the loss changes when that weight changes. **Backpropagation** is the
   algorithm that computes all the gradients at once, working backward from
   the output.
3. **Gradient descent** moves every weight a little downhill, by the
   **learning rate** :math:`\eta` times its gradient:

   .. math::

      w \leftarrow w - \eta \, \frac{\partial L}{\partial w}

The numbers are chosen for this example. There is one weight, the output is
:math:`\hat{y} = w x`, and the loss is the squared error
:math:`L = (w x - y)^2`, with :math:`x = 2`, target :math:`y = 6`,
:math:`w = 1` and :math:`\eta = 0.05`.

1. The output is 2, so the loss is :math:`(2 - 6)^2 = 16`.
2. The gradient is :math:`2 (w x - y) x = 2 \times (-4) \times 2 = -16`.
3. Step against it: :math:`w \leftarrow 1 - 0.05 \times (-16) =` **1.8**.
   Now the output is 3.6 and the loss has dropped to
   :math:`(3.6 - 6)^2 = 5.76`.

Training is this step, repeated thousands of times or more, for millions of
weights at once.

Softmax: From Scores to Probabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A network's last layer gives one raw score per class. A score can be any
number, positive or negative. Softmax turns the scores into shares.

.. admonition:: Definition: softmax
   :class: note

   Turns raw scores :math:`s_1, \dots, s_K`, one per class, into numbers
   that are positive and add to 1:

   .. math::

      p_i = \frac{e^{s_i}}{e^{s_1} + e^{s_2} + \dots + e^{s_K}}

The numbers are chosen for this example: scores :math:`(2.0, 1.0, 0.1)` for
(bus, person, car).

1. Raise :math:`e` to each score: 7.3891, 2.7183 and 1.1052. A power of
   :math:`e` is always positive.
2. Add them: :math:`7.3891 + 2.7183 + 1.1052 = 11.2126`.
3. Divide each by the sum: **0.659**, 0.242 and 0.099. Together they make 1.

The order stays the same, and the largest score gets the largest share. You
met softmax inside attention in the lecture. It also produced the
classifier's 0.616 for "police van" in the Object Detection section.

.. note::

   Detectors differ here. YOLOv8 scores each class on its own with a
   **sigmoid**, :math:`1 / (1 + e^{-x})`, a number from zero to one, instead
   of one softmax over all classes.

Cross-Entropy: The Loss for a Wrong Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Training needs one number that says how wrong a classification is.

.. admonition:: Definition: cross-entropy loss
   :class: note

   The number training makes smaller for classification: minus the natural
   log of the probability the network gave the **correct** class,

   .. math::

      L = -\ln p_{\text{correct}}

Take the probabilities from the softmax example, :math:`(0.659, 0.242,
0.099)` for (bus, person, car). Each row below is a separate case:

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * - **If the truth is**
     - :math:`p_{\text{correct}}`
     - :math:`L = -\ln p_{\text{correct}}`
   * - bus
     - 0.659
     - **0.417**
   * - person
     - 0.242
     - 1.417
   * - car
     - 0.099
     - 2.317
   * - sure and right
     - 1
     - 0

The less probability the network gives the truth, the larger the loss.
Training adjusts the weights to make the loss smaller, with the gradient
descent from earlier in this section.

Train, Validation, Test: Learning, Not Memorizing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A falling training loss does not prove that the network learned anything
general. So you split the data three ways.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Split**
     - **Used for**
   * - **Train**
     - Computing the gradients.
   * - **Validation**
     - Choosing settings: how many **epochs** (passes over the training
       images), which confidence cut, which model size.
   * - **Test**
     - One final score. Never used to choose anything, or it stops being a
       fair test.

.. important::

   **Overfitting:** the training loss keeps falling while the validation
   loss rises. The network is memorizing its training images. The standard
   remedy is **data augmentation**: flip, recolor, crop and combine the
   training images (mosaics), so the network sees more variety without new
   labels.

This matters for any detector you train. Do not pick your confidence cut on
the images you report mAP on. Pick it on the validation set, and report on
the test set.

Four Architectures Behind Today's Backbones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Today's backbones come from four networks. Each added one idea.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Network**
     - **What it added**
   * - **AlexNet** (2012)
     - A deep CNN trained on GPUs, with ReLU. It beat the hand-designed
       features of the time on ImageNet, a large image classification
       dataset. That started the deep learning era in vision (Krizhevsky et
       al., 2012).
   * - **VGG** (2015)
     - Stacks of small :math:`3 \times 3` filters instead of large ones
       (Simonyan and Zisserman, 2015).
   * - **ResNet** (2016)
     - Skip connections: :math:`y = F(x) + x`, so a block learns only a
       correction to its input (He et al., 2016).
   * - **ViT** (2021)
     - No convolution at all: attention over image patches (Dosovitskiy et
       al., 2021).

VGG's argument in numbers: two stacked :math:`3 \times 3` layers see
:math:`5 \times 5` pixels, like one :math:`5 \times 5` layer. But they need
18 weights per channel pair (:math:`2 \times 9`) against 25, and they put an
extra activation in between.

ResNet's skip connection made very deep networks trainable. The same trick
is in every transformer layer from the lecture.

Fine-Tuning
~~~~~~~~~~~

You rarely train a detector from scratch. You **fine-tune** one.

1. **Start** from weights trained on a big dataset: COCO, for both our
   detectors.
2. **Replace the head** (the last part of the network, which outputs the
   classes and boxes) so it outputs your classes: say 5, where COCO has 80.
3. **Train** on your data with a small learning rate. The backbone changes
   only a little while the new head learns the new classes.
4. Optionally **freeze** the first layers, meaning you stop training them.
   Their edge and color filters, the ones the lecture showed, already work
   on any image, CARLA included.

.. important::

   Fine-tuning needs far less data than training from scratch: a few
   thousand of your own images, not COCO's 118,287 training images. The
   expensive general learning is already done.

Check: CNN Fundamentals
~~~~~~~~~~~~~~~~~~~~~~~

Answer each one on your own before opening the answers.

1. A layer takes 64 channels to 128 with :math:`3 \times 3` filters. How many
   weights?
2. A :math:`3 \times 3` convolution, stride 2, padding 1, on a map 320 high.
   What is the output height?
3. Why is a stack of layers with no activation no better than one layer?
4. The training loss falls and the validation loss rises. What is
   happening, and what do you try?

.. dropdown:: Check: CNN fundamentals. Answers
   :color: success
   :icon: check-circle

   1. :math:`3 \times 3 \times 64 \times 128 =` **73,728**.
   2. :math:`320 + 2 - 3 = 319`. Divided by 2 that is 159.5, rounded down
      159. Plus one: **160**.
   3. **Weighted sums of weighted sums are still one weighted sum.**
   4. **Overfitting.** Try more data or augmentation, fewer epochs, or a
      smaller model, chosen on the validation set.


Decoding a YOLO Cell
--------------------

This section continues **One-Stage Detectors** in the
:doc:`lecture <l4_lecture>`. There, one run of YOLOv8s gave every grid cell
its 80 class scores and 4 distances at once, and the cell at column 3, row
13 of the stride-32 grid drew the man's box. Here we decode that cell by
hand, with the measured values.

Decoding One Cell Into the Man's Box, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cell is not the one that holds the center of his box. It is one of the
about ten cells trained to predict him, and it scored highest.

For each side of the box, the head gives 16 raw scores, one per possible
distance from 0 to 15 strides. A **softmax** turns them into 16
probabilities that are positive and add to 1. The distance is their weighted
average.

.. figure:: /_static/images/L4/dfl_bins.png
   :alt: A bar chart of probability against the top-side distance, in strides of 32 pixels, for distances 0 to 15. Almost all the probability is in one bar at 6, about 0.92, with a small bar at 7 and a smaller one at 5. A dashed orange line at 6.058 is labeled weighted average 6.058.
   :width: 55%
   :align: center

   The top side of the man's box: 16 probabilities after the softmax, one
   per distance in strides of 32 pixels. Almost all of it sits at 6, and
   the weighted average is 6.058.

All numbers below are measured. Distances are in input pixels, on the
480-wide image the network saw.

1. **Cell center:** :math:`(3.5 \times 32,\ 13.5 \times 32) = (112, 432)`.
2. **Each side** is the weighted average of its 16 bins. For the top:

   .. math::

      5 \times 0.012 + 6 \times 0.918 + 7 \times 0.069 + \ldots = 6.058

3. **Times the stride, 32:** left :math:`2.576 \to 82.4`, top
   :math:`6.058 \to 193.9`, right :math:`1.028 \to 32.9`, bottom
   :math:`3.200 \to 102.4` pixels.
4. **Corners:** subtract the left and top distances from the center, and add
   the right and bottom ones.

   .. math::

      (112 - 82.4,\ 432 - 193.9) = (29.6,\ 238.1), \qquad
      (112 + 32.9,\ 432 + 102.4) = (144.9,\ 534.4)

5. **Back to the image:** the image is 810 pixels wide and the network saw it
   480 wide, so multiply by :math:`810/480`. That gives his box,
   (49.9, 401.8) to (244.5, 901.8), up to rounding. The same scale turns the
   four distances into the lecture's 139.1, 327.2, 55.5 and 172.8 image
   pixels.
6. **His confidence:** the raw person score is 2.056, and the sigmoid gives

   .. math::

      \frac{1}{1 + e^{-2.056}} = \mathbf{0.887}


AP in Detail
------------

This section continues **Grading a Detector** in the
:doc:`lecture <l4_lecture>`. The lecture computed AP as the exact area under
a precision-recall line. Here are the two steps the COCO evaluation code
(``cocoeval.py`` in the COCO API, https://github.com/cocodataset/cocoapi)
takes instead: first marking each box right or wrong, then turning the
ranked list into one number.

A few terms from the lecture:

- **IoU** (intersection over union): the overlap of two boxes, divided by
  the area they cover together. 1 means the same box; 0 means no overlap.
- A **true positive (TP)** is a box that matches a real object. A **false
  positive (FP)** is a box that matches nothing. A **false negative (FN)** is
  a real object no box found.
- **Precision** is the share of boxes given so far that are right.
  **Recall** is the share of real objects found so far.

AP, Step 1: Which Boxes Are Right, at One IoU Threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AP is computed for **one class** and **one IoU threshold** :math:`t` at a
time. The COCO code matches boxes like this:

1. Sort the detections by confidence, highest first. COCO keeps at most the
   top 100 per image.
2. Go down the list. For each detection, look among the ground-truth boxes
   of its class that are **not yet matched**. Find the one with the highest
   IoU, if that IoU is at least :math:`t`.
3. If one is found, the detection is a **TP**, and that ground-truth box is
   used up. If not, the detection is an **FP**.
4. Ground-truth boxes still unmatched at the end are **FN**.

.. important::

   **The order matters.** The most confident box is matched first. A
   duplicate further down finds its person already taken, so it counts as
   an FP. That is why **NMS** (non-maximum suppression, the clean-up step
   that removes duplicate boxes) matters for the grade.

The threshold changes the answer. The box from the lecture's IoU example
overlaps the truth with IoU 0.574. It is a TP at :math:`t = 0.50` and
:math:`0.55`. At the 8 stricter thresholds it is an FP, and the person it
covers is left unmatched, an FN.

AP, Step 2: From the Ranked List to One Number
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The lecture's example, chosen for the purpose, is one class, person: 3
people in the ground truth and 5 detections, sorted by confidence.

.. list-table::
   :widths: 20 20 30 30
   :header-rows: 1
   :class: compact-table

   * - **Confidence**
     - **Right?**
     - **Precision**
     - **Recall**
   * - 0.95
     - TP
     - 1/1 = 1.00
     - 1/3 = 0.33
   * - 0.90
     - TP
     - 2/2 = 1.00
     - 2/3 = 0.67
   * - 0.80
     - FP
     - 2/3 = 0.67
     - 2/3 = 0.67
   * - 0.60
     - TP
     - 3/4 = 0.75
     - 3/3 = 1.00
   * - 0.40
     - FP
     - 3/5 = 0.60
     - 3/3 = 1.00

With every detection marked right or wrong, COCO does three things.

1. After each detection in the ranked list, compute precision and recall so
   far. That is the table above.
2. Make precision never rise as recall grows: at each recall, take the best
   precision at that recall or beyond. This is the blue step line on the
   lecture's AP slide.
3. Read that line at **101 recalls**, 0, 0.01, ..., 1.00, and average the 101
   values. A recall the detector never reaches counts as 0. If the detector
   finds only half the people, say, every point above that recall is 0.

For our person example, step by step:

1. Recalls 0 to 0.66 read precision 1.00: 67 points.
2. Recalls 0.67 to 1.00 read 0.75: 34 points.
3. Average them:

   .. math::

      \text{AP} = \frac{67 \times 1.00 + 34 \times 0.75}{101}
                = \frac{92.5}{101} = \mathbf{0.916}

The exact area from the lecture is 0.917, so the two are almost the same.

.. important::

   **Then mAP:** repeat for every class and every IoU threshold, 0.50 to
   0.95 in steps of 0.05, and average them all. Papers call that average
   COCO's "AP". The lecture calls it mAP at 0.5 to 0.95.


Detectors on an AV
------------------

This section widens the lecture's view from our two models to the whole AV.
It builds on **Object Detection** in the :doc:`lecture <l4_lecture>`, which
asks which approaches AVs use, and ends with the model sizes behind the time
budget in **Detection on the Road**.

Detection Approaches on an AV, by Sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is no single AV detector. The approach follows the sensor, and an AV
usually runs several at once.

.. figure:: /_static/images/L4/approaches.png
   :alt: The AV seen from above, front up, in the middle, inside a dashed orange circle labeled LiDAR. A blue cone ahead of it is the front camera; five gray-blue cones around it are labeled cameras around the AV. Left, under the heading 2D boxes, in pixels, from one camera, two blue cards fed by the front camera: One-stage CNN, YOLOv8, YOLO26, one pass, a box from every grid cell, then a clean-up; and Set prediction, RT-DETR, RF-DETR, one box per object, no clean-up; both tagged today. Right, under the heading 3D boxes, in meters: an orange card fed by the LiDAR, LiDAR seen from above, PointPillars, CenterPoint; a blue card fed by the cameras, Cameras around the AV, bird's-eye view, BEVFormer; and a double-edged card fed by both, Camera plus LiDAR fusion; each tagged L5. Below a dashed line separating on the AV from not on the AV, offline: a gray card, Any camera, open vocabulary, Grounding DINO, SAM 3, boxes and masks for a typed phrase, used to label data and find rare objects, tagged reading.
   :width: 95%
   :align: center

   Detectors sorted by sensor. Left: 2D boxes in pixels from one camera,
   today's lecture. Right: 3D boxes in meters from LiDAR, from cameras
   around the AV, or from both, in L5. Bottom: offline, open-vocabulary
   models that do not run on the AV.

- **From one camera**, two families give 2D boxes in pixels.

  - **One-stage CNNs**, the kind built in the lecture: the YOLO line, up to
    YOLO26 from this year. One pass of the network gives a box from every
    grid cell, and a clean-up keeps one box per object.
  - **Set prediction with transformers**: RT-DETR and the newer RF-DETR.
    They give one box per object, with nothing to clean up.

  The lecture uses one model of each.
- **From LiDAR**, detectors look at the scene from above and give 3D boxes
  in meters: PointPillars and CenterPoint, in L5.
- **From several cameras around the AV**, current stacks build one view from
  above, the **bird's-eye view**, and detect on it. BEVFormer is the
  example. **Camera and LiDAR fusion** combines both sensors. Both are in
  L5.
- **Offline**, open-vocabulary models such as Grounding DINO and SAM 3 find
  objects from a typed phrase, not only from a fixed list of classes. They
  label data and hunt for rare objects. The reading slide "Objects outside
  the 80 classes", in the lecture's Detection on the Road section, covers
  them.

AV Sensor and Detector Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Companies do not publish the detectors running in their AVs. They do
publish their sensors, and the sensors decide which detectors can run at
all. The drawing reads top to bottom: sensors in, then detectors, then what
comes out.

.. figure:: /_static/images/L4/waymo_tesla_mobileye.jpeg
   :alt: A pencil-sketch infographic on grid paper. Banner: companies do not publish onboard detectors; they publish their sensors, and sensors decide detectors. Three columns, each with three rows labeled input (sensors), processing (detectors) and compute and report (outcome). Waymo, 6th gen: an SUV with roof sensors labeled 13 cameras, 4 LiDAR and 6 radar; a camera 2D detector and a LiDAR 3D detector, with the radar, feed a sensor fusion engine; the outcome is a street scene with cars, a pedestrian and signs, captioned cohesive environment model (fused). Tesla, Vision Autopilot: a sedan labeled Tesla Vision, camera-based system, camera array, no radar since 2021 and no ultrasonics since 2022; a box reading camera detectors only; the outcome is a bird's-eye view with boxes around the Tesla, captioned 3D from cameras (L5). Mobileye, True Redundancy: a minivan with branches cameras alone (e.g., L2+) and radar or LiDAR alone (e.g., L4+); stack 1, camera detection, and stack 2, radar and LiDAR detection, lead to a redundant safe path determination; the outcome is two kinematics reports, one per stack, captioned two complete, independent sensor and detector systems.
   :width: 100%
   :align: center

   Three published sensor strategies and the detectors they allow. Sources:
   `Waymo blog, August 2024
   <https://waymo.com/blog/2024/08/meet-the-6th-generation-waymo-driver/>`_;
   `Tesla, "Transitioning to Tesla Vision"
   <https://www.tesla.com/support/transitioning-tesla-vision>`_;
   `Mobileye, True Redundancy
   <https://www.mobileye.com/technology/true-redundancy/>`_.

- **Waymo's sixth-generation driver**, in Waymo's words, has 13 cameras, 4
  lidar and 6 radar. So it can run camera detectors for 2D boxes and LiDAR
  detectors for 3D boxes side by side, and fuse them, with the radar, into
  one model of the scene.
- **Tesla** went the other way. Its support page calls its camera-based
  Autopilot system **Tesla Vision**. Radar was removed from new Model 3 and
  Model Y in 2021, and ultrasonic sensors in 2022. So everything is camera
  detection, and the 3D has to come from cameras, with the bird's-eye-view
  methods of L5.
- **Mobileye** calls its approach **True Redundancy**: one complete system
  that can drive on cameras alone, and a second that can drive on radar and
  lidar alone. So it runs two independent detection stacks, each with its
  own output.

Lecture 2 compares these sensor suites in detail.

YOLO Sizes: Accuracy Against Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

YOLO comes in several sizes, and on an AV the size decides the speed. The
table is from the `Ultralytics YOLO26 page
<https://docs.ultralytics.com/models/yolo26/>`_. YOLO26 is Ultralytics'
newest model family, released in January 2026.

.. list-table::
   :widths: 22 26 22 30
   :header-rows: 1
   :class: compact-table

   * - **YOLO26**
     - **mAP@0.5:0.95**
     - **Weights**
     - **Time, T4 TensorRT**
   * - n (nano)
     - 40.9
     - 2.4 M
     - 1.7 ms
   * - s (small)
     - 48.6
     - 9.5 M
     - 2.5 ms
   * - m
     - 53.1
     - 20.4 M
     - 4.7 ms
   * - l (large)
     - 55.0
     - 24.8 M
     - 6.2 ms
   * - x
     - 57.5
     - 55.7 M
     - 11.8 ms

The scores are on the COCO validation images, at 640 input. The time is per
image on an NVIDIA T4 GPU with **TensorRT**, NVIDIA's speed-up library. For
comparison, our YOLOv8s, from 2023, scores 44.9. YOLO26s, about the same
size, scores 48.6.

Read the table the way an AV engineer would.

1. From nano to extra large, mAP gains :math:`57.5 - 40.9 = 16.6` points.
2. The time grows :math:`11.8 / 1.7 = 6.9` times.

.. important::

   **Pick the size by your time budget.** On an AV the time budget comes
   first: pick the biggest model that fits it.

YOLO26 also changes two things from YOLOv8s's head.

- **It has no NMS.** A one-to-one head gives at most 300 boxes, one per
  object. That idea comes from the transformer detectors in the lecture's
  Transformers section.
- **It drops the 16 bins per side** that `Decoding a YOLO Cell`_ walks
  through.

The one-stage and the transformer families are borrowing from each other.


More on Transformers
--------------------

This section continues **Transformers** in the :doc:`lecture <l4_lecture>`,
its Encoder part: step 2, embedding, and step 5, attention. A **token** is
one item the transformer reads: a word in a sentence, or a patch of the
image. The lecture uses one sentence throughout that section, "The boat
reached the bank", and both subsections end with it.

Embedding: King Minus Man Plus Woman
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the lecture, the learned matrix :math:`E` turns each image patch into a
vector. Why add and subtract such vectors at all? To show that a learned
vector is not an arbitrary code. Its numbers hold what the thing stands for,
so arithmetic on them means something. Subtracting two vectors keeps what
differs between them. Adding that difference to another vector carries it
over. Attention (step 5) compares tokens by multiplying their numbers and
adding, which only works because the numbers mean something.

The clearest example comes from words. Each word gets **2 numbers**, chosen
for this example so we can draw them: the first says how royal, the second
how male.

.. figure:: /_static/images/L4/word2vec_toy.png
   :alt: A plot, not a picture of space. The horizontal axis is the first number, how royal, from 0 to 1; the vertical axis is the second number, how male. Man at (0.1, 0.8) and King at (0.9, 0.8) are blue points, joined by an orange arrow labeled King minus Man equals (0.8, 0). Woman at (0.1, 0.1) and Queen at (0.9, 0.1) are green points, joined by the same orange arrow, labeled plus the same arrow.
   :width: 55%
   :align: center

   A plot of two numbers per word, not a map of anything. The arrow from Man
   to King is the same arrow as from Woman to Queen.

1. King is royal and male, (0.9, 0.8). Man is male but not royal,
   (0.1, 0.8). Subtract:

   .. math::

      \text{King} - \text{Man} = (0.9 - 0.1,\ 0.8 - 0.8) = (0.8,\ 0)

   What is left is "royal", with the male part taken out.
2. Add Woman, (0.1, 0.1): :math:`(0.8 + 0.1,\ 0 + 0.1) = (0.9,\ 0.1)`.
3. That is **Queen**.

.. important::

   **In word2vec** (Mikolov et al., 2013), the vectors have hundreds of
   numbers, none of them named royal or male. Training set them all from
   which words appear near which. And still, the paper reports, King minus
   Man plus Woman lands nearest Queen.

**In our sentence:** "boat" sits near "ship" in word2vec because the two
words are used the same way. :math:`E` is simpler: one matrix, so patches
whose pixels look alike get vectors that are alike, wherever they sit in the
image. We measured this on our image with torchvision's ViT-B/16, using
**cosine similarity**, where 1 means the two vectors point the same way.
Two light patches 13 cells apart score 0.844. Two side-by-side patches, one
light and one dark, score -0.47. Closeness in meaning comes later, from the
encoder.

Close By or the Whole Picture: CNN and Transformer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main difference between a CNN and a transformer is how much of the
image one layer can read. One CNN layer reads only the cells **close by**.
One transformer layer reads the **whole picture**.

.. figure:: /_static/images/L4/local_global.png
   :alt: Our bus image twice, each with the stride-32 grid of 15 by 20 cells and the man's cell, on his leg, as an orange square. Left, titled Convolution, a 3 x 3 window: the 3 by 3 block of cells around his cell is shaded blue, with short white arrows from the 8 neighbors toward it. Right, titled Attention, all 300 cells: thin orange lines run from every cell of the grid into his cell.
   :width: 90%
   :align: center

   The same stride-32 grid, 300 cells, with the man's cell in orange. Left:
   one :math:`3 \times 3` convolution reads his cell and its 8 neighbors.
   Right: one attention layer reads all 300 cells. The lines are all drawn
   alike: they show which cells are read, not how much each one counts.

- **Left, a CNN.** One :math:`3 \times 3` convolution reads his cell and its
  8 neighbors, nothing else. To connect him with the bus on the other side,
  information has to hop across many layers.
- **Right, a transformer.** One attention layer reads all 300 cells. How
  much each cell counts is computed for each image. The lecture's
  "Attention by hand" slides compute some of those weights.

In the table, :math:`N` is the number of cells (tokens).

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **CNN**
     - **Transformer**
   * - One layer reads
     - :math:`3 \times 3` cells
     - All cells
   * - Weights
     - One filter for all cells
     - Computed per image
   * - Cost
     - Grows with :math:`N`
     - Grows with :math:`N^2`
   * - Needs
     - Less data
     - More data
   * - Our models
     - YOLOv8s
     - RT-DETR-L, after a CNN

A CNN reads a small window with the same filter everywhere. Its cost grows
in step with the number of cells, and it learns from less data. A
transformer reads every token, with weights computed from the image itself.
Its cost grows with the square of the number of tokens, and it needs more
data. RT-DETR-L uses both: a CNN backbone, then a transformer.

**In our sentence:** a 3-word window on "bank" holds only "the bank". It
takes three layers of such windows before "boat" reaches it. One attention
layer links "bank" and "boat" at once. The catch: comparing every word with
every word costs more as the sentence grows.


Sources for This Page
---------------------

The full reading list for the lecture is in :doc:`l4_references`. This page
cites:

- Krizhevsky, A., Sutskever, I. and Hinton, G. E. (2012). *ImageNet
  Classification with Deep Convolutional Neural Networks.* NeurIPS.
- Simonyan, K. and Zisserman, A. (2015). *Very Deep Convolutional Networks
  for Large-Scale Image Recognition.* ICLR.
- He, K. et al. (2016). *Deep Residual Learning for Image Recognition.*
  CVPR.
- Dosovitskiy, A. et al. (2021). `An Image is Worth 16x16 Words:
  Transformers for Image Recognition at Scale
  <https://arxiv.org/abs/2010.11929>`_. ICLR.
- Mikolov, T., Chen, K., Corrado, G. and Dean, J. (2013). `Efficient
  Estimation of Word Representations in Vector Space
  <https://arxiv.org/abs/1301.3781>`_. arXiv:1301.3781.
- COCO Consortium. `COCO API: pycocotools/cocoeval.py
  <https://github.com/cocodataset/cocoapi>`_.
- Ultralytics. `Ultralytics documentation <https://docs.ultralytics.com/>`_:
  YOLOv8, YOLO26 and RT-DETR model pages.
