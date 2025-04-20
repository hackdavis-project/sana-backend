import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000/api"


def test_spt_endpoint():
    """
    Test the speech-to-text endpoint.

    Before running this script:
    1. Make sure the backend server is running
    2. Ensure you have a test audio file in MP3, WAV, OGG, FLAC, M4A, or WEBM format
    3. Update the file path below to point to your audio file
    4. Make sure you have a valid auth token (login first via the frontend)
    """
    # Replace with your test audio file
    audio_file_path = "examples/test_audio.mp3"

    # Check if file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: File {audio_file_path} does not exist.")
        return

    # Get auth token
    # For testing, you can manually set a token from a browser session
    # or use your authentication flow to get a token
    auth_token = os.getenv("AUTH_TOKEN", "")
    if not auth_token:
        print(
            "Error: No AUTH_TOKEN found. Please set it in .env or provide it directly."
        )
        return

    # Set up request headers
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Prepare the file for upload
    with open(audio_file_path, "rb") as audio_file:
        files = {
            "file": (
                os.path.basename(audio_file_path),
                audio_file,
                f"audio/{audio_file_path.split('.')[-1].lower()}",
            )
        }

        # Additional parameters
        data = {
            "include_timestamps": "true"  # Set to "false" if you don't need timestamps
        }

        # Make the request
        print(f"Sending {audio_file_path} to Speech-to-Text endpoint...")
        response = requests.post(
            f"{BASE_URL}/spt/transcribe", headers=headers, files=files, data=data
        )

    # Process the response
    if response.status_code == 200:
        result = response.json()
        print("Transcription successful!")
        print(f"Full text: {result['transcription']['full_text']}")
        print(f"Language: {result['transcription']['language']}")
        print("Segments:")
        for i, segment in enumerate(result["transcription"]["segments"]):
            print(
                f"  {i+1}. [{segment['start_time']:.2f}s - {segment['end_time']:.2f}s]: {segment['text']}"
            )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    test_spt_endpoint()
