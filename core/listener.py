import speech_recognition as sr 
recognizer = sr.Recognizer()
mic = sr.Microphone() 
recognizer.energy_threshold = 250 
# lower = more sensitive 
recognizer.dynamic_energy_threshold = True 
recognizer.pause_threshold = 0.7 
recognizer.phrase_threshold = 0.3 
recognizer.non_speaking_duration = 0.5 
def listen(timeout=6, phrase_time_limit=6):
    with mic as source:
        try:     
            audio = recognizer.listen(
            source,
            timeout=timeout, 
            phrase_time_limit=phrase_time_limit 
            )
            return recognizer.recognize_google(audio).lower()
        except:
            return None