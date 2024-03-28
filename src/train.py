# train.py

from keras.callbacks import ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
from data_preprocessing import load_data_folder_structure
from model import build_model
import matplotlib.pyplot as plt
import numpy as np

# Пути к папкам с изображениями и лейблами
images_folder = '../data/images'
labels_folder = '../data/labels'

# Загрузка данных
images, labels = load_data_folder_structure(images_folder, labels_folder)

# Преобразование меток в числовой формат, если необходимо
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Определение архитектуры модели и параметров обучения
input_shape = (32, 32, 1)  # Размеры изображений после изменения размера и преобразования в оттенки серого
num_classes = len(set(labels))
epochs = 150
batch_size = 64

# Создание модели
model = build_model(input_shape, num_classes)

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Колбэк для сохранения модели с наилучшими параметрами
checkpoint_path = '../models/model_checkpoint.keras'
checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True, mode='min', verbose=1)

# Разделение данных на обучающую и тестовую выборки
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(images, labels_encoded, test_size=0.2, random_state=42)

# Обучение модели
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint], validation_data=(X_test, y_test))

# Сохранение классов в файл label_encoder_classes.npy
np.save('../models/label_encoder_classes.npy', label_encoder.classes_)

# Визуализация результатов обучения
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['loss'], label='loss')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend()
plt.show()
