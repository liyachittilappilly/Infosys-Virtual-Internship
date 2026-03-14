# Sentence-Level Audio Test CLI
# Usage: python quick_test2.py <audio_file>

import sys
import torch
import librosa
import numpy as np
import whisper
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
INDEX_NAME = "speech-therapy"
NAMESPACE = "speech"

whisper_model = whisper.load_model("large-v3")


def score_to_severity(score: float) -> str:
    if score < 0.65:
        return "high"
    if score < 0.8:
        return "medium"
    return "low"


def get_feedback_from_groq(error_obj: dict) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a supportive speech pronunciation coach.",
            },
            {
                "role": "user",
                "content": f"""
The learner mispronounced the word '{error_obj["word"]}'.
The ARPAbet phoneme breakdown for this word is: {error_obj["weak_phoneme"]}.
The similarity score is {error_obj["similarity_score"]:.3f}.
The severity is {error_obj["severity"]}.
Give a short and encouraging pronunciation tip focusing on 1-2 key phonemes.
""",
            },
        ],
        "temperature": 0.2,
        "max_tokens": 120,
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("Groq exception:", e)

    return "Good try. Slow down and exaggerate the key sounds slightly."


def test_audio_sentence(audio_path: str, selected_sentence_id: int):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    wav2vec = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h").to(device)
    wav2vec.eval()

    pc = Pinecone(api_key=API_KEY)
    index = pc.Index(INDEX_NAME)

    waveform, sr = librosa.load(audio_path, sr=16000)

    # Whisper → timestamps only
    result = whisper_model.transcribe(audio_path, word_timestamps=True)
    spoken_sentence = result["text"].strip()
    words = [w for seg in result["segments"] for w in seg.get("words", [])]

    word_scores = []
    word_details = []

    for i, w in enumerate(words):

        start = int(w["start"] * sr)
        end = min(int(w["end"] * sr), len(waveform))
        chunk = waveform[start:end]

        if len(chunk) < 3200:
            chunk = np.pad(chunk, (0, 3200 - len(chunk)), mode="constant")

        inputs = processor(chunk, sampling_rate=sr, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            embedding = (
                wav2vec(**inputs)
                .last_hidden_state.mean(dim=1)
                .squeeze()
                .cpu()
                .numpy()
                .tolist()
            )

        print(f"  [{i + 1}/{len(words)}] Checking word index {i}...")

        match = index.query(
            vector=embedding,
            top_k=1,
            include_metadata=True,
            namespace=NAMESPACE,
            filter={
                "sentence_id": selected_sentence_id,
                "word_index": i
            }
        )

        if match["matches"]:
            best = match["matches"][0]
            metadata = best.get("metadata", {}) or {}

            expected_word = metadata.get("word", "unknown").strip().lower()

            word_scores.append(best["score"])

            word_details.append(
                {
                    "expected_word": expected_word,
                    "phoneme": metadata.get("phonemes", "unknown"),
                    "score": float(best["score"]),
                }
            )
        else:
            print(f"    ⚠ No match found for word index {i}")

    sentence_score = float(np.mean(word_scores)) if word_scores else 0.0

    ai_feedback = "No major pronunciation issues detected."

    if word_details:

        weakest = min(word_details, key=lambda x: x["score"])

        print("\nWord Scores:")
        for d in word_details:
            print(
                f"  word='{d['expected_word']}' | score={d['score']:.4f}"
            )

        print(
            f"\nWeakest Word: '{weakest['expected_word']}' "
            f"(score={weakest['score']:.4f})"
        )

        error_obj = {
            "word": weakest["expected_word"],
            "weak_phoneme": weakest["phoneme"],
            "similarity_score": weakest["score"],
            "severity": score_to_severity(weakest["score"]),
        }

        ai_feedback = get_feedback_from_groq(error_obj)

    print("\n" + "=" * 50)
    print(f"  Whisper (raw) : {spoken_sentence}")
    print(f"  Score         : {sentence_score:.4f} ({sentence_score * 100:.1f}%)")
    print(f"  Feedback      : {ai_feedback}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_test2.py <audio_file>")
        sys.exit(1)

    try:
        # Change sentence_id here depending on which sentence user selected
        test_audio_sentence(sys.argv[1], selected_sentence_id=2)

    except FileNotFoundError:
        print(f"Error: File not found → {sys.argv[1]}")
    except Exception as e:
        print(f"Error: {e}")
        raise