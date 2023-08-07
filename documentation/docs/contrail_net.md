# Implementing Contrail Net for Contrail Detection - OpenContrail
### Neural Network Models: Contrail Detection & Segmentation from Satellite Images

[Fork from @junzis| contrail-net](https://github.com/junzis/contrail-net)

Contrail Net leverages a pre-trained ResUNet model, image augmentations, and SR Loss using Hough space. Demonstrates contrail detection with various models, loss functions, and image sources. Built with PyTorch and includes a visualization notebook.

## Advancements:
- **Augmented Transfer Learning**: Image transformations on pre-trained ResUNet for diverse contrail scenarios.
- **SR Loss**: Merges segmentation and optimization using Hough space.
- **Model & Loss Function Examples**: Contrail detection with ResUNet, Dice Loss, Focal Loss.
- **Image Source Examples**: Contrail detection from GOES-16, Himawari-8, MODIS.


## Image Sources:
Uses GOES-16 channels 13 (10.35 µm) and 15 (12.3 µm) to generate brightness temperature difference (BTD) images, isolating optically thin cirrus clouds and contrails.

| ![channel_13](../images/research/abi_band_13.png) | ![channel_14](../images/research//abi_band_14.png) | ![channel_15](../images/research/abi_band_15.png) |
|:---:|:---:|:---:|
| *ABI Band 13 - 10.3 µms - "Clean" Longwave Window* | *ABI Band 14 - 11.2 µms - Longwave Window* | *ABI Band 15 - 12.3 µms - "Dirty" Longwave Window - Water Vapor Absorption* |


## References:
- [Flight Contrail Segmentation with SR Loss in Hough Space](https://arxiv.org/pdf/2307.12032.pdf)
- [ABI Band 13 - 10.3 µms](http://cimss.ssec.wisc.edu/goes/OCLOFactSheetPDFs/ABIQuickGuide_Band13.pdf)
- [Split Window Difference](http://cimss.ssec.wisc.edu/goes/OCLOFactSheetPDFs/ABIQuickGuide_SplitWindowDifference.pdf)

## Data Augmentation:
1. **Random Transformations**: Applied to original image and contrail mask.
2. **Padding/Cropping**: Transformed image and mask adjusted to a consistent pixel size (multiple of 32 pixels).
3. **Brightness & Contrast Adjustments**: Random changes to padded image; mask remains unchanged.

## Split Window Difference (SWD):
Brightness temperature difference field highlighting low-level moisture and dust. Calculated by subtracting the 12.3 µm channel from the 10.3 µm channel. Identifies moisture gradients and detects atmospheric moistening, influencing convection and precipitation. Limitations include susceptibility to temperature or water vapor changes and reduced post-sunrise effectiveness.

---

# Feature Engineering Ideas for Contrail Detection


## Dataset Adjustments:
- **Band Selection**:
  - For a simplified approach, modify the dataset class to read from `band_13` to `band_16` (4 bands).
  - Adjust the U-Net `in_channels` to 4 to match the number of bands used.
  - Switch to the aggregated ground truth masks (`human_pixel_masks.npy`) for training.

## Temporal Sequence Handling:
- Consider using a **Recurrent Neural Network (RNN)** or **LSTM layers** after feature extraction to capture temporal dependencies in the sequences.
- Explore **3D convolutions**, treating the temporal sequence as a depth dimension.
- Implement an **attention mechanism** to focus on specific frames in the sequence that might be more informative.

## Band Selection:
- Utilize domain knowledge or feature importance techniques to select the most informative bands for contrail detection.
- Experiment with different combinations of bands to determine the optimal performance.

## Augmentation Strategies:
- Given the temporal nature of the data, consider temporal augmentations such as:
  - Frame shuffling
  - Frame skipping
  - Frame reversing
- Apply traditional image augmentations:
  - Rotations
  - Flips
  - Brightness and contrast adjustments

## Incorporate Metadata:
- If additional metadata (e.g., time of day, weather conditions) is available, incorporate it as additional input features.

## Ensemble Models:
- Train multiple models with varying architectures or on different bands.
- Use ensemble techniques, such as stacking or majority voting, for the final prediction.

## Attention Mechanisms:
- Implement attention mechanisms to focus on specific regions in the image sequence, especially since contrails should be visible in at least two images.

## Use Pre-trained Models:
- Fine-tune pre-trained models for contrail detection.
- Leverage transfer learning, especially if the dataset size is limited.

## Contrail Net Advancements:
- **Augmented Transfer Learning**: Utilize image transformations on a pre-trained ResUNet model to adapt to various contrail scenarios.
- **SR Loss**: Introduce a new loss function that combines segmentation and optimization objectives using Hough space information.
- **Diverse Model Examples**: Showcase contrail detection using various models and loss functions, such as ResUNet, Dice Loss, and Focal Loss.
- **Diverse Image Sources**: Demonstrate contrail detection capabilities using different image sources like GOES-16, Himawari-8, and MODIS.

## Image Sources and Band Information:
- Utilize the brightness temperature difference (BTD) images, which can isolate the presence of optically thin cirrus clouds and contrails from background interference.
- Consider the significance of the "clean" infrared window band (band 13 covering 10.35 µm) and the "dirty" infrared window band (band 15 covering 12.3 µm) in contrail detection.
- Explore the potential of other infrared bands for BTD calculation.

## Split Window Difference (SWD):
- Understand the importance of SWD in highlighting low-level moisture and dust.
- Recognize the benefits of SWD in identifying moisture gradients and detecting atmospheric moistening, which can influence convection and precipitation.
- Be aware of the limitations of SWD, such as its susceptibility to temperature or water vapor changes and reduced effectiveness after sunrise.

## Data Preprocessing

1. **Padding**:
Ensure consistent padding for both images and masks using the following:
```python
Lambda(lambda x: pad(x, (0, 0, 0, (32 - x.shape[1] % 32) % 32)))
```

2. **Transpose Ground Truth Tensor**:
To match the shape of the input image tensor, adjust the dimensions of the ground truth tensor:
```python
if target_tensor.ndim == 4:
  target_tensor = np.transpose(target_tensor, (0, 3, 1, 2))
elif target_tensor.ndim == 3:
  target_tensor = np.transpose(target_tensor, (2, 0, 1))
```

3. **Resize Ground Truth Tensor**:
Ensure the ground truth tensor has the desired shape:
```python
target_tensor = resize(target_tensor, (8, 1, 320, 320), mode='constant', anti_aliasing=False)
```

## Refactored Solution

### Dimension Mismatch in `ContrailDataset`

- Mismatch between `y_hat` (predicted tensor) and `y` (ground truth tensor).
- Issue: `y_hat` has a single channel while `y` contains 256 channels.
- Solution: Adjust the `ContrailDataset` class to make sure `y` also has a single channel.

```python
class ContrailDataset(Dataset):
    # ... [rest of the class]
    
    def __getitem__(self, idx):
        # ... [rest of the function]
        
        target_path = os.path.join(record_dir, 'human_pixel_masks.npy')
        target = np.load(target_path) if os.path.exists(target_path) else None
        
        if target:
            target = np.mean(target, axis=1, keepdims=True)
            target = Resize((320, 320))(target)

        return sample, target
```

### Handling Issues in `ContrailDataset` 

1. The `Resize` function expects a PIL image or PyTorch tensor, but a numpy array is passed to it after the `np.mean()` operation.
2. Ensure that `target` is two-dimensional and of type `uint8` in the `Image.fromarray` operation.
3. Ensure that the model's output (`y_hat`) and the target tensor (`y`) have the same spatial dimensions by updating the resizing operation within the `ContrailDataset` class.
4. Ensure that the target tensor's shape matches the channel dimension of the predicted tensor by adding an extra dimension.

```python
class ContrailDataset(Dataset):
    # ... [rest of the class]
    
    def __getitem__(self, idx):
        # ... [rest of the function]
        
        sample = torch.tensor(sample, dtype=torch.float32)
        if target:
            target = torch.tensor(target_resized, dtype=torch.float32).unsqueeze(0)

        return sample, target
```

### Ensuring Appropriate Model's Output for BCE

To use the binary cross-entropy loss, the model's output should be between 0 and 1. To achieve this, apply the sigmoid activation function to the model's output and clip the values to the desired range.

```python
class ContrailModel(pl.LightningModule):
    # ... [rest of the class]

    def forward(self, x):
        x = self.model(x)
        return self.sigmoid(x).clamp(min=1e-5, max=1-1e-5)
```

### Approach to Resolve the Issues

1. **Code Review**: Thoroughly examine the content of the `contrail-net-vision (5).ipynb` notebook.
2. **Implement Resolutions**: Rectify issues based on the provided error resolutions.
3. **Maintain Consistency**: Make sure the changes are consistent with the related scripts (`detect.ipynb`, `loss.py`, `train.py`, `contrail_tf_keras.py`, `contrail.py`).
4. **Present Corrected Code**: Once modifications are made, present the rectified code.

The `ContrailDataset` class and its __getitem__ method are crucial for loading data with consistent shape and type. Proper transformations and resizing operations should be applied to maintain data integrity.
