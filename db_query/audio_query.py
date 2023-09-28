import io
import librosa
from fastapi import UploadFile

async def read_audio_metadata(file: UploadFile):
    """Read metadata of an audio file uploaded by the client."""

    # Read the contents of the uploaded file.
    audio_content = await file.read()

    # Extract file name and type from the UploadFile object.
    file_name = file.filename
    file_type = file.content_type
    file_size = file.size

    # Create a BytesIO object to hold the audio data.
    audio_io = io.BytesIO(audio_content)

    # Read the audio file using Librosa to get metadata.
    audio_data, sample_rate = librosa.load(audio_io, sr=None)

    # Get the duration of the audio file.
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    # Return the metadata including file name and type.
    return {
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "sample_rate": sample_rate,
        "duration": duration

    }
