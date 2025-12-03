"""
Model Evaluation Script
Complete testing with visualizations for presentation
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix,
    precision_recall_fscore_support, accuracy_score
)
import tensorflow as tf

# Import from train_model
import sys
sys.path.append('.')
from train_model import Config, load_dataset

# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_model():
    """Complete model evaluation with visualizations"""
    
    print("\n" + "="*60)
    print("📊 MODEL EVALUATION")
    print("="*60)
    
    # Load model
    model_path = os.path.join(Config.MODEL_DIR, 'emotion_cnn.h5')
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("Please train the model first: python train_model.py")
        return
    
    print(f"\nLoading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    print("✓ Model loaded")
    
    # Load test data
    print("\nLoading test dataset...")
    X_test, Y_test = load_dataset('test', verbose=False)
    print(f"✓ Test set: {len(X_test)} images")
    
    # Predictions
    print("\nMaking predictions...")
    Y_pred_probs = model.predict(X_test, verbose=1)
    Y_pred = np.argmax(Y_pred_probs, axis=1)
    
    # Calculate metrics
    print("\n" + "="*60)
    print("PERFORMANCE METRICS")
    print("="*60)
    
    accuracy = accuracy_score(Y_test, Y_pred)
    print(f"\n✓ Overall Accuracy: {accuracy*100:.2f}%")
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        Y_test, Y_pred, average=None
    )
    
    print("\nPer-Class Metrics:")
    print(f"{'Emotion':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support'}")
    print("-" * 65)
    
    for i in range(Config.NUM_CLASSES):
        emotion = Config.EMOTIONS[i]
        print(f"{emotion:<15} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]}")
    
    # Macro and weighted averages
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        Y_test, Y_pred, average='macro'
    )
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        Y_test, Y_pred, average='weighted'
    )
    
    print("\n" + "-" * 65)
    print(f"{'Macro Average':<15} {precision_macro:<12.4f} {recall_macro:<12.4f} {f1_macro:<12.4f}")
    print(f"{'Weighted Avg':<15} {precision_weighted:<12.4f} {recall_weighted:<12.4f} {f1_weighted:<12.4f}")
    
    # Detailed classification report
    print("\n" + "="*60)
    print("DETAILED CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(
        Y_test, Y_pred,
        target_names=list(Config.EMOTIONS.values()),
        digits=4
    ))
    
    # Confusion matrix analysis
    cm = confusion_matrix(Y_test, Y_pred)
    print("\n" + "="*60)
    print("CONFUSION MATRIX ANALYSIS")
    print("="*60)
    
    # Most confused pairs
    confused_pairs = []
    for i in range(Config.NUM_CLASSES):
        for j in range(Config.NUM_CLASSES):
            if i != j and cm[i, j] > 0:
                confused_pairs.append((
                    Config.EMOTIONS[i],
                    Config.EMOTIONS[j],
                    cm[i, j]
                ))
    
    confused_pairs.sort(key=lambda x: x[2], reverse=True)
    
    print("\nTop 5 Most Confused Emotion Pairs:")
    for i, (true_emotion, pred_emotion, count) in enumerate(confused_pairs[:5], 1):
        print(f"{i}. {true_emotion} → {pred_emotion}: {count} times")
    
    # Generate comprehensive visualizations
    print("\n" + "="*60)
    print("GENERATING COMPREHENSIVE VISUALIZATIONS")
    print("="*60)
    
    generate_all_visualizations(model, X_test, Y_test, Y_pred, Y_pred_probs)
    
    # Summary
    print("\n" + "="*60)
    print("✅ EVALUATION COMPLETE")
    print("="*60)
    print(f"Overall Accuracy: {accuracy*100:.2f}%")
    print(f"Results saved to: {Config.RESULTS_DIR}/")
    print("="*60 + "\n")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

def generate_all_visualizations(model, X_test, Y_test, Y_pred, Y_pred_probs):
    """Generate all visualizations for presentation"""
    
    # 1. Enhanced confusion matrix
    print("\n1. Generating confusion matrix...")
    plot_enhanced_confusion_matrix(Y_test, Y_pred)
    
    # 2. Per-class performance
    print("2. Generating per-class performance chart...")
    plot_per_class_performance(Y_test, Y_pred)
    
    # 3. Confidence distribution
    print("3. Generating confidence distribution...")
    plot_confidence_distribution(Y_pred_probs, Y_test, Y_pred)
    
    # 4. Prediction examples (correct & wrong)
    print("4. Generating prediction examples...")
    plot_prediction_examples(X_test, Y_test, Y_pred, Y_pred_probs)
    
    # 5. Training history (if available)
    print("5. Loading training history...")
    history_path = os.path.join(Config.MODEL_DIR, 'training_history.json')
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
        plot_enhanced_training_history(history)
    else:
        print("   ⚠ Training history not found, skipping...")
    
    print("\n✓ All visualizations generated successfully!")

def plot_enhanced_confusion_matrix(y_true, y_pred):
    """Enhanced confusion matrix with percentages"""
    cm = confusion_matrix(y_true, y_pred)
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Absolute counts
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=list(Config.EMOTIONS.values()),
        yticklabels=list(Config.EMOTIONS.values()),
        cbar_kws={'label': 'Count'},
        ax=axes[0]
    )
    axes[0].set_title('Confusion Matrix (Counts)', fontsize=16, fontweight='bold', pad=20)
    axes[0].set_ylabel('True Label', fontsize=12)
    axes[0].set_xlabel('Predicted Label', fontsize=12)
    
    # Percentages
    sns.heatmap(
        cm_percent, 
        annot=True, 
        fmt='.1f', 
        cmap='RdYlGn',
        xticklabels=list(Config.EMOTIONS.values()),
        yticklabels=list(Config.EMOTIONS.values()),
        cbar_kws={'label': 'Percentage (%)'},
        ax=axes[1]
    )
    axes[1].set_title('Confusion Matrix (Percentages)', fontsize=16, fontweight='bold', pad=20)
    axes[1].set_ylabel('True Label', fontsize=12)
    axes[1].set_xlabel('Predicted Label', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'confusion_matrix_enhanced.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def plot_per_class_performance(y_true, y_pred):
    """Bar chart of per-class metrics"""
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None
    )
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(Config.NUM_CLASSES)
    width = 0.25
    
    ax.bar(x - width, precision, width, label='Precision', color='#667eea')
    ax.bar(x, recall, width, label='Recall', color='#764ba2')
    ax.bar(x + width, f1, width, label='F1-Score', color='#f093fb')
    
    ax.set_xlabel('Emotion', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Per-Class Performance Metrics', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(list(Config.EMOTIONS.values()), rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'per_class_performance.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def plot_confidence_distribution(y_pred_probs, y_true, y_pred):
    """Distribution of prediction confidence"""
    confidences = np.max(y_pred_probs, axis=1)
    correct = (y_true == y_pred)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Overall distribution
    axes[0].hist(confidences, bins=50, color='#667eea', alpha=0.7, edgecolor='black')
    axes[0].axvline(np.mean(confidences), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean: {np.mean(confidences):.3f}')
    axes[0].set_xlabel('Confidence', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Prediction Confidence Distribution', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Correct vs Incorrect
    axes[1].hist(confidences[correct], bins=30, alpha=0.7, label='Correct', 
                 color='green', edgecolor='black')
    axes[1].hist(confidences[~correct], bins=30, alpha=0.7, label='Incorrect', 
                 color='red', edgecolor='black')
    axes[1].set_xlabel('Confidence', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].set_title('Confidence: Correct vs Incorrect Predictions', 
                      fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'confidence_distribution.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def plot_prediction_examples(X_test, y_true, y_pred, y_pred_probs, num_examples=12):
    """Show correct and incorrect prediction examples"""
    correct_mask = (y_true == y_pred)
    incorrect_mask = ~correct_mask
    
    # Get indices
    correct_indices = np.where(correct_mask)[0]
    incorrect_indices = np.where(incorrect_mask)[0]
    
    # Sample
    n = num_examples // 2
    correct_sample = np.random.choice(correct_indices, min(n, len(correct_indices)), replace=False)
    incorrect_sample = np.random.choice(incorrect_indices, min(n, len(incorrect_indices)), replace=False)
    
    fig, axes = plt.subplots(4, 3, figsize=(15, 18))
    axes = axes.flatten()
    
    # Plot correct predictions
    for idx, ax in zip(correct_sample, axes[:n]):
        img = X_test[idx]
        true_label = Config.EMOTIONS[y_true[idx]]
        pred_label = Config.EMOTIONS[y_pred[idx]]
        confidence = y_pred_probs[idx][y_pred[idx]]
        
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(
            f"✓ CORRECT\nTrue: {true_label}\nPred: {pred_label}\nConf: {confidence*100:.1f}%",
            fontsize=10,
            color='green',
            fontweight='bold'
        )
    
    # Plot incorrect predictions
    for idx, ax in zip(incorrect_sample, axes[n:]):
        img = X_test[idx]
        true_label = Config.EMOTIONS[y_true[idx]]
        pred_label = Config.EMOTIONS[y_pred[idx]]
        confidence = y_pred_probs[idx][y_pred[idx]]
        
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(
            f"✗ INCORRECT\nTrue: {true_label}\nPred: {pred_label}\nConf: {confidence*100:.1f}%",
            fontsize=10,
            color='red',
            fontweight='bold'
        )
    
    plt.suptitle('Prediction Examples (Correct & Incorrect)', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'prediction_examples_detailed.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

def plot_enhanced_training_history(history):
    """Enhanced training history plots"""
    epochs = range(1, len(history['train_loss']) + 1)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Loss
    axes[0, 0].plot(epochs, history['train_loss'], 'o-', label='Train Loss', linewidth=2, markersize=4)
    axes[0, 0].plot(epochs, history['val_loss'], 's-', label='Val Loss', linewidth=2, markersize=4)
    axes[0, 0].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Epoch', fontsize=12)
    axes[0, 0].set_ylabel('Loss', fontsize=12)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Accuracy
    axes[0, 1].plot(epochs, history['train_accuracy'], 'o-', label='Train Accuracy', linewidth=2, markersize=4)
    axes[0, 1].plot(epochs, history['val_accuracy'], 's-', label='Val Accuracy', linewidth=2, markersize=4)
    axes[0, 1].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Epoch', fontsize=12)
    axes[0, 1].set_ylabel('Accuracy', fontsize=12)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Overfitting analysis
    train_val_gap = np.array(history['train_accuracy']) - np.array(history['val_accuracy'])
    axes[1, 0].plot(epochs, train_val_gap, 'o-', linewidth=2, markersize=4, color='purple')
    axes[1, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].fill_between(epochs, 0, train_val_gap, alpha=0.3, color='purple')
    axes[1, 0].set_title('Overfitting Analysis (Train-Val Gap)', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Epoch', fontsize=12)
    axes[1, 0].set_ylabel('Accuracy Gap', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Learning progression
    axes[1, 1].plot(epochs, history['train_loss'], label='Train Loss', linewidth=2)
    axes[1, 1].plot(epochs, history['val_loss'], label='Val Loss', linewidth=2)
    ax2 = axes[1, 1].twinx()
    ax2.plot(epochs, history['val_accuracy'], 'g--', label='Val Accuracy', linewidth=2)
    axes[1, 1].set_title('Loss vs Accuracy Progression', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Epoch', fontsize=12)
    axes[1, 1].set_ylabel('Loss', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12, color='g')
    axes[1, 1].legend(loc='upper left')
    ax2.legend(loc='upper right')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Training History Analysis', fontsize=18, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULTS_DIR, 'training_history_enhanced.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    evaluate_model()