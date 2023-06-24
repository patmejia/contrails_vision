Title:
# GOES16 Contrail Detection with Computer Vision

Description:

Harnessing machine learning and computer vision techniques, this project discerns contrails within GOES-16 satellite data, thereby supplying critical knowledge for climate change studies and global warming countermeasures. It exemplifies the conversion of intricate satellite data into data-driven, impactful environmental solutions.

<br>Contrails are thermodynamically formed condensation trails.

<br>High-temperature, high-humidity exhaust from aircraft engines undergoes adiabatic cooling and condensation upon encountering colder, drier air at cruising altitudes.

<br>This adiabatic process forms visible ice-crystal trails.

<br>These trails can persist for hours or days, depending on atmospheric conditions.

<br>Contrails contribute to the greenhouse effect by trapping heat in the atmosphere.

<br>Contrails introduce uncertainty in climate models due to prediction and modeling difficulties.

<br>Detecting and tracking contrails is essential for understanding their climate change impact and devising mitigation strategies.

```mermaid
graph TD
  A[Start]
  A --> B{Dark?}
  B --> |No| C1[Not a contrail]
  B --> |Yes| D{Line-shaped?}
  D --> |No| E1[Not a contrail]
  D --> |Yes| F{Appears suddenly or from sides?}
  F --> |No| G1[Not a contrail]
  F --> |Yes| H{Visible in 2+ images?}
  H --> |No| I1[Not a contrail]
  H --> |Yes| J{10+ pixels, 3x longer \n than wide at least once?}
  J --> |No| K1[Not a contrail]
  J --> |Yes| L{Moves with wind?}
  L --> |No| M1[Not a contrail]
  L --> |Yes| N{Spreads quickly?}
  N --> |No| O1[Not a contrail]
  N --> |Yes| P{Flight path reference?}
  P --> |No| Q1[Contrail, >90% confidence]
  P --> |Yes| R[Contrail, 60% confidence]
```

## process of identifying a contrail:

- Darkness of the object: <br>Contrails are calibrated to appear darker than their surroundings in the image.

- Linearity of the object: <br>Contrails are line-shaped clouds produced by aircraft engines.

- Object appearance: <br>Does the object appear suddenly or enter from the sides of the image? Contrails are formed by planes moving at high speeds, so they appear quickly in the image.

- Object visibility: <br>Is the object visible in at least two images? As contrails are created by moving airplanes, they should be visible across multiple frames.

- Size and shape of the object: <br>Does the object contain at least 10 pixels and has it been at least three times longer than its width at some point? This is a unique characteristic of contrails due to their shape and formation.

- Object movement: <br>Does the object move with time due to wind? Contrails, being high in the atmosphere, will be influenced by wind, causing them to move and change shape over time.


## further considerations increasing confidence in contrail identification:


- Contrail Aging and Dissipation: <br> Over time, contrails spread and dissipate, becoming more diffuse. This might be another feature to consider. If an object starts very sharp and becomes gradually wider over time, it is likely a contrail.

- Contrail Color: <br> Although contrails are dark in infrared images, their color can vary in other types of images depending on the position of the sun and the altitude of the aircraft. This could provide additional information for contrail detection.

- Flight Path Alignment: <br> If possible, aligning the observed contrails with known flight paths could greatly increase the confidence of contrail identification.

- Cloud Shadows: <br> These can sometimes look like contrails. Shadows will usually be aligned with the sun's position and may not exhibit the same behavior as contrails in a sequence of images.

- Cloud Streets: <br> These are rows of cumulus clouds that could potentially be mistaken for contrails. However, they are typically wider, not as straight as contrails, and don't have the sudden appearance and dissipation behavior of contrails.
 
- Jet Stream Impact: <br> Contrails are affected by high altitude winds. Observing the direction and speed of wind aloft can help distinguish contrails from other linear objects.

- Consistency Across Different Wavelengths: <br> If multi-spectral images are available, a consistent appearance across different wavelengths could further support the identification of a contrail. 

- The detection algorithm should also consider objects that behave similarly to contrails and use additional rules or machine learning techniques to differentiate them:
    > Cloud shadows and cloud streets can sometimes mimic contrails. Cloud shadows will usually be aligned with the sun's position and may not exhibit the same behavior as contrails in a sequence of images. 
    >
    > Cloud streets are rows of cumulus clouds that could potentially be mistaken for contrails. However, they are typically wider, not as straight as contrails, and don't have the sudden appearance and dissipation behavior of contrails.  

## updated decision tree:

```mermaid
graph TD;
    A[Start]
    A --> B{Dark?}
    B --> |No| C[Not Dark]
    B --> |Yes| D{Linear?}
    D --> |No| E[Not Linear]
    D --> |Yes| F{Sudden Appearance or from Sides?}
    F --> |No| G[Stable Appearance]
    F --> |Yes| H{Visible in 2+ Images?}
    H --> |No| I[Single Image]
    H --> |Yes| J{Meets Size/Shape Criteria?}
    J --> |No| K[Incorrect Size/Shape]
    J --> |Yes| L{Moves with Wind?}
    L --> |No| M[Static]
    L --> |Yes| N{Spreads Over Time?}
    N --> |No| O{Potential Shadow?}
    O --> |Yes| P[Cloud Shadow]
    O --> |No| Q{Cloud Street Traits?}
    Q --> |Yes| R[Cloud Street]
    Q --> |No| S{Consistent Across Wavelengths?}
    S --> |No| T[Wavelength Inconsistency]
    S --> |Yes| U{Flight Path Reference?}
    U --> |No| V[Contrail >90% Confidence]
    U --> |Yes| W[Contrail 60% Confidence]
```

## Acknowledgements:

arxiv: https://arxiv.org/abs/2304.02122

contrails-labeling-guide: https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf

challenge-guide: https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-gobal-warming/data

high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds

visualize (input dataset 450.91 GB): https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation

GOES-16 (Geostationary Operational Environmental Satellite, Launch Date: Nov. 19, 2016): https://eospso.nasa.gov/missions/geostationary-operational-environmental-satellite-16

contrails dataset sample (11.74 GB) train_df.csv, valid_df.csv: https://www.kaggle.com/datasets/shashwatraman/contrails-images-ash-color