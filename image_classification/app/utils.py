import tensorflow as tf
import numpy as np
from PIL import Image

from image_classification.settings import SAVE_USER_UPLOADS_DIRECTORY, IMG_HEIGHT, IMG_WIDTH, MODEL, CLASS_NAMES, CLASS_RU_NAMES, CLASS_IMAGES

import os
import shutil


def clear_user_uploads_directory():
    '''
    Clears users uploads directory, set in settings (SAVE_USER_UPLOADS_DIRECTORY)
    '''
    if os.path.exists(SAVE_USER_UPLOADS_DIRECTORY):
        shutil.rmtree(SAVE_USER_UPLOADS_DIRECTORY + '\\') # очистка директории
        os.makedirs(SAVE_USER_UPLOADS_DIRECTORY)

def predict_image(image_file):
    '''
    Tries to predict image.
    Returns results and user_image if successful
    Return error otherwise
    '''
    context = dict()
    try:
        # Генерируем путь к сохраняемому изображению
        image_path = os.path.join(SAVE_USER_UPLOADS_DIRECTORY, image_file.name)

        # Сохраняем изображение на сервере
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Генерируем URL для сохраненного изображения
        image_url = f'media/uploaded_images/{image_file.name}'

        img = Image.open(image_file)
        img = img.resize((IMG_HEIGHT, IMG_WIDTH))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        # make predictions
        predictions = MODEL.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # print inference result
        print("На изображении скорее всего {} ({:.2f}% вероятность)".format(
            CLASS_NAMES[np.argmax(score)],
            100 * np.max(score)))
        
        winner = {
            'name' : CLASS_RU_NAMES[CLASS_NAMES[np.argmax(score)]],
            'score' : f'{100 * np.max(score):.2f}%',
            'img' : CLASS_IMAGES[CLASS_NAMES[np.argmax(score)]]
        }
        context.update({'winner' : winner})

        scores = np.array(score)

        results = dict()

        index = 1
        for s in np.nditer(-np.sort(-scores)):
            i = np.where(scores == s)
            print("{} - {:.2f}%".format(CLASS_NAMES[int(i[0])], 100 * s))

            results.update({
                f'{index}' : {
                    'name' : CLASS_RU_NAMES[f'{CLASS_NAMES[int(i[0])]}'],
                    'score' : f'{100 * s:.2f}',
                    'img' : CLASS_IMAGES[f'{CLASS_NAMES[int(i[0])]}']
                }
            })
            index += 1
            
        context.update({'results' : results})
        context.update({'user_image_url' : image_url})

    except Exception as ex:
        print(ex)
        context.update({
            'error' : 'Не получилось открыть файл. Поддерживаемые типы файлов: jpg, jpeg, webp.'
        })
    
    return context