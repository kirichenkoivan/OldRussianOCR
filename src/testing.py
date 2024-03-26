import cv2
import numpy as np
from data_preprocessing import load_data  # Импорт функции для предобработки изображений
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model

# Путь к сохраненной модели
saved_model_path = '../models/model_checkpoint.keras'

# Загрузка обученной модели
model = load_model(saved_model_path)

# Загрузка меток для преобразования предсказанных числовых значений в текстовые метки
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('../models/label_encoder_classes.npy')

# Путь к изображению для тестирования
test_image_path = '../data/images/02.png'
test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)  # Загрузка изображения в оттенках серого

# Расширение размерности изображения для подходящего ввода в модель
test_image = np.expand_dims(test_image, axis=0)

# Предсказание метки для тестового изображения
predicted_label_index = np.argmax(model.predict(test_image))
predicted_label = label_encoder.inverse_transform([predicted_label_index])[0]

# Вывод предсказанной метки
print("Predicted Label:", predicted_label)
