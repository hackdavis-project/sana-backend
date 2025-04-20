# Speech-to-Text (SPT) API

This API provides speech-to-text transcription using Google's Gemini AI model.

## Endpoint

### POST `/api/spt/transcribe`

Transcribes an audio file to text with optional timestamps.

#### Authentication

Requires a valid authentication token.

#### Request

- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `file` (required): Audio file in one of the supported formats (MP3, WAV, M4A, OGG, FLAC, WEBM)
  - `include_timestamps` (optional, default: true): Whether to include timestamps for each text segment

#### Response

```json
{
  "transcription": {
    "full_text": "This is the complete transcribed text from the audio file.",
    "segments": [
      {
        "text": "This is the first segment.",
        "start_time": 0.0,
        "end_time": 2.5
      },
      {
        "text": "This is the second segment.",
        "start_time": 2.6,
        "end_time": 5.1
      }
    ],
    "language": "en"
  },
  "status": "success"
}
```

#### Error Responses

- **400 Bad Request**: Unsupported file format or invalid request
- **401 Unauthorized**: Missing or invalid authentication token
- **500 Internal Server Error**: Processing error

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/spt/transcribe" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -F "file=@path/to/your/audio.mp3" \
  -F "include_timestamps=true"
```

### Using Python

See the example script in `examples/test_spt.py`:

```python
import requests

# Set up the request
files = {"file": open("audio.mp3", "rb")}
headers = {"Authorization": "Bearer YOUR_AUTH_TOKEN"}
data = {"include_timestamps": "true"}

# Make the request
response = requests.post(
    "http://localhost:8000/api/spt/transcribe",
    headers=headers,
    files=files,
    data=data
)

# Process the response
if response.status_code == 200:
    result = response.json()
    print(result["transcription"]["full_text"])
```

## Notes

- Transcription quality depends on audio clarity and Gemini's speech recognition capabilities
- Audio files should not exceed 20MB
- For best results, use clear audio with minimal background noise
- Supports multiple languages (auto-detected by Gemini)
- The API is designed to handle sensitive content with appropriate care

## Integration with DavisHacks Frontend

This endpoint can be integrated with the DavisHacks frontend to allow users to:

1. Record journal entries by voice instead of typing
2. Process voice notes for later text analysis
3. Make the application more accessible to users who prefer speaking over writing

To implement this in the frontend, you can use standard HTML file inputs or modern browser APIs for recording audio directly in the application.
