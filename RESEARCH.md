# GOES16-satellite-detection
Repository for machine learning-based contrail detection in GOES-16 satellite imagery to combat global warming

```mermaid
graph TD;
  A[Start]
  A --> B{Dark?}
  B --> |No| C1[Result: Not a contrail]
  B --> |Yes| D{Linear?}
  D --> |No| E1[Result: Not a contrail]
  D --> |Yes| F{Appear suddenly or \n from sides?}
  F --> |No| G1[Result: Not a contrail]
  F --> |Yes| H{Visible in \n 2 or more images?}
  H --> |No| I1[Result: Not a contrail]
  H --> |Yes| J{Has 10+ pixels and \n 3x longer than wide \n at least once?}
  J --> |No| K1[Result: Not a contrail]
  J --> |Yes| L{Moves with \n wind over time?}
  L --> |No| M1[Result: Not a contrail]
  L --> |Yes| N[Result: Contrail]
```



## Acknowledgements:
##### https://storage.googleapis.com/goes_contrails_dataset/20230419/Contrail_Detection_Dataset_Instruction.pdf
##### https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/data
##### high-score-example: https://www.kaggle.com/code/egortrushin/gr-icrgw-training-with-4-folds
##### visualize: https://www.kaggle.com/code/inversion/visualizing-contrails#OpenContrails-dataset-documentation