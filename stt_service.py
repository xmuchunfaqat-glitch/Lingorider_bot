"""
Bepul, lokal ishlaydigan nutqni matnga aylantirish (STT) xizmati — faster-whisper.
Hech qanday tashqi API kalit talab qilmaydi, model bir marta yuklab olinadi va
keyin kompyuteringizda (CPU) lokal ishlaydi.
"""
from faster_whisper import WhisperModel

from config import WHISPER_MODEL_SIZE

_model: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        # compute_type="int8" -> CPU'da tezroq va kam xotira sarflaydi
        _model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path: str, language_whisper_code: str) -> str:
    """
    Audio fayldan matnni aniqlaydi. language_whisper_code beriladi, chunki
    foydalanuvchi qaysi tilda gapirayotgani oldindan ma'lum (mashq tili).
    """
    model = _get_model()
    segments, _info = model.transcribe(
        audio_path,
        language=language_whisper_code,
        beam_size=5,
        vad_filter=True,
    )
    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()
