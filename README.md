Title:
# GOES16 Contrail Detection with Computer Vision

Description:

Harnessing machine learning and computer vision techniques, this project discerns contrails within GOES-16 satellite data, thereby supplying critical knowledge for climate change studies and global warming countermeasures. It exemplifies the conversion of intricate satellite data into data-driven, impactful environmental solutions.

## process of identifying a contrail:

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
##### https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf
##### https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/data
##### high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds
##### visualize: https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation
##### https://eospso.nasa.gov/missions/geostationary-operational-environmental-satellite-16