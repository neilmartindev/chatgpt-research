from flask import Flask, render_template, request
import speech_recognition as sr
import requests
import json

app = Flask(__name__)

# obtain the API key for ChatGPT
API_KEY = "enter-api-here"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result',methods = ['POST'])
def result():
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
            return render_template('result.html', answer=answer)
        else:
            print("Error: Response does not contain 'choices' key.")
            return render_template('result.html', answer='Error: Response does not contain "choices" key.')

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return render_template('result.html', answer='Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return render_template('result.html', answer='Could not request results from Google Speech Recognition service; {0}'.format(e))
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('result.html', answer='An error occurred: {0}'.format(e))

if __name__ == '__main__':
    app.run(debug = True)
