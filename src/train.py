import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
from data_preprocessing import load_data
from model import build_model
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Загрузка данных
images, labels = load_data('../data/images', '../data/labels')

# Преобразование меток в числовой формат, если необходимо
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Определение архитектуры модели и параметров обучения
input_shape = (19, 19, 1)  # Размеры изображений после изменения размера и преобразования в оттенки серого
num_classes = len(set(labels))
epochs = 50
batch_size = 64

# Создание модели
model = build_model(input_shape, num_classes)

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Колбэк для сохранения модели с наилучшими параметрами
checkpoint = ModelCheckpoint('../models/model_checkpoint.keras', monitor='val_loss')

# Обучение модели
history = model.fit(images, labels_encoded, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint])
# Сохранение классов в файл label_encoder_classes.npy
np.save('../models/label_encoder_classes.npy', label_encoder.classes_)

# Визуализация результатов обучения
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['loss'], label='loss')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend()
plt.show()
