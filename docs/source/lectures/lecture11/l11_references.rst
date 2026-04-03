References
==========


.. dropdown:: Lecture 10
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818Z -- L10: Prediction & Decision-Making**

        Covers why prediction is necessary for planning (horizon
        requirements), physics-based prediction (CV, CTRA),
        maneuver-based prediction (intent classification + conditional
        model), interaction-aware prediction (Social Force, GNNs),
        Transformer-based prediction (MotionTransformer, scene
        context encoding, multi-modal output), multi-modal prediction
        metrics (MinADE, MinFDE, MissRate, mAP), FSM behavior
        planning (states, transitions, limitations), rule-based vs.
        learned decision-making, behavior cloning (distribution shift,
        compounding errors), and DAgger (dataset aggregation, expert
        querying, convergence guarantees).


.. dropdown:: Trajectory Prediction
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Schubert et al. -- CTRA Model (2008)
            :class-card: sd-border-secondary

            **IEEE IV 2008**

            Analysis and comparison of constant-motion kinematic
            models (CV, CA, CTRA, CTRV) for vehicle trajectory
            prediction with empirical accuracy benchmarks.

            +++

            - CTRA derivation
            - Model comparison
            - Short-horizon accuracy

        .. grid-item-card:: Helbing & Molnar -- Social Force (1995)
            :class-card: sd-border-secondary

            **Physical Review E, 1995**

            Seminal social force model for pedestrian dynamics,
            modelling attraction toward goals and repulsion from
            obstacles and other pedestrians.

            +++

            - Force model formulation
            - Crowd dynamics simulation
            - Parameter estimation

        .. grid-item-card:: Alahi et al. -- Social LSTM (CVPR 2016)
            :class-card: sd-border-secondary

            **CVPR 2016**

            Introduced the social pooling mechanism to LSTM-based
            pedestrian trajectory prediction, enabling interaction-
            aware learning.

            +++

            - LSTM trajectory prediction
            - Social pooling
            - ETH/UCY benchmark results

        .. grid-item-card:: Gupta et al. -- Social GAN (CVPR 2018)
            :class-card: sd-border-secondary

            **CVPR 2018**

            Generative adversarial network for multi-modal
            pedestrian trajectory prediction with socially
            acceptable samples.

            +++

            - GAN-based multi-modal prediction
            - Variety loss
            - Social acceptability


.. dropdown:: Transformer-Based Prediction
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Shi et al. -- MotionTransformer (NeurIPS 2023)
            :class-card: sd-border-secondary

            **NeurIPS 2023**

            State-of-the-art Transformer predictor with two-stage
            global + local motion Transformers and learnable motion
            query pairs for multi-modal prediction on WOMD.

            +++

            - Two-stage Transformer architecture
            - Factorized attention
            - WOMD state-of-the-art results

        .. grid-item-card:: Nayakanti et al. -- Wayformer (ICRA 2023)
            :class-card: sd-border-secondary

            **ICRA 2023**

            Waymo's Transformer-based prediction model with
            efficient factorized attention for joint agent and
            map encoding.

            +++

            - Factorized attention design
            - Scalability analysis
            - Real-time inference

        .. grid-item-card:: Ngiam et al. -- Scene Transformer (ICLR 2022)
            :class-card: sd-border-secondary

            **ICLR 2022**

            Joint prediction of all agents in a scene using a
            single Transformer, enabling fully interaction-aware
            prediction.

            +++

            - Joint multi-agent prediction
            - Factored attention masks
            - nuScenes and WOMD results

        .. grid-item-card:: Shi et al. -- MTR++ (T-PAMI 2024)
            :class-card: sd-border-secondary

            **IEEE T-PAMI 2024**

            Extension of MotionTransformer with improved scene
            encoding and multi-agent prediction, achieving SOTA
            across multiple benchmarks.

            +++

            - Extended architecture
            - Multi-dataset training
            - Benchmark leaderboard


.. dropdown:: Behavior Planning
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Paden et al. -- AV Planning Survey (IEEE T-ITS 2016)
            :class-card: sd-border-secondary

            **IEEE T-ITS, 2016**

            Survey of behavior planning approaches including FSMs,
            POMDP, and rule-based methods for autonomous vehicles.

            +++

            - FSM design patterns
            - POMDP formulation
            - Rule-based systems

        .. grid-item-card:: Ulbrich & Maurer -- MOMDP for Behavior (IV 2013)
            :class-card: sd-border-secondary

            **IV 2013**

            Models behavior planning as a Mixed Observability MDP,
            enabling principled uncertainty handling beyond FSMs.

            +++

            - MOMDP formulation
            - Belief-space planning
            - Intersection scenarios

        .. grid-item-card:: Brechtel et al. -- Probabilistic MDP (ITSC 2014)
            :class-card: sd-border-secondary

            **ITSC 2014**

            Probabilistic behavior planning under prediction
            uncertainty using continuous-state MDP.

            +++

            - MDP with probabilistic transitions
            - Integration with prediction
            - Risk-aware planning

        .. grid-item-card:: Werber et al. -- Rule Book (IV 2019)
            :class-card: sd-border-secondary

            **IV 2019**

            Formalization of traffic rules as a hierarchically
            ordered rule book for certifiable behavior planning.

            +++

            - Rule formalization
            - Hierarchical priority
            - Verification


