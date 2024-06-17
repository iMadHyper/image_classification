from . import utils

from django.core.files.uploadedfile import InMemoryUploadedFile
import io

from image_classification.settings import STATICFILES_DIRS


def test_predict_jpg_file():
    '''
    Should not return error.
    Should return results
    '''
    img_name = 'apple.jpg'
    img_path = STATICFILES_DIRS[0] + f'files_to_test\\{img_name}'

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_file = InMemoryUploadedFile(
    io.BytesIO(img_data),  # Передаем данные в формате BytesIO
    None,  # Здесь можно указать поле name, если необходимо
    img_name,  # Имя файла
    "image/jpeg",  # MIME тип
    len(img_data),  # Размер файла
    None  # Здесь можно указать кодировку
    )

    context = utils.predict_image(img_file)
    print(context)
    assert context.get('error') == None
    assert context.get('results') != None


def test_predict_webp_file():
    '''
    Should not return error.
    Should return results
    '''
    img_name = 'avocado.webp'
    img_path = STATICFILES_DIRS[0] + f'files_to_test\\{img_name}'

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_file = InMemoryUploadedFile(
    io.BytesIO(img_data),  # Передаем данные в формате BytesIO
    None,  # Здесь можно указать поле name, если необходимо
    img_name,  # Имя файла
    "image/webp",  # MIME тип
    len(img_data),  # Размер файла
    None  # Здесь можно указать кодировку
    )

    context = utils.predict_image(img_file)
    print(context)
    assert context.get('error') == None
    assert context.get('results') != None


def test_predict_png_file():
    '''
    Should return error.
    Should not return results
    '''
    img_name = 'cherry.png'
    img_path = STATICFILES_DIRS[0] + f'files_to_test\\{img_name}'

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_file = InMemoryUploadedFile(
    io.BytesIO(img_data),  # Передаем данные в формате BytesIO
    None,  # Здесь можно указать поле name, если необходимо
    img_name,  # Имя файла
    "image/png",  # MIME тип
    len(img_data),  # Размер файла
    None  # Здесь можно указать кодировку
    )

    context = utils.predict_image(img_file)
    print(context)
    assert context.get('error') != None
    assert context.get('results') == None


def test_predict_pdf_file():
    '''
    Should return error.
    Should not return results
    '''
    img_name = 'asd.pdf'
    img_path = STATICFILES_DIRS[0] + f'files_to_test\\{img_name}'

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_file = InMemoryUploadedFile(
    io.BytesIO(img_data),  # Передаем данные в формате BytesIO
    None,  # Здесь можно указать поле name, если необходимо
    img_name,  # Имя файла
    "image/pdf",  # MIME тип
    len(img_data),  # Размер файла
    None  # Здесь можно указать кодировку
    )

    context = utils.predict_image(img_file)
    print(context)
    assert context.get('error') != None
    assert context.get('results') == None


def test_predict_word_file():
    '''
    Should return error.
    Should not return results
    '''
    img_name = 'asd.docx'
    img_path = STATICFILES_DIRS[0] + f'files_to_test\\{img_name}'

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_file = InMemoryUploadedFile(
    io.BytesIO(img_data),  # Передаем данные в формате BytesIO
    None,  # Здесь можно указать поле name, если необходимо
    img_name,  # Имя файла
    "image/pdf",  # MIME тип
    len(img_data),  # Размер файла
    None  # Здесь можно указать кодировку
    )

    context = utils.predict_image(img_file)
    print(context)
    assert context.get('error') != None
    assert context.get('results') == None