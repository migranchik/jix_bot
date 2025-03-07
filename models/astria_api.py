import requests


class AstriaApi:

    # Init base config for Astria API model: api key, callback url, base api url
    def __init__(self, api_key, callback_url):
        self.api_key = api_key
        self.callback_url = callback_url
        self.base_url = "https://api.astria.ai/tunes"

    # Request to AstriaAPI for create model and learn it
    def create_model(self, user_id, gender, model_title, images):

        # Auth header
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        # Param for tuning the model
        request_param = {
            'tune[title]': f"{model_title}",
            'tune[branch]': "fast",
            'tune[callback]': f"{self.callback_url}/model?user_id={user_id}&model_title={model_title}",
            'tune[name]': f"{gender}"
        }

        response = requests.post(self.base_url, headers=headers, files=images, data=request_param)

        if response.status_code == 200:
            print("Tune успешно создан:", response.json())
        else:
            print("Ошибка при создании tune:", response.status_code, response.text)

        return response

    def create_prompt(self, model_id, user_id, prompt_text):

        # Auth header
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        # Param for creating prompt
        data = {
            'prompt[text]': f'sks man {prompt_text}',
            'prompt[callback]': f'{self.callback_url}/prompt?user_id={user_id}'
        }

        response = requests.post(f'{self.base_url}/{model_id}/prompts', headers=headers, data=data)

        if response.status_code == 200:
            print("Tune успешно создан:", response.json())
        else:
            print("Ошибка при создании prompt:", response.status_code, response.text)

        return response

