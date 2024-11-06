
import json
import os
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2 import service_account
import logging

import httpx

class AudioSTT:
    initialized = False
    _supported_languages = None
    _client = None
    _config = None

    @staticmethod
    def initialize():
        if not AudioSTT.initialized:

            supported_languages_str = os.getenv('STT_SUPPORTED_LANGUAGES')
            AudioSTT._supported_languages = json.loads(supported_languages_str)
            
            credentials = service_account.Credentials.from_service_account_file('key.json')

            # Instantiates a client
            AudioSTT._client = SpeechClient(credentials=credentials)
            AudioSTT._config = cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=AudioSTT._supported_languages,
                model="long"
            )
            AudioSTT.initialized = True
                                    

    @staticmethod
    async def transcribe_file_v2(project_id: str, audio_data: bytes,) -> cloud_speech.RecognizeResponse:

        AudioSTT.initialize()


        # Reads a file as bytes
        content = audio_data
        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{project_id}/locations/global/recognizers/_",
            config=AudioSTT._config,
            content=content,
        )

        logging.info(f"Transcribing audio file")
        # Transcribes the audio into text
        try:
            response = AudioSTT._client.recognize(request=request)
            logging.info(f"Transcriptionw all results: {response.results}")
            return response.results[0].alternatives[0].transcript
        
        except Exception as e:
            logging.error(f"An error occurred in Transcribe: {e}")
            return None

    @staticmethod
    async def getDownloadAudio(audioURL, facebookToken):    
        
        # Define the headers
        headers = {
            'Authorization': f'Bearer {facebookToken}'
        }
        
        try:
            # Download the audio file
            async with httpx.AsyncClient() as client:
                audio_response = await client.get(audioURL, headers=headers)

            # Store the audio data in a variable
            audio_data = audio_response.content
            return audio_data

        except httpx.HTTPStatusError as exc:
            print(f"An HTTP error occurred: {exc}")
            return None
        except httpx.NetworkError:
            print("A network error occurred.")
            return None
        except httpx.TimeoutException:
            print("The request timed out.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
    