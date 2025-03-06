import requests


class AstriaApi:

    # Init base config for Astria API model
    def __init__(self, api_key, callback_url):
        self.api_key = api_key
        self.callback_url = callback_url
        self.base_url = "https://api.astria.ai/tunes"

    # Request to AstriaAPI for create model and learn it
    def create_model(self, user_id, gender, model_title, images):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        request_param = {
            'tune[title]': f"{model_title}",
            'tune[branch]': "fast",
            'tune[callback]': f"{self.callback_url}?user_id={user_id}&model_title={model_title}",
            'tune[name]': f"{gender}"
        }

        response = requests.post(self.base_url, headers=headers, files=images, data=request_param)

        if response.status_code == 200:
            print("Tune успешно создан:", response.json())
        else:
            print("Ошибка при создании tune:", response.status_code, response.text)

        return response
