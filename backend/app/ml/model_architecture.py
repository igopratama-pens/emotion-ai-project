"""
Definisi Arsitektur Model (Sama Persis dengan train_model.py lama)
"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, 
    BatchNormalization, Activation
)

def build_emotion_cnn():
    # Hardcoded values sesuai train_model.py lama
    IMG_SIZE = 100
    CHANNELS = 3
    NUM_CLASSES = 7

    model = Sequential([
        # Block 1
        Conv2D(64, (3, 3), input_shape=(IMG_SIZE, IMG_SIZE, CHANNELS), padding='same'),
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
        Dense(NUM_CLASSES, activation='softmax')
    ])
    
    return model