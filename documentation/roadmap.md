# Roadmap for 3D Visualization, Contrail Detection, and Image Segmentation

## PyVista - 3D Visualization & Mesh Analysis
- **Renderer**: Utilize 3D scene rendering tools like `view_isometric()`.
- **Surface Normals**: Compute mesh shading and lighting.
- **Point Clouds**: Techniques for visualizing point clouds.

## Contrail Net - Contrail Detection & Segmentation
- **Pre-trained ResUNet Model**: Leverage for contrail detection.
- **Image Augmentations**: Apply augmentations to enhance model accuracy.
- **SR Loss using Hough Space**: Implement for detection.
- [Fork from @junzis| contrail-net](https://github.com/junzis/contrail-net)

## Image Segmentation Techniques
- **Libraries**: OpenCV, TensorFlow, Keras, PyTorch, Scikit-Image.
- **Feature Extraction**: Techniques like SIFT, SURF, HOG, LBP.
- **Graph-Based Segmentation**: Focus on RAGs (Region Adjacency Graphs).

## Contrail Analysis Roadmap
- **Data Acquisition and Preparation**: Organize and understand data.
- **Data Quality and Integrity**: Perform visual inspection, checks.
- **Model Building**: Implement models for contrail vs. cloud differentiation.
- **Evaluation and Interpretation**: Analyze model results and insights.

## Project To-do's
- ☑︎ Resolve `run.py` and Dataset Incompatibility.
- ○ Revise script for modular data transformation and visualization.
- □ Organize repository branches.
