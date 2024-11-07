import json
import os
import httpx
import logging
from pydub import AudioSegment
import io
from dotenv import load_dotenv

class AudioSTT:
    initialized = False
    _supported_languages = None
    _base_url = "https://api.mesolitica.com/"  # Replace with actual Mesolitica API URL

    load_dotenv('variables.env')
    _api_key = os.getenv('MESOLITICA_API_KEY')
    
    @staticmethod
    async def transcribe_file(audio_data: bytes) -> str:
        temp_ogg = 'temp_audio.ogg'
        temp_mp3 = 'temp_audio.mp3'
        
        try:
            logging.info("Starting audio transcription process...")
            
            # Save the original OGG file
            with open(temp_ogg, 'wb') as f:
                f.write(audio_data)
            logging.info(f"Saved OGG file: {temp_ogg}")

            # Convert OGG to MP3
            audio = AudioSegment.from_ogg(temp_ogg)
            audio.export(temp_mp3, format="mp3")
            logging.info(f"Converted to MP3: {temp_mp3}")

            # Prepare the file for upload
            files = {
                'file': ('audio.mp3', open(temp_mp3, 'rb'), 'audio/mpeg')
            }

            # Match exact API parameters
            params = {
                'model': 'base',
                'language': 'ms'
            }
            
            logging.info("Making request to Mesolitica API with parameters:")
            logging.info(json.dumps(params, indent=2))

            # Make request to Mesolitica API
            headers = {
                'Authorization': f'Bearer {AudioSTT._api_key}'
            }

            async with httpx.AsyncClient() as client:
                logging.info("Sending request to Mesolitica API...")
                response = await client.post(
                    f"{AudioSTT._base_url}audio/transcriptions",
                    files=files,
                    data=params,
                    headers=headers
                )

            if response.status_code == 200:
                logging.info("Transcription successful!")
                logging.info(f"Response: {response.text}")
                return response.text
            else:
                logging.error(f"Transcription failed with status code: {response.status_code}")
                logging.error(f"Error response: {response.text}")
                return None

        except Exception as e:
            logging.error(f"An error occurred in Transcribe: {str(e)}")
            logging.exception("Full exception details:")
            return None
        finally:
            # Clean up temporary files
            if os.path.exists(temp_ogg):
                os.remove(temp_ogg)
                logging.info(f"Cleaned up {temp_ogg}")
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
                logging.info(f"Cleaned up {temp_mp3}")

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
    