import os
import cv2
import numpy as np

def load_data_folder_structure(images_dir, labels_dir):
    images = []
    labels = []

    # Получаем список подпапок в папке с изображениями
    subfolders = os.listdir(images_dir)

    for subfolder in subfolders:
        # Формируем пути к подпапкам с изображениями и метками
        subfolder_images_dir = os.path.join(images_dir, subfolder)
        subfolder_labels_dir = os.path.join(labels_dir, subfolder)

        # Получаем список файлов в подпапке с изображениями
        image_files = os.listdir(subfolder_images_dir)

        for image_file in image_files:
            if image_file.endswith('.jpg') or image_file.endswith('.png'):
                image_path = os.path.abspath(os.path.join(subfolder_images_dir, image_file))

                print("Loading image from path:", image_path)

                # Загрузка изображения
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    print(f"Unable to load image from path: {image_path}")
                    continue

                image = cv2.resize(image, (32, 32))  # Примените соответствующий размер

                # Определение пути к файлу метки
                label_file = os.path.join(subfolder_labels_dir, os.path.splitext(image_file)[0] + '.txt')

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


