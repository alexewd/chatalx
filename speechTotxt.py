import whisper

model = whisper.load_model("base")  # можешь взять "small", "medium" или "large" для лучшего качества
result = model.transcribe("d:/Music_dict/radio_records_/250412_0142.mp3 ")
print(result["text"])