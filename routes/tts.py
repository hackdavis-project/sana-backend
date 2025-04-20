from io import BytesIO
import logging

from fastapi import APIRouter, status, UploadFile, File, Depends, HTTPException
from modules import eleven_labs, database
from elevenlabs import AsyncElevenLabs, VoiceSettings
from fastapi.responses import StreamingResponse
import os
from utils.auth import get_current_user

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/tts/generate", status_code=status.HTTP_200_OK)
async def tts(text: str, user=Depends(get_current_user)):
    client: AsyncElevenLabs = await eleven_labs.get_eleven_client()
    # Try to get custom voice_id for user
    voice_id = await database.get_voice_id(user['user_id'])
    if not voice_id:
        voice_id = os.getenv('ELEVEN_LABS_VOICE_ID')
        logger.info(f"No custom voice for user_id={user['user_id']}, using default voice_id={voice_id}")
    else:
        logger.info(f"Using custom voice_id={voice_id} for user_id={user['user_id']}")
        
    try:
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_flash_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.05,
            ),
        )
        audio_data = BytesIO()
        async for chunk in response:
            if chunk:
                audio_data.write(chunk)
        audio_data.seek(0)  # rewind to start
        logger.info(f"Generated TTS audio for user_id={user['user_id']}")
        return StreamingResponse(
            audio_data,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=output.mp3"}
        )
    except Exception as e:
        logger.error(f"TTS generation failed for user_id={user['user_id']}: {e}")
        raise HTTPException(status_code=500, detail="TTS generation failed.")

@router.post("/tts/clone_voice", status_code=status.HTTP_200_OK)
async def clone_voice(file: UploadFile = File(...), user=Depends(get_current_user)):
    """
    Accepts an audio file, sends it to ElevenLabs for voice cloning, saves the returned voice_id for the user.
    """
    logger.info(f"Received request to clone voice for user_id={user['user_id']}")
    try:
        client: AsyncElevenLabs = await eleven_labs.get_eleven_client()
        audio_bytes = await file.read()
        # ElevenLabs expects a file-like object, so wrap in BytesIO
        audio_file = BytesIO(audio_bytes)
        # The following is a placeholder for the actual ElevenLabs API call
        # Replace with the correct call to create a new voice from audio sample
        result = await client.voices.add(
            name=f"user_{user['user_id']}_voice",
            files=[audio_file],
            remove_background_noise=True
        )
        voice_id = result.voice_id if hasattr(result, 'voice_id') else result['voice_id']
        logger.info(f"Cloned voice for user_id={user['user_id']}, received voice_id={voice_id}")
        await database.save_voice_id(user['user_id'], voice_id)
        return {"voice_id": voice_id, "status": "success"}
    except Exception as e:
        logger.error(f"Voice cloning failed for user_id={user['user_id']}: {e}")
        raise HTTPException(status_code=500, detail="Voice cloning failed.")