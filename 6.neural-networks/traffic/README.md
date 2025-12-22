### Architecture

My neural network uses a convolutional neural network (CNN) architecture optimized for traffic sign recognition:

1. **Convolutional Layers**: Three convolutional layers with 32, 64, and 128 filters respectively, each using 3x3 kernels and ReLU activation. These layers progressively extract more complex features from the images.

2. **Pooling Layers**: Max pooling layers (2x2) after each convolutional layer to reduce dimensionality and computational cost while preserving important features.

3. **Dense Layers**: Two fully connected layers (256 and 128 units) with ReLU activation, each followed by dropout layers (0.5 and 0.3 respectively) to prevent overfitting.

4. **Output Layer**: A dense layer with 43 units (one for each traffic sign category) using softmax activation for multi-class classification.

### Key Improvements

The model achieved high accuracy through several important improvements:

1. **Image Normalization**: Normalized pixel values from 0-255 range to 0-1 range by dividing by 255.0. This is critical for neural networks to learn effectively.

2. **Enhanced Architecture**:

   - Added a third convolutional layer (128 filters) for better feature extraction
   - Increased the first dense layer to 256 units
   - Added a second dense layer (128 units) with dropout

3. **Proper Data Preprocessing**: Ensured all images are resized to 30x30 pixels and normalized before training.

### Evaluation Metrics

**Final Model Performance:**

- **Test Accuracy**: 97.23% (0.9723)
- **Test Loss**: 0.1063
- **Training Epochs**: 10
- **Test Split**: 40% of the dataset

The model demonstrates excellent performance on the German Traffic Sign Recognition Benchmark (GTSRB) dataset, successfully classifying 43 different types of traffic signs with high accuracy.

### Experimentation Notes

During development, I experimented with:

- **More convolutional layers**: Added a third Conv2D layer which improved feature extraction
- **More filters**: Increased filter counts (32 → 64 → 128) in deeper layers
- **Additional dense layers**: Added a second dense layer which improved classification performance
- **Dropout rates**: Used different dropout rates (0.5 and 0.3) to balance overfitting prevention
- **Image normalization**: This was the most critical fix - normalizing pixel values from 0-255 to 0-1 range dramatically improved accuracy from ~5% to 97%

Future improvements could include:

- Data augmentation (rotation, shifting, flipping) to increase training data diversity
- Different optimizers or learning rate schedules
- Early stopping to prevent overfitting during longer training
