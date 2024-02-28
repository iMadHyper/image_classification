from django.shortcuts import render

import pathlib
import tensorflow as tf
import numpy as np
from PIL import Image

from .models import ObjectImage

from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL

import os
import glob
import shutil

img_height = 160
img_width = 160
model = tf.keras.models.load_model('model_v1.h5')

class_names = ['apple', 'avocado', 'banana', 'cherry', 'coconut', 'grape']
class_images = {
    'apple' : 'img/apples.jpg', 
    'avocado' : 'img/avocado.jpg', 
    'banana' : 'img/bananas.jpg', 
    'cherry' : 'img/cherry.jpg', 
    'coconut' : 'img/coconut.jpg', 
    'grape' : 'img/grape.jpg'
}
class_ru_names = {
    'apple' : 'Яблоко', 
    'avocado' : 'Авокадо', 
    'banana' : 'Банан', 
    'cherry' : 'Вишня', 
    'coconut' : 'Кокос', 
    'grape' : 'Виноград'
}

def main(request):
    context = dict()
    if request.method == 'POST':
        image_file = request.FILES.get('image_input')

        try:
            # Определяем директорию, куда будем сохранять изображения
            save_directory = os.path.join(MEDIA_ROOT, 'uploaded_images') # предположим, что у вас есть MEDIA_ROOT в настройках Django
            
            if os.path.exists(save_directory):
                shutil.rmtree(save_directory + '\\') # очистка директории
            os.makedirs(save_directory)
            
            '''files = glob.glob(save_directory + '\\')
            if files:
                for f in files:
                    os.remove(f)'''

            # Генерируем путь к сохраняемому изображению
            image_path = os.path.join(save_directory, image_file.name)

            # Сохраняем изображение на сервере
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Генерируем URL для сохраненного изображения
            image_url = f'media/uploaded_images/{image_file.name}'

            img = Image.open(image_file)
            img = img.resize((img_height, img_width))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            # make predictions
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            # print inference result
            '''print("На изображении скорее всего {} ({:.2f}% вероятность)".format(
                class_names[np.argmax(score)],
                100 * np.max(score)))'''

            winner = {
                'name' : class_ru_names[class_names[np.argmax(score)]],
                'score' : f'{100 * np.max(score):.2f}%',
                'img' : class_images[class_names[np.argmax(score)]]
            }
            context.update({'winner' : winner})

            scores = np.array(score)

            results = dict()

            index = 1
            for s in np.nditer(-np.sort(-scores)):
                #i, = np.where(np.isclose(scores, s))
                i = np.where(scores == s)
                # print(i)
                print("{} - {:.2f}%".format(class_names[int(i[0])], 100 * s))

                results.update({
                    f'{index}' : {
                        'name' : class_ru_names[f'{class_names[int(i[0])]}'],
                        'score' : f'{100 * s:.2f}',
                        'img' : class_images[f'{class_names[int(i[0])]}']
                    }
                })
                index += 1
            
            context.update({'results' : results})
            context.update({'user_image_url' : image_url})
        except Exception as ex:
            print(ex)
            context.update({
                'error' : 'Не получилось открыть файл. Поддерживаемые типы файлов: png, jpg, jpeg.'
            })

    return render(request, 'base.html', context=context)