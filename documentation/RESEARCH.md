#### Title:
# GOES16 Advanced Baseline Imager (ABI) 
### Contrail Detection with Computer Vision

#### Description:

#### Harnessing machine learning and computer vision, this project detects contrails in GOES-16 satellite data, supplying critical insights for climate change research and global warming mitigation. Adiabatic processes create visible ice-crystal trails of varying duration, contributing to the greenhouse effect and introducing uncertainty in climate models. Accurate contrail detection and tracking are crucial for understanding their climate change impact and devising effective mitigation strategies.

![Atmospheric-optics-Contrail-shadows](./images/atmospheric-optics-contrail-shadows.png)

---
### Process of identifying a contrail:
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
  N --> |No| O{Potential Shadow?}
  O --> |Yes| P1[Cloud Shadow]
  O --> |No| Q{Cloud Street Traits?}
  Q --> |Yes| R1[Cloud Street]
  Q --> |No| S{Consistent Across Wavelengths?}
  S --> |No| T1[Wavelength Inconsistency]
  S --> |Yes| U{Flight Path Reference?}
  U --> |No| V[Contrail, >90% confidence]
  U --> |Yes| W[Contrail, 60% confidence]

```

#### 1. Darkness of the object: Contrails appear darker than their surroundings in the image.
#### 2. Linearity of the object: Contrails are line-shaped clouds produced by aircraft engines.
#### 3. Object appearance: Contrails appear suddenly or enter from the sides of the image due to planes moving at high speeds.
#### 4. Object visibility: Contrails should be visible in at least two images, as they are created by moving airplanes.
#### 5. Size and shape of the object: Contrails have a length at least three times longer than their width and contain at least 10 pixels.
#### 6. Object movement: Contrails move and change shape over time due to wind influence.
#### 7. Contrail Aging and Dissipation: Contrails spread and become more diffuse over time.
#### 8. Contrail Color: Contrails' color can vary depending on the sun's position and aircraft altitude.
#### 9. Flight Path Alignment: Aligning observed contrails with known flight paths increases confidence in identification.
#### 10. Cloud Shadows: Shadows aligned with the sun's position may resemble contrails but behave differently in a sequence of images.
#### 11. Cloud Streets: Rows of cumulus clouds that are wider, less straight, and have different appearance and dissipation behavior than contrails.
#### 12. Jet Stream Impact: Contrails are influenced by high altitude winds, which can help distinguish them from other linear objects.
#### 13. Consistency Across Different Wavelengths: Consistent appearance across different wavelengths supports contrail identification.
#### 14. Consider similar objects: Cloud shadows and cloud streets can mimic contrails but exhibit different behaviors and characteristics.

---
### Acknowledgements:

#### 📌 arxiv: https://arxiv.org/abs/2304.02122
#### 📌 challenge-guide: https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-gobal-warming/data
#### ☛ Adam Duran (Michigan Tech, Q&A with SATAVIA: Climate and Contrails): https://www.mtu.edu/unscripted/2021/06/qa-with-satavia-climate-and-contrails.html
#### ☛ contrails-labeling-guide: https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf
#### ☛ catalogues of atmospheric optics (rocket plume, contrail shadow): https://atoptics.co.uk/atoptics/shuttle.htm, https://atoptics.co.uk/atoptics/contr1.htm
#### ☛ high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds
#### ☛ visualize (input dataset 450.91 GB): https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation
#### ☛ GOES-16 (Geostationary Operational Environmental Satellite, Launch Date: Nov. 19, 2016): https://eospso.nasa.gov/missions/geostationary-operational-environmental-satellite-16
#### ☛ contrails dataset sample (11.74 GB) train_df.csv, valid_df.csv: https://www.kaggle.com/datasets/shashwatraman/contrails-images-ash-color
