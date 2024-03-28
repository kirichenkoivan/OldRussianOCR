import cv2
import os
import random
import string

def generate_random_name(length=10):
    """Генерация случайного имени файла."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def detect_words(image_path, output_folder):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение операции бинаризации
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Нахождение контуров на бинарном изображении
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создание папки для сохранения вырезанных изображений, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Обработка каждого контура
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Отбрасываем слишком маленькие или слишком большие контуры
        if w > 10 and h > 10:
            # Вырезаем содержимое контура из оригинального изображения
            word_image = image[y:y+h, x:x+w]
            # Генерируем случайное имя файла
            random_name = generate_random_name()
            # Сохраняем вырезанное изображение в папку с рандомным именем файла
            cv2.imwrite(os.path.join(output_folder, f'{random_name}.png'), word_image)

            # Отрисовка прямоугольника вокруг слова (можно закомментировать, если не нужно)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Вывод изображения с выделенными словами (можно закомментировать, если не нужно)
    cv2.imshow('Detected Words', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Пример использования
detect_words('images/test2.png', 'result_images')
