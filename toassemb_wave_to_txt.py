# Install the assemblyai package by executing the command `pip3 install assemblyai` (macOS) or `pip install assemblyai` (Windows).
# https://www.assemblyai.com/dashboard/overview

""" 9711210@gmail.com
https://www.assemblyai.com/dashboard/signup
9711210

ate5Ngush_ass

6703742c9af245ed889ff041e29ac101 """


# Import the AssemblyAI module
import assemblyai as aai

# Your API token is already set here
aai.settings.api_key = "6703742c9af245ed889ff041e29ac101"

# Create a transcriber object.
transcriber = aai.Transcriber()

# If you have a local audio file, you can transcribe it using the code below.
# Make sure to replace the filename with the path to your local audio file.
transcript = transcriber.transcribe("d:/Music_dict/radio_records_/radio2.wav")

# Alternatively, if you have a URL to an audio file, you can transcribe it with the following code.
# Uncomment the line below and replace the URL with the link to your audio file.
# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/espn-bears.m4a")

# After the transcription is complete, the text is printed out to the console.
print(transcript.text)