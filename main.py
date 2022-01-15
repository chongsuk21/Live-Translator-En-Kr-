from __future__ import division
import speech_recognition

from googletrans import Translator
import re
import sys
from google_cloud_speech_to_text_api import MicrophoneStream
import os
from pynput.keyboard import Key, Listener
from google.cloud import texttospeech
from google.cloud import texttospeech_v1






os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:\side projects\Live translator\wide-gamma-202518-3f29d8c610fc.json"


#pip install --upgrade google-cloud-texttospeech

from google.cloud import speech

import pyaudio
from six.moves import queue

#pip install googletrans==3.1.0a0
tr = Translator()


def textToSpeech_outputMP3():
    client = texttospeech_v1.TextToSpeechClient()

    #To check langauge codes
    #print(client.list_voices())

    synthesis_input_en = texttospeech_v1.SynthesisInput(text=total_text_src)
    synthesis_input_ko = texttospeech_v1.SynthesisInput(text=total_text_ko)
    synthesis_input_fr = texttospeech_v1.SynthesisInput(text=total_text_fr)


    voice1 = texttospeech_v1.VoiceSelectionParams(
        language_code= 'en-US',
        ssml_gender= texttospeech_v1.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED

    )
    voice2 = texttospeech_v1.VoiceSelectionParams(
        language_code='ko-KR',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED

    )
    voice3 = texttospeech_v1.VoiceSelectionParams(
        language_code='fr-CA',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED

    )



    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding = texttospeech_v1.AudioEncoding.MP3
    )

    response1 = client.synthesize_speech(
        input=synthesis_input_en,
        voice=voice1,
        audio_config=audio_config
    )
    response2 = client.synthesize_speech(
        input=synthesis_input_ko,
        voice=voice2,
        audio_config=audio_config
    )
    response3 = client.synthesize_speech(
        input=synthesis_input_fr,
        voice=voice3,
        audio_config=audio_config
    )

    with open('The whole conversation in English.mp3', 'wb') as output1:
        output1.write(response1.audio_content)

    with open('The whole conversation in Korean.mp3', 'wb') as output1:
        output1.write(response2.audio_content)
    with open('The whole conversation in French.mp3', 'wb') as output1:
        output1.write(response3.audio_content)





def listen_print_loop(responses, src, dest):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    global total_text_src, total_text_ko, total_text_fr
    total_text_src = ""
    total_text_ko = ""
    total_text_fr = ""


    num_chars_printed = 0
    for response in responses:

        if not response.results:
            continue
        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        total_text = transcript + overwrite_chars
        if not result.is_final:
            sys.stdout.write(total_text + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            total_text_src += total_text
            total_text_ko += tr.translate(total_text, src='en', dest='ko').text
            total_text_fr += tr.translate(total_text, src='en', dest='fr').text

            print("English: " + total_text + " |||  Korean: " + tr.translate(total_text, src='en', dest='ko').text + " ||| French: " + tr.translate(total_text, src='en', dest='fr').text)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                break

            num_chars_printed = 0







print("Welcome to the live translator")

#src_lan = input(" What source language do you want to choose?")

#des_lan = input(" What destination language do you want to choose?")



src_lan = 'en'

des_lan = 'ko'



# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

language_code = "en-US"  # a BCP-47 language tag

client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code=language_code,
)

streaming_config = speech.StreamingRecognitionConfig(
    config=config, interim_results=True
)

with MicrophoneStream(RATE, CHUNK) as stream:
    audio_generator = stream.generator()
    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator
    )

    responses = client.streaming_recognize(streaming_config, requests)
    # Now, put the transcription responses to use.
    listen_print_loop(responses, src_lan, des_lan)
#After quiting the method the app will go make MP3 file
textToSpeech_outputMP3()
