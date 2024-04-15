from config import IAMTOKEN, FOLDER_ID
import requests


def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {IAMTOKEN}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': FOLDER_ID,
    }
    # Выполняем запрос
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"
