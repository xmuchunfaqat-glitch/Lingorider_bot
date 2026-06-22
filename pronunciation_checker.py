"""
Talaffuzni baholash mantiqi.
Whisper orqali eshitilgan matnni maqsadli matn bilan solishtiradi va
foiz ko'rinishida moslik darajasini (score) chiqaradi.
"""
import re
from rapidfuzz import fuzz


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text


def score_pronunciation(target_text: str, heard_text: str) -> dict:
    """
    Returns: {"score": float (0-100), "is_correct": bool, "heard": str}
    score >= 85   -> juda yaxshi
    score 60-84   -> o'rtacha, mashq kerak
    score < 60    -> talaffuz noto'g'ri / tushunarsiz
    """
    norm_target = _normalize(target_text)
    norm_heard = _normalize(heard_text) if heard_text else ""

    if not norm_heard:
        return {"score": 0.0, "is_correct": False, "heard": heard_text or ""}

    score = fuzz.ratio(norm_target, norm_heard)
    return {
        "score": round(score, 1),
        "is_correct": score >= 85,
        "heard": heard_text,
    }


def feedback_tier(score: float) -> str:
    if score >= 85:
        return "great"
    elif score >= 60:
        return "ok"
    return "bad"