.. dropdown:: Imitation Learning and DAgger
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Ross & Bagnell -- Behavior Cloning (2010)
            :class-card: sd-border-secondary

            **JMLR Workshop, 2010**

            Analysis of distribution shift in behavior cloning with
            the formal :math:`O(\epsilon T^2)` error bound derivation.

            +++

            - Distribution shift analysis
            - Compounding error bound
            - Theoretical foundations

        .. grid-item-card:: Ross, Gordon & Bagnell -- DAgger (AISTATS 2011)
            :class-card: sd-border-secondary

            **AISTATS 2011**

            Original DAgger paper introducing the dataset aggregation
            algorithm with formal reduction from :math:`O(\epsilon T^2)`
            to :math:`O(\epsilon T)` regret.

            +++

            - DAgger algorithm
            - Convergence guarantees
            - No-regret analysis

        .. grid-item-card:: Codevilla et al. -- CILRS (ICCV 2019)
            :class-card: sd-border-secondary

            **ICCV 2019**

            Conditional imitation learning with reinforcement
            learning for robust urban driving, addressing
            distribution shift via hybrid IL+RL training.

            +++

            - Conditional command inputs
            - IL + RL hybrid
            - CARLA benchmark results

        .. grid-item-card:: Chen et al. -- TransFuser (CVPR 2021)
            :class-card: sd-border-secondary

            **CVPR 2021**

            Transformer-based imitation learning agent fusing
            camera and LiDAR via cross-attention for CARLA
            Leaderboard challenge.

            +++

            - Sensor fusion via attention
            - End-to-end imitation
            - Leaderboard benchmark


.. dropdown:: Datasets and Benchmarks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Waymo Open Motion Dataset (WOMD)
            :link: https://waymo.com/open/data/motion/
            :class-card: sd-border-secondary

            **Waymo Open Dataset**

            Large-scale real-world prediction benchmark with 570 hours
            of driving data across diverse scenarios. Standard benchmark
            for MotionTransformer and similar models.

            +++

            - Agent trajectory annotations
            - HD map with road graph
            - Prediction challenge leaderboard

        .. grid-item-card:: nuScenes Prediction
            :link: https://www.nuscenes.org/prediction
            :class-card: sd-border-secondary

            **nuScenes (Motional)**

            360-degree sensor suite dataset with prediction challenge
            and standardized MinADE/MinFDE/MissRate metrics.

            +++

            - Multi-sensor annotations
            - Prediction challenge
            - MinADE/MinFDE baseline results

        .. grid-item-card:: ETH/UCY Pedestrian Datasets
            :link: https://graphics.cs.ucy.ac.cy/research/downloads/crowd-data
            :class-card: sd-border-secondary

            **ETH Zurich / UCY**

            Standard pedestrian trajectory prediction benchmarks
            used to evaluate Social LSTM, Social GAN, and subsequent
            pedestrian prediction models.

            +++

            - Overhead video annotations
            - Multiple crowd scenarios
            - ADE/FDE metrics


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Schmerling et al.
            :class-card: sd-border-secondary

            **Multimodal Probabilistic Model-Based Planning for
            Human-Robot Interaction (ICRA 2018)**

            Unified framework for prediction and planning under
            multi-modal agent behavior uncertainty.

        .. grid-item-card:: Sutton & Barto
            :class-card: sd-border-secondary

            **Reinforcement Learning: An Introduction (2nd Ed.)**

            Comprehensive RL textbook. Chapters 3--6 provide the
            MDP and policy optimization foundations underlying
            learned behavior planners and DAgger.

        .. grid-item-card:: Vaswani et al.
            :class-card: sd-border-secondary

            **Attention Is All You Need (NeurIPS 2017)**

            Original Transformer paper. Essential background for
            understanding MotionTransformer and all Transformer-based
            prediction architectures.

        .. grid-item-card:: Goodfellow, Bengio & Courville
            :class-card: sd-border-secondary

            **Deep Learning (MIT Press, 2016)**

            Chapters 6--10 cover the deep learning foundations
            (MLPs, CNNs, RNNs) underlying LSTM-based and
            Transformer-based prediction models.
