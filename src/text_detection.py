import cv2
import numpy as np

def detect_words(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение порогового преобразования
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Применение морфологической операции закрытия для объединения близко расположенных контуров
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Поиск контуров
    contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Фильтрация контуров по размеру
    min_width = 15
    max_width = 350
    min_height = 10
    max_height = 100
    filtered_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if min_width < w < max_width and min_height < h < max_height:
            filtered_contours.append(contour)

    # Нарисовать контуры на изображении
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Вывести изображение с выделенными словами
    cv2.imshow('Words Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


detect_words('text_detection_images/test2.png')
