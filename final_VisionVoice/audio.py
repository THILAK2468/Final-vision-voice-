from gtts import gTTS #type: ignore
import pygame #type: ignore
import os
from settings import user_language

pygame.mixer.init()
spoken_cache = set()

def speak_text(text):
    if not text.strip() or text in spoken_cache:
        return
    spoken_cache.add(text)

    filename = "output.mp3"
    tts = gTTS(text=text, lang=user_language, slow=False)
    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    try:
        os.remove(filename)
    except PermissionError:
        pass