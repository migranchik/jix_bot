# THIS FILE FOR ONLY TESTING

from bot import astria_api

response = astria_api.create_prompt(2205398, 123456, 'draw me pls')
# #response = astria_api.prompt_info(2204087, 22893833)

print(response.json())
