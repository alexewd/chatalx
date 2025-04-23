import assemblyai as aai

""" 9711210@gmail.com
https://www.assemblyai.com/dashboard/signup
9711210

ate5Ngush_ass

6703742c9af245ed889ff041e29ac101 """


# https://www.assemblyai.com/dashboard/overview

aai.settings.api_key = "6703742c9af245ed889ff041e29ac101"

# You can use a local filepath:
audio_file = "d:/Music_dict/radio_records_/radio2.mp3"

# Or use a publicly-accessible URL:
#""" audio_file = (
#    "https://assembly.ai/wildfires.mp3"
#)
 #"""

transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_file)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed")


print(transcript.text)