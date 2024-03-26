import os
import cv2
import numpy as np


def load_data(images_dir, labels_dir):
    images = []
    labels = []

    # Полный путь к директориям с изображениями и метками
    images_dir = os.path.join(os.path.dirname(__file__), images_dir)
    labels_dir = os.path.join(os.path.dirname(__file__), labels_dir)

    image_files = os.listdir(images_dir)

    for image_file in image_files:
        if image_file.endswith('.jpg') or image_file.endswith('.png'):
            image_path = os.path.join(images_dir, image_file)

            # Загрузка изображения
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image,
                               (19, 19))  # Размеры изображений могут отличаться, примените соответствующий размер

            # Определение пути к файлу метки
            label_file = os.path.join(labels_dir, os.path.splitext(image_file)[0] + '.txt')

            # Проверка наличия файла метки
            if not os.path.exists(label_file):
                print(f"Метка для файла {image_path} не найдена.")
                continue

            # Загрузка метки из файла
            with open(label_file, 'r', encoding='utf-8') as f:
                label = f.read().strip()

            images.append(image)
            labels.append(label)

    return np.array(images), np.array(labels)



