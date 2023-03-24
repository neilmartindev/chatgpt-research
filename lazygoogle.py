import speech_recognition as sr
import webbrowser

# Set up recognizer instance
r = sr.Recognizer()

# Set up microphone input
mic = sr.Microphone()

# Google search function
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)

# Listen for voice command
with mic as source:
    print("Say something!")
    audio = r.listen(source)

# Convert speech to text
try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
    google_search(text)
except sr.UnknownValueError:
    print("Sorry, I didn't understand what you said.")
except sr.RequestError:
    print("Sorry, my speech recognition service is currently down.")
