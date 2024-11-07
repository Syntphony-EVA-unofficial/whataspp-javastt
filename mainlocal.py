import logging
import json
import os
import time
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
from starlette.responses import Response
from AudioSTT import AudioSTT
from models import TranscriptRequest, TranscriptResponse
from datetime import datetime, timezone
import httpx
import urllib.parse
from fastapi import HTTPException
from pydantic import ValidationError


logging.basicConfig(level=logging.INFO)


load_dotenv('variables.env')
app = FastAPI()


#Verify the webhook from WhatsApp API configuration, this is only needed once

@app.get("/test")
def test_endpoint():
    return {"message": "This is a test endpoint from transcriber"}


@app.post("/transcript", response_model=TranscriptResponse)
async def transcript_request(request: Request):
    try:
        data = await request.json()
        logging.info("Request received {data}")
        try:
            transcript_request = TranscriptRequest(**data)
            logging.info(f"transcript incoming data: {json.dumps(data, indent=4)}")
            
            if transcript_request.mediaURL:
                downloadAudio = await AudioSTT.getDownloadAudio(transcript_request.mediaURL, transcript_request.token)
                if downloadAudio:
                    logging.info("Audio message downloaded successfully")
                    if isinstance(downloadAudio, bytes):
                        logging.info(f"The size of the binary data is {len(downloadAudio)} bytes")
                        STT_Result = await AudioSTT.transcribe_file(downloadAudio)
                        if STT_Result:
                            return JSONResponse(
                                status_code=200,
                                content=TranscriptResponse(lang="ms", message=STT_Result, success=True).model_dump()
                            )
                        else:
                            return JSONResponse(
                                status_code=200,
                                content=TranscriptResponse(lang="ms", message="", success=False).model_dump()
                            )
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"message": "Error processing request", "details": str(e)}
            )
    except Exception as e:
        logging.error(f"Error parsing request: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"message": "Error processing request", "details": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run("mainlocal:app", host="0.0.0.0", port=int(os.getenv("PORT", 8083)), reload=True, log_level="debug")


 


