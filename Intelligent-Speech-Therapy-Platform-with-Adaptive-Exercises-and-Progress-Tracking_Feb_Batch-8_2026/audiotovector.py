import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Load model + processor
processor = Wav2Vec2Processor.from_pretrained(
    "facebook/wav2vec2-base-960h"
)
model = Wav2Vec2Model.from_pretrained(
    "facebook/wav2vec2-base-960h"
)
model.eval()

# Load audio (MUST be 16kHz)
audio_path = "D:\\INFOSYS\\audioraw.wav"
audio, sr = librosa.load(audio_path, sr=16000)

# Preprocess
inputs = processor(
    audio,
    sampling_rate=16000,
    return_tensors="pt",
    padding=True
)

# Generate embeddings
with torch.no_grad():
    outputs = model(**inputs)

# Time-level embeddings
hidden_states = outputs.last_hidden_state
# shape: [1, T, 768]

# Convert to single vector (mean pooling)
embedding = hidden_states.mean(dim=1)

print("Embedding shape:", embedding.shape)
