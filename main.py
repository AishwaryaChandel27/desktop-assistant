import datetime
import os
import webbrowser

import pyttsx3
import speech_recognition as sr
import openai
import sys
import api
import random
import numpy as np

chatStr = ""

# def chat(query):
#     global chatStr
#     print(chatStr)
#     openai.api_key = api.api
#     chatStr += f"Aishwarya: {query}\n Shine: "
#
#     response = openai.Completion.create(
#         engine="davinci-002",
#         prompt=query,
#         temperature=1,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#
#     say(response.choices[0].text.strip())
#     chatStr += f"{response.choices[0].text.strip()}\n"
#     return response.choices[0].text.strip()
#

def ai(prompt):
    openai.api_key = api.api
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

    return response.choices[0].text.strip()


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        print("Listening....")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Sorry, I couldn't catch that. Could you please repeat?")
            return ""


if __name__ == "__main__":
    print("PyCharm")
    say("Hello, I am Shine A.I.")
    while True:
        print("Listening....")
        query = takeCommand()

        sites = {
            "linkedin": "https://www.linkedin.com/",
            "youtube": "https://www.youtube.com/",
            "chatgpt": "https://openai.com/gpt",
        }

        for site_name, site_url in sites.items():
            if f"open {site_name}".lower() in query:
                say(f"Good to go. Opening {site_name}.")
                webbrowser.open(site_url)
                break
        if "open google" in query.lower() and "search for" in query.lower():
            query = query.lower().replace("open google and search for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "open google" in query.lower():
            webbrowser.open("https://www.google.com/")

        elif "open spotify".lower() in query:
            spotify_path = r"C:\Users\Aishwarya\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
            os.system(f'start "" "{spotify_path}"')

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f" time is {hour}  {min} minutes")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Shine Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

        say(query)
