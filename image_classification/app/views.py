from django.shortcuts import render

from . import utils


def main(request):
    context = dict()
    if request.method == 'POST':
        image_file = request.FILES.get('image_input')
        
        # очистка директории, куда сохраняются загруженные изображения
        utils.clear_user_uploads_directory()

        # тест изображения
        context = utils.predict_image(image_file)

    return render(request, 'base.html', context=context)