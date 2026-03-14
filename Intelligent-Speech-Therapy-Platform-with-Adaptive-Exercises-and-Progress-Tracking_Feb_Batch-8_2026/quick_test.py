"""
Quick Audio Test CLI
Usage: python quick_test.py <audio_file_path>
"""

import sys
import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()
# Configuration

API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "speech-therapy"

def test_audio(audio_path, top_k=5):
    """Quick test of audio file against database"""
    
    print("\n" + "="*60)
    print("🎤 AUDIO SIMILARITY SEARCH")
    print("="*60)
    print(f" Audio file: {audio_path}\n")
    
    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Device: {device}")
    
    # Load models (this takes time on first run)
    print(" Loading Wav2Vec2 model...", end=" ")
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h").to(device)
    model.eval()
    print("✓")
    
    # Connect to Pinecone
    print("🔌 Connecting to Pinecone...", end=" ")
    pc = Pinecone(api_key=API_KEY)
    index = pc.Index(INDEX_NAME)
    print("✓")
    
    # Load and process audio
    print(" Processing audio...", end=" ")
    waveform, sr = librosa.load(audio_path, sr=16000)
    print(f"✓ ({len(waveform)/sr:.2f}s)")
    
    # Generate embedding
    print(" Generating embedding...", end=" ")
    inputs = processor(waveform, sampling_rate=sr, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    embedding = outputs.last_hidden_state.mean(dim=1)
    embedding_list = embedding.squeeze().cpu().numpy().tolist()
    print(f"✓ (768-d)")
    
    # Search database
    print(f" Searching database...", end=" ")
    result = index.query(
        vector=embedding_list,
        top_k=top_k,
        include_metadata=True
    )
    print(f"✓ (found {len(result['matches'])} matches)")
    
    # Display results
    print("\n" + "="*60)
    print(" TOP MATCHES")
    print("="*60)
    
    for i, match in enumerate(result["matches"], 1):
        score = match["score"]
        word = match["metadata"]["word"]
        phonemes = match["metadata"].get("phonemes", "N/A")
        
        # Score indicator
        if score > 0.95:
            emoji = "🟢"
        elif score > 0.85:
            emoji = "🟡"
        elif score > 0.75:
            emoji = "🟠"
        else:
            emoji = "🔴"
        
        print(f"\n{i}. {emoji} Score: {score:.4f} ({score*100:.1f}%)")
        print(f"   Word: '{word}'")
        print(f"   Phonemes: {phonemes}")
    
    print("\n" + "="*60)
    print(" DONE!")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n Error: Please provide an audio file path")
        print("\nUsage:")
        print("  python quick_test.py <audio_file.wav>")
        print("\nExample:")
        print("  python quick_test.py my_recording.wav")
        print("  python quick_test.py 'D:\\\\audio\\\\test.wav'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    try:
        test_audio(audio_file)
    except FileNotFoundError:
        print(f"\n Error: File not found: {audio_file}")
    except Exception as e:
        print(f"\n Error: {e}")
