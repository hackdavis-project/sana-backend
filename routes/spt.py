import logging
from fastapi import APIRouter, status, File, UploadFile, Depends, HTTPException
from pydantic import BaseModel
from utils.auth import get_current_user
from io import BytesIO
import base64
from google import genai
from google.genai import types, errors
import os
import json
from typing import List, Optional
import random
import time

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define Pydantic models for structured output
class Transcription(BaseModel):
    full_text: str
    language: str


class TranscriptionResponse(BaseModel):
    transcription: Transcription
    status: str = "success"


@router.post(
    "/spt/transcribe",
    response_model=TranscriptionResponse,
    status_code=status.HTTP_200_OK,
)
async def transcribe_audio(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    """
    Convert speech audio to text using Gemini.
    Accepts an audio file, processes it with Gemini, and returns transcription.
    """
    logger.info(f"Processing speech-to-text request for user_id={user['user_id']}")

    try:
        # Read audio file
        audio_bytes = await file.read()

        # Create BytesIO object from audio bytes
        audio_file = BytesIO(audio_bytes)
        audio_file.name = file.filename  # Set name attribute for proper file handling

        # Initialize Gemini client
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Determine mime type based on file extension
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["mp3", "wav", "m4a", "ogg", "flac", "webm"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Please upload mp3, wav, m4a, ogg, flac, or webm.",
            )

        mime_type = f"audio/{file_extension}"

        # Upload the file to Gemini
        audio_upload = await client.aio.files.upload(
            file=audio_file, config=types.UploadFileConfig(mime_type=mime_type)
        )

        # Create prompt for audio transcription with structured output
        prompt = f"""
        Please transcribe the provided audio file and format the result as a structured JSON object.
        
        Instructions:
        - Transcribe the speech as accurately as possible
        - Preserve the meaning and content of what is spoken
        - Detect the language of the audio
        
        Format your response exactly as this JSON structure:
        {{
          "full_text": "The complete transcribed text from the audio",
          "language": "en"
        }}
        
        If the audio contains sensitive content about personal experiences, trauma, or mental health concerns,
        please treat it with appropriate care and accuracy.
        """

        # Configure Gemini for JSON output
        config = types.GenerateContentConfig(
            response_schema=Transcription, response_mime_type="application/json"
        )

        # Max retries for API calls
        max_retries = 3
        retry_count = 0
        base_wait_time = 2  # Start with 2 seconds

        # Implement retry with exponential backoff
        while retry_count <= max_retries:
            try:
                # Generate content with Gemini
                response = await client.aio.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt, audio_upload],
                    config=config,
                )

                # Parse the response
                result = json.loads(response.text)

                # Create response with the structured Transcription model
                transcription = Transcription(**result)

                logger.info(
                    f"Successfully transcribed audio for user_id={user['user_id']}"
                )
                return TranscriptionResponse(transcription=transcription)

            except errors.ClientError as e:
                # Check if it's a rate limit error (429)
                if hasattr(e, "status_code") and e.status_code == 429:
                    retry_count += 1

                    if retry_count > max_retries:
                        logger.error(f"Rate limit exceeded after {max_retries} retries")
                        raise HTTPException(
                            status_code=429,
                            detail="Service temporarily unavailable due to rate limiting. Please try again later.",
                        )

                    # Calculate wait time with exponential backoff and jitter
                    wait_time = base_wait_time * (
                        2 ** (retry_count - 1)
                    ) + random.uniform(0, 1)
                    logger.info(
                        f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    # For other client errors
                    logger.error(f"Client error: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Speech-to-text processing failed: {str(e)}",
                    )
            except json.JSONDecodeError as json_err:
                logger.error(f"Error parsing JSON response: {str(json_err)}")
                logger.error(
                    f"Raw response: {response.text if 'response' in locals() else 'No response'}"
                )
                raise HTTPException(
                    status_code=500,
                    detail="Failed to parse transcription result. The response was not valid JSON.",
                )

    except Exception as e:
        logger.error(
            f"Speech-to-text processing failed for user_id={user['user_id']}: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"Speech-to-text processing failed: {str(e)}"
        )
