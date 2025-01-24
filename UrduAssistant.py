import speech_recognition as sr
from gtts import gTTS
import os
import time
import random
import datetime
import webbrowser
import requests  # For API calls
import json  # For handling JSON data
from datetime import datetime, timedelta  # For reminders

def convert_to_urdu_numbers(number):
    urdu_numbers = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }
    return ''.join(urdu_numbers.get(char, char) for char in str(number))

def get_time():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute

    # Convert to 12-hour format
    period = "صبح" if hour < 12 else "شام"
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12

    # Convert numbers to Urdu
    hour_urdu = convert_to_urdu_numbers(hour)
    minute_urdu = convert_to_urdu_numbers(minute)

    return f"ابھی {period} کے {hour_urdu} بج کر {minute_urdu} منٹ ہیں"

def listen_urdu():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("سنو...")  # Listening...
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.energy_threshold = 2000

        try:
            print("بولیں...")  # Speak now...
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="ur-PK")
            print(f"آپ نے کہا: {text}")
            return text.lower()

        except sr.UnknownValueError:
            print("معذرت، میں سمجھ نہیں سکا")
            return None
        except sr.RequestError:
            print("انٹرنیٹ کنکشن چیک کریں")
            return None
        except Exception as e:
            print(f"کوئی مسئلہ ہے: {str(e)}")
            return None

def speak_urdu(text):
    try:
        tts = gTTS(text=text, lang='ur')
        tts.save("response.mp3")
        os.system("mpg123 -q response.mp3")  # -q for quiet mode
        os.remove("response.mp3")
    except Exception as e:
        print(f"آواز میں مسئلہ ہے: {str(e)}")

def get_weather(location):
    # Fetch weather data from OpenWeatherMap API
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        conditions = data['weather'][0]['description']
        return f"{location} میں آج کا موسم {conditions} اور {temperature} ڈگری سینٹی گریڈ ہے۔"
    else:
        return "موسم کی معلومات حاصل کرنے میں مسئلہ ہے۔"

def get_news():
    # Fetch news headlines from NewsAPI
    api_key = "YOUR_NEWSAPI_API_KEY"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?language=ur&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        headlines = [article['title'] for article in data['articles']]
        return "آج کی اہم خبریں: " + ", ".join(headlines)
    else:
        return "خبریں حاصل کرنے میں مسئلہ ہے۔"

def set_reminder(reminder_text, reminder_time):
    # Store reminders (could be in a file or database)
    # For simplicity, just print the reminder
    print(f"آپ کا ریمائنڈر: {reminder_text}۔ وقت: {reminder_time}")

def get_response(text):
    # Wake-up phrase
    if "احمد" in text:
        return "جی، میں احمد ہوں! آپ کی کیا مدد کر سکتا ہوں؟"

    time_patterns = [
        "مجھے", "ٹائم", "وقت", "بتاؤ", "کتنے", "بجے",
        "کتنا", "بجا", "کیا", "ٹائم", "ہوا", "ہے"
    ]

    google_patterns = [
        "گوگل", "کھولو", "سرچ", "تلاش", "ڈھونڈو",
        "دیکھو", "کرو", "مجھے", "چاہیے"
    ]

    youtube_patterns = [
        "یوٹیوب", "ویڈیو", "کھولو", "دکھاؤ", "چلاؤ",
        "دیکھنا", "ہے", "چاہیے"
    ]

    if any(word in text for word in time_patterns) and ("وقت" in text or "ٹائم" in text or "بجے" in text):
        return get_time()

    if any(word in text for word in google_patterns) and "گوگل" in text:
        webbrowser.open('https://www.google.com')
        return "میں گوگل کھول رہا ہوں"

    if any(word in text for word in youtube_patterns) and ("یوٹیوب" in text or "ویڈیو" in text):
        webbrowser.open('https://www.youtube.com')
        return "میں یوٹیوب کھول رہا ہوں"

    if "موسم" in text:
        location = "Karachi"  # You can modify to get user input for location
        return get_weather(location)

    if "خبریں" in text:
        return get_news()

    responses = {
        "سلام": [
            "وعلیکم السلام! میں آپ کی کیا مدد کر سکتا ہوں؟",
            "السلام علیکم! کیا حال ہے آپ کا؟"
        ],
        "کیسے": [
            "میں بالکل ٹھیک ہوں، آپ کیسے ہیں؟",
            "الحمدللہ، آپ سنائیں"
        ],
        "کون": [
            "میں آپ کا ذاتی اسسٹنٹ ہوں",
            "میں ایک اے آئی اسسٹنٹ ہوں جو آپ کی مدد کے لیے ہے"
        ],
        "شکریہ": [
            "آپ کا شکریہ",
            "کوئی بات نہیں"
        ],
        "حافظ": [
            "اللہ حافظ، اپنا خیال رکھیے گا",
            "خدا حافظ، پھر ملیں گے"
        ]
    }

    for key, responses_list in responses.items():
        if key in text:
            return random.choice(responses_list)

    return "معذرت، مجھے سمجھ نہیں آیا۔ آپ مجھے دوبارہ بتا سکتے ہیں؟"

def main():
    print("اردو اے آئی شروع ہو رہی ہے...")
    speak_urdu("السلام علیکم! میں آپ کا ذاتی اسسٹنٹ احمد ہوں۔ میں آپ کی کیا مدد کر سکتا ہوں؟")

    while True:
        try:
            text = listen_urdu()

            if text:
                response = get_response(text)
                print(f"AI کا جواب: {response}")
                speak_urdu(response)

            time.sleep(0.5)

        except KeyboardInterrupt:
            speak_urdu("اللہ حافظ، پھر ملیں گے")
            print("\nپروگرام ختم ہو رہا ہے...")
            break

if __name__ == "__main__":
    main()
