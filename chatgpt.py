import speech_recognition as sr
import requests
import json

# obtain the API key for ChatGPT
API_KEY = "enter-api-here"

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak:")
    audio = r.listen(source)

try:
    # use Google's speech recognition to convert speech to text
    query = r.recognize_google(audio)
    print("You said: " + query)

    # make a request to the ChatGPT API
    response = requests.post(
        "https://api.openai.com/v1/engines/davinci/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": query,
            "max_tokens": 1000,
            "n": 1,
            "stop": ".",
            "temperature": 0.75,
        },
    )

    # parse the response from ChatGPT
    response_text = json.loads(response.text)
    if "choices" in response_text:
        answer = response_text["choices"][0]["text"].strip()
        print("ChatGPT says: " + answer)
    else:
        print("Error: Response does not contain 'choices' key.")

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
except Exception as e:
    print(f"An error occurred: {e}")
