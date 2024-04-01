import time
import pyttsx3
import speech_recognition as sr
import webbrowser
from datetime import datetime

class SpeechModule:
    def __init__(self, voice=0, volume=1, rate=125):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice].id)
        self.speaking = True  # Añadido para controlar si el bot debe hablar
    
    def talk(self, text):
        if self.speaking:  # Verifica si el bot debe hablar
            self.engine.say(text)
            self.engine.runAndWait()

    def stop_talking(self):  # Método para detener el habla
        self.speaking = False
        self.engine.stop()

    def start_talking(self):  # Método para permitir que el bot hable de nuevo
        self.speaking = True

class VoiceRecognitionModule:
    def __init__(self, key=None):
        self.key = key 
        self.r = sr.Recognizer()

    def recognize(self):
        with sr.Microphone() as source:
            print('Habla algo:')
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_google(audio, key=self.key, language="es-ES")
                return text
            except sr.UnknownValueError:
                print("No te entendí, intenta de nuevo.")
                return None
            except sr.RequestError:
                print("No hay servicio disponible.")
                return None

def respond_to_input(input_text, speech_module):
    input_text = input_text.lower()
    if "hola" in input_text or "buenos días" in input_text or "buenas tardes" in input_text or "buenas noches" in input_text:
        response = "Hola, ¿en qué puedo ayudarte hoy?"
        print("Bot:", response)
        speech_module.talk(response)
        return "greeting"
    elif "busca" in input_text or "investiga" in input_text or "quiero saber" in input_text:
        search_query = input_text.replace('busca', '').replace('investiga', '').replace('quiero saber', '').strip()
        print("Bot: Buscando información sobre", search_query)
        speech_module.talk("Buscando información sobre " + search_query)
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return "searching"
    elif "pon" in input_text and "canción" in input_text:
        song = input_text.replace('pon', '').replace('canción', '').strip()
        print("Bot: Reproduciendo", song, "en YouTube.")
        speech_module.talk("Reproduciendo " + song + " en YouTube.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return "playing music"
    elif "cállate" in input_text:
        print("Bot: Me voy a callar.")
        speech_module.stop_talking()  # Detiene el habla del bot
        return "silence"
    elif "responde" in input_text:
        print("Bot: Hola, aquí estoy.")
        speech_module.start_talking()  # Permite que el bot hable de nuevo
        speech_module.talk("Hola, aquí estoy.")
        return "resume"
    elif "fecha" in input_text:
        today_date = datetime.now().strftime("%d de %B de %Y")
        response = f"Hoy es {today_date}."
        print("Bot:", response)
        speech_module.talk(response)
        return "date"
    elif "hora" in input_text:
        current_time = datetime.now().strftime("%H:%M")
        response = f"Son las {current_time} horas."
        print("Bot:", response)
        speech_module.talk(response)
        return "time"
    elif "whatsapp" in input_text:
        print("Bot: Abriendo WhatsApp.")
        speech_module.talk("Abriendo WhatsApp.")
        webbrowser.open("https://web.whatsapp.com/")
        return "whatsapp"
    else:
        response = "No estoy seguro de cómo responder a eso. ¿Puedes ser más específico?"
        print("Bot:", response)
        speech_module.talk(response)
        return "unknown"

speech = SpeechModule()
recognition = VoiceRecognitionModule()
while True:
    text = recognition.recognize()
    if text:
        print("Usuario:", text)
        response = respond_to_input(text, speech)
        if response not in ["greeting", "searching", "playing music", "silence", "date", "time", "whatsapp"]:
            speech.talk(response)
    time.sleep(1)  