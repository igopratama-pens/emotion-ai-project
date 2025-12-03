"""
Emotion Recognition Training Script
Custom CNN Architecture with Complete Visualization
"""

import os
import json
import numpy as np
import cv2
from pathlib import Path
from datetime import datetime

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, 
    BatchNormalization, Activation
)
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model

# Visualization & Metrics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_recall_fscore_support
)
from sklearn.model_selection import train_test_split

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    # Paths
    DATASET_ROOT = "data/DATASET"
    MODEL_DIR = "model"
    RESULTS_DIR = "results"
    
    # Model params
    IMG_SIZE = 100
    CHANNELS = 3
    NUM_CLASSES = 7
    
    # Training params
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 0.001
    VALIDATION_SPLIT = 0.25
    
    # Callbacks params
    PATIENCE_EARLY_STOP = 20
    PATIENCE_LR_REDUCE = 5
    MIN_DELTA = 0.001
    
    # Emotion labels
    EMOTIONS = {
        0: 'Surprise',
        1: 'Fear',
        2: 'Disgust',
        3: 'Happiness',
        4: 'Sadness',
        5: 'Anger',
        6: 'Neutral'
    }

# Create directories
os.makedirs(Config.MODEL_DIR, exist_ok=True)
os.makedirs(Config.RESULTS_DIR, exist_ok=True)

# ============================================================================
# DATA LOADING
# ============================================================================

def load_dataset(split='train', verbose=True):
    """
    Load dataset from folder structure
    
    Args:
        split: 'train' or 'test'
        verbose: Print statistics
    
    Returns:
        X: Images array
        Y: Labels array
    """
    data_path = Path(Config.DATASET_ROOT) / split
    
    if not data_path.exists():
        raise ValueError(f"Dataset path not found: {data_path}")
    
    data = []
    class_counts = {i: 0 for i in range(Config.NUM_CLASSES)}
    
    print(f"\n{'='*60}")
    print(f"Loading {split.upper()} Dataset")
    print(f"{'='*60}")
    
    # Load images from each class folder
    for class_idx in range(1, Config.NUM_CLASSES + 1):
        class_path = data_path / str(class_idx)
        
        if not class_path.exists():
            print(f"⚠ Warning: Folder {class_path} not found, skipping...")
            continue
        
        label = class_idx - 1  # Convert to 0-indexed
        
        for img_file in class_path.glob('*'):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                try:
                    # Read and preprocess image
                    img = cv2.imread(str(img_file))
                    if img is not None:
                        img = cv2.resize(img, (Config.IMG_SIZE, Config.IMG_SIZE))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        data.append([img, label])
                        class_counts[label] += 1
                except Exception as e:
                    print(f"Error loading {img_file}: {e}")
    
    # Shuffle data
    np.random.shuffle(data)
    
    # Separate features and labels
    X = np.array([item[0] for item in data])
    Y = np.array([item[1] for item in data])
    
    # Normalize
    X = X.astype('float32') / 255.0
    
    if verbose:
        print(f"\nDataset Statistics:")
        print(f"  Total images: {len(X)}")
        print(f"  Image shape: {X.shape[1:]}")
        print(f"\nClass Distribution:")
        for label, count in class_counts.items():
            emotion = Config.EMOTIONS[label]
            print(f"  {emotion:12s} (class {label}): {count:5d} images")
        print(f"{'='*60}\n")
    
    return X, Y

def create_data_augmentation():
    """Create ImageDataGenerator for data augmentation"""
    return ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        shear_range=0.1,
        fill_mode='nearest'
    )

# ============================================================================
# MODEL ARCHITECTURE
# ============================================================================

def build_custom_cnn():
    """
    Build custom CNN architecture for emotion recognition
    
    Architecture:
    - 3 Conv blocks (64, 64, 32 filters)
    - MaxPooling after each Conv block
    - BatchNormalization for stability
    - Dropout for regularization
    - Dense layer with softmax
    """
    model = Sequential([
        # Block 1
        Conv2D(64, (3, 3), input_shape=(Config.IMG_SIZE, Config.IMG_SIZE, Config.CHANNELS), 
               padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 2
        Conv2D(64, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 3
        Conv2D(32, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Classifier
        Flatten(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(Config.NUM_CLASSES, activation='softmax')
    ])
    
    return model

# ============================================================================
# TRAINING
# ============================================================================

def train_model():
    """Main training function with complete pipeline"""
    
    print("\n" + "="*60)
    print("🎯 EMOTION RECOGNITION CNN TRAINING")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Device: {tf.config.list_physical_devices('GPU')}")
    print("="*60)
    
    # Load datasets
    print("\n📊 LOADING DATA...")
    X_train_full, Y_train_full = load_dataset('train')
    X_test, Y_test = load_dataset('test')
    
    # Split train into train + validation
    X_train, X_val, Y_train, Y_val = train_test_split(
        X_train_full, Y_train_full, 
        test_size=Config.VALIDATION_SPLIT, 
        stratify=Y_train_full,
        random_state=42
    )
    
    print(f"\nFinal Split:")
    print(f"  Training:   {len(X_train)} images")
    print(f"  Validation: {len(X_val)} images")
    print(f"  Test:       {len(X_test)} images")
    
    # Build model
    print("\n🏗️  BUILDING MODEL...")
    model = build_custom_cnn()
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    print("\n" + "="*60)
    print("MODEL ARCHITECTURE")
    print("="*60)
    model.summary()
    
    # Save model architecture
    try:
        plot_model(
            model, 
            to_file=os.path.join(Config.RESULTS_DIR, 'model_architecture.png'),
            show_shapes=True,
            show_layer_names=True,
            dpi=150
        )
        print(f"\n✓ Model architecture saved to results/model_architecture.png")
    except Exception as e:
        print(f"⚠ Could not save model plot: {e}")
    
    # Callbacks
    print("\n⚙️  SETTING UP CALLBACKS...")
    
    checkpoint = ModelCheckpoint(
        filepath=os.path.join(Config.MODEL_DIR, 'emotion_cnn.h5'),
        monitor='val_accuracy',
        mode='max',
        save_best_only=True,
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        mode='max',
        patience=Config.PATIENCE_EARLY_STOP,
        min_delta=Config.MIN_DELTA,
        verbose=1,
        restore_best_weights=True
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=Config.PATIENCE_LR_REDUCE,
        min_lr=1e-7,
        verbose=1
    )
    
    tensorboard = TensorBoard(
        log_dir=os.path.join(Config.RESULTS_DIR, 'logs'),
        histogram_freq=1
    )
    
    callbacks = [checkpoint, early_stop, reduce_lr, tensorboard]
    
    # Data augmentation
    datagen = create_data_augmentation()
    
    # Training
    print("\n🚀 STARTING TRAINING...")
    print("="*60)
    
    history = model.fit(
        datagen.flow(X_train, Y_train, batch_size=Config.BATCH_SIZE),
        validation_data=(X_val, Y_val),
        epochs=Config.EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save training history
    history_dict = {
        'train_loss': [float(x) for x in history.history['loss']],
        'train_accuracy': [float(x) for x in history.history['accuracy']],
        'val_loss': [float(x) for x in history.history['val_loss']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']]
    }
    
    with open(os.path.join(Config.MODEL_DIR, 'training_history.json'), 'w') as f:
        json.dump(history_dict, f, indent=4)
    
    print("\n✓ Training history saved")
    
    # Evaluation on test set
    print("\n📊 EVALUATING ON TEST SET...")
    test_loss, test_accuracy = model.evaluate(X_test, Y_test, verbose=0)
    print(f"  Test Loss: {test_loss:.4f}")
    print(f"  Test Accuracy: {test_accuracy*100:.2f}%")
    
    # Predictions
    Y_pred = model.predict(X_test, verbose=0)
    Y_pred_classes = np.argmax(Y_pred, axis=1)
    
    # Generate visualizations
    print("\n📈 GENERATING VISUALIZATIONS...")
    
    # 1. Training plots
    plot_training_history(history)
    
    # 2. Confusion matrix
    plot_confusion_matrix(Y_test, Y_pred_classes)
    
    # 3. Classification report
    save_classification_report(Y_test, Y_pred_classes)
    
    # 4. Sample predictions
    plot_sample_predictions(X_test, Y_test, Y_pred_classes)
    
    # Summary
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model saved: {Config.MODEL_DIR}/emotion_cnn.h5")
    print(f"Results saved: {Config.RESULTS_DIR}/")
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")
    print("="*60)

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_training_history(history):
    """Plot training & validation loss and accuracy"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss
    axes[0].plot(history.history['loss'], label='Train Loss', linewidth=2)
    axes[0].plot(history.history['val_loss'], label='Val Loss', linewidth=2)
    axes[0].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Loss', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy
    axes[1].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
    axes[1].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
    axes[1].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Accuracy', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'training_plots.png'), dpi=300, bbox_inches='tight')
    print("  ✓ Training plots saved")
    plt.close()

def plot_confusion_matrix(y_true, y_pred):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=list(Config.EMOTIONS.values()),
        yticklabels=list(Config.EMOTIONS.values()),
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
    print("  ✓ Confusion matrix saved")
    plt.close()

def save_classification_report(y_true, y_pred):
    """Save detailed classification report"""
    report = classification_report(
        y_true, 
        y_pred,
        target_names=list(Config.EMOTIONS.values()),
        digits=4
    )
    
    with open(os.path.join(Config.RESULTS_DIR, 'classification_report.txt'), 'w') as f:
        f.write("="*60 + "\n")
        f.write("EMOTION RECOGNITION - CLASSIFICATION REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(report)
        f.write("\n" + "="*60 + "\n")
    
    print("  ✓ Classification report saved")

def plot_sample_predictions(X_test, Y_test, Y_pred, num_samples=16):
    """Plot sample predictions"""
    indices = np.random.choice(len(X_test), num_samples, replace=False)
    
    fig, axes = plt.subplots(4, 4, figsize=(16, 16))
    axes = axes.flatten()
    
    for idx, ax in zip(indices, axes):
        img = X_test[idx]
        true_label = Config.EMOTIONS[Y_test[idx]]
        pred_label = Config.EMOTIONS[Y_pred[idx]]
        
        ax.imshow(img)
        ax.axis('off')
        
        color = 'green' if Y_test[idx] == Y_pred[idx] else 'red'
        ax.set_title(
            f"True: {true_label}\nPred: {pred_label}",
            fontsize=10,
            color=color,
            fontweight='bold'
        )
    
    plt.suptitle('Sample Predictions (Green=Correct, Red=Wrong)', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'sample_predictions.png'), dpi=300, bbox_inches='tight')
    print("  ✓ Sample predictions saved")
    plt.close()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Train model
    train_model()