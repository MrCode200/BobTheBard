import google.generativeai as genai
import os

GOOGLE_API_KEY = "AIzaSyDdyD4JGdKgM6kcYMcWlkhvRK4gkW4_U4k"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro-latest')

response = model.generate_content("What is the weather in Germany")
print(response)
