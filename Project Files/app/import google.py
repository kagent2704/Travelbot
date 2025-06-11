import google.generativeai as genai

genai.configure(api_key="AIzaSyAjOZL82IBO7q-rtySTOMNMM5Ez91aohzY")

models = genai.list_models()
for model in models:
    print(model.name)
