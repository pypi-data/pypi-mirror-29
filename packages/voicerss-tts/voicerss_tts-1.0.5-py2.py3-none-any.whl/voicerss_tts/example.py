import logging_helper
logging = logging_helper.setup_logging()

from voicerss_tts import (TextToSpeech,
                          TextToSpeechCache,
                          ENGLISH_GREAT_BRITAIN,
                          WAV,
                          MONO_16KHZ_16BIT)
YOUR_API_KEY = u'?'

def text_to_speech(text,
                   api_key = YOUR_API_KEY):

    tts = TextToSpeech(api_key=api_key,
                       text=text,
                       language=ENGLISH_GREAT_BRITAIN,
                       codec=WAV,
                       audio_format=MONO_16KHZ_16BIT,
                       ssl=True)
    return tts.speech


def write_speech_data_to_cache(cache_location,
                               api_key = YOUR_API_KEY):
    text_to_speech_cache = TextToSpeechCache(folder=cache_location,
                                             api_key=api_key,
                                             language=ENGLISH_GREAT_BRITAIN,
                                             codec=WAV,
                                             audio_format=MONO_16KHZ_16BIT,
                                             ssl=True)
    while True:
        text = raw_input(u'Text (return to quit) >').strip().lower()
        if not text:
            break

        _ = text_to_speech_cache.fetch(text=text)

