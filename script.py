from bot import astria_api

files = [('tune[images][]', open("7047174818_0.jpg", 'rb')),
         ('tune[images][]', open("7047174818_1.jpg", 'rb'))]

response = astria_api.create_model("7047174818", "man", "81252", files)

print(response.json())
