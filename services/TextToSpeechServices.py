import whisper
import torch

class TextToSpeechServices:
    def __init__(self, device, audio) -> None:
        self.model = whisper.load_model(name="../models/ggml-small.bin", device=device)
        self.options = whisper.DecodingOptions(language="vie", without_timestamps=True)
        self.audio = audio

    def __audio_processing(self):
        audio = whisper.load_audio(self.audio)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        return mel
        
    def __language_detection(self, mel):
        # detect the spoken language
        _, probs = self.model.detect_language(mel)
        return probs
    
    def generate_text(self):
        mel = self.__audio_processing()
        probs = self.__language_detection(mel)
        self.language = max(probs, key=probs.get)
        # convert speech to texts
        fp16 = False if self.model.device == torch.device("cpu") else True
        # For decoding options, change fp16 to false if you run on CPU
        options = whisper.DecodingOptions(language=self.language, fp16 = fp16)
        result = whisper.decode(self.model, mel, options)

        return result