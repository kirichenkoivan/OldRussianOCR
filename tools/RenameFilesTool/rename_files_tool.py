import os
import os
from PIL import Image, ImageEnhance, ImageFilter
import random
def create_image_variations(image_path):
    # Открываем оригинальное изображение
    original_image = Image.open(image_path)

    # Сохраняем исходное изображение
    original_image.save(image_path.replace('.png', '_original.png'))

    # Создаем 15 различных вариаций
    for i in range(15):
        # Создаем копию оригинального изображения для модификации
        modified_image = original_image.copy()

        # Производим случайные изменения
        modified_image = apply_random_transformations(modified_image)

        # Сохраняем модифицированное изображение
        output_path = image_path.replace('.png', f'_variation_{i+1}.png')
        modified_image.save(output_path)

def apply_random_transformations(image):
    # Применяем случайные преобразования
    random_contrast = random.uniform(0.5, 1.5)
    random_brightness = random.uniform(0.5, 1.5)
    random_sharpness = random.uniform(0.5, 1.5)
    random_rotation = random.randint(-10, 10)

    # Изменяем контрастность
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(random_contrast)

    # Изменяем яркость
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(random_brightness)

    # Изменяем резкость
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(random_sharpness)

    # Поворачиваем изображение
    image = image.rotate(random_rotation)

    return image
def rename_folders_and_create_labels(image_folder, labels_folder):
    # Получаем список всех папок в директории с изображениями
    folders = [folder for folder in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, folder))]

    # Подготавливаем счетчик для порядкового номера
    counter = 0

    # Переименовываем папки в порядковые номера и создаем метки для файлов в каждой папке
    for folder_name in folders:
        old_path = os.path.join(image_folder, folder_name)
        new_folder_name = f"{counter:02d}"
        new_path = os.path.join(image_folder, new_folder_name)
        os.rename(old_path, new_path)

        # Создаем метки для файлов в текущей папке
        create_labels_for_folder(new_path, labels_folder, new_folder_name)
        counter += 1


def create_labels_for_folder(folder_path, labels_folder, folder_name):
    # Получаем список всех файлов .png в текущей папке
    png_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]

    # Проходимся по каждому файлу .png и создаем для него .txt файл с содержимым из char.txt
    for png_file in png_files:
        txt_file_path = os.path.join(labels_folder, folder_name, f"{png_file[:-4]}.txt")  # Путь к метке
        char_file_path = os.path.join(folder_path, 'char.txt')  # Путь к файлу char.txt

        # Читаем содержимое файла char.txt
        with open(char_file_path, 'r', encoding='utf-8') as char_file:
            char_content = char_file.read()

        # Создаем папку для меток, если она не существует
        labels_folder_path = os.path.join(labels_folder, folder_name)
        if not os.path.exists(labels_folder_path):
            os.makedirs(labels_folder_path)

        # Записываем содержимое в новый .txt файл
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(char_content)

def variate_images(folder_path):
    # Получаем список всех папок в указанной директории
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    for subfolder in subfolders:
        png_files = [file for file in os.listdir(subfolder) if file.endswith('.png')]
        # Проходимся по каждому файлу .png в папке
        for png_file in png_files:
            image_path = os.path.join(subfolder, png_file)
            create_image_variations(image_path)



if __name__ == "__main__":
    # Получаем путь к текущей директории
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Формируем путь к директории с изображениями и к директории для меток
    image_folder = os.path.join(script_dir, "../../data/images")
    labels_folder = os.path.join(script_dir, "../../data/labels")

    # Проверяем существуют ли указанные директории
    if os.path.exists(image_folder) and os.path.exists(labels_folder):
        variate_images(image_folder)
        rename_folders_and_create_labels(image_folder, labels_folder)
        print("Папки были успешно переименованы, и созданы файлы меток.")
    else:
        print("Указанные директории не существуют.")
