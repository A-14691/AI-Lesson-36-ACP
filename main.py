import os
from datetime import datetime
from urllib.parse import quote_plus
import pyttsx3
import speech_recognition as sr


class VoiceAssistant:
    def __init__(self):
        self.running = True
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

    def speak(self, text: str) -> None:
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 8) -> str:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
        except OSError as error:
            self.speak(f"I could not access the microphone: {error}")
            return ""

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower().strip()
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand that.")
        except sr.RequestError as error:
            self.speak(f"The speech service is unavailable: {error}")
        return ""

    def respond(self, command: str) -> None:
        if not command:
            return

        if any(word in command for word in ("hello", "hey", "hi")):
            self.speak("Hello! How can I help you?")
        elif "your name" in command or "who are you" in command:
            self.speak("I am your Python voice assistant.")
        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}.")
        elif "date" in command:
            current_date = datetime.now().strftime("%A, %d %B %Y")
            self.speak(f"Today is {current_date}.")
        elif "open google" in command:
            self.speak("Opening Google.")
            os.startfile("https://www.google.com")
        elif "open youtube" in command:
            self.speak("Opening YouTube.")
            os.startfile("https://www.youtube.com")
        elif "search for" in command:
            query = command.split("search for", 1)[1].strip()
            if query:
                self.speak(f"Searching for {query}.")
                os.startfile(f"https://www.google.com/search?q={quote_plus(query)}")
            else:
                self.speak("What would you like me to search for?")
        elif any(word in command for word in ("exit", "quit", "stop", "goodbye")):
            self.speak("Goodbye!")
            self.running = False
        else:
            self.speak("I am not sure how to help with that yet. Try asking for the time or date.")

    def run(self) -> None:
        self.speak("Voice assistant activated. Say something!")
        while self.running:
            self.respond(self.listen())

        self.engine.stop()


def main() -> None:
    assistant = VoiceAssistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
        if assistant.engine.isBusy():
            assistant.engine.stop()


if __name__ == "__main__":
    main()
