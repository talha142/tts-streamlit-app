# synthesize.py
import re
import os
from TTS.api import TTS
from pydub import AudioSegment
import tempfile

def split_text_to_chunks(text, max_chars=1200):
    # split on sentence boundaries, but ensure chunk <= max_chars
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            if len(s) > max_chars:
                # fallback: hard split
                for i in range(0, len(s), max_chars):
                    chunks.append(s[i:i+max_chars])
                current = ""
            else:
                current = s
    if current:
        chunks.append(current)
    return chunks

def synthesize_with_coqui(text, model_name=None, out_path="output.wav", temp_dir=None):
    """
    text: full text
    model_name: e.g., "tts_models/en/ljspeech/something" or None for default
    Returns path to final concatenated wav
    """
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()
    chunks = split_text_to_chunks(text, max_chars=1200)
    # load model (this will download model on first run)
    if model_name:
        tts = TTS(model_name)
    else:
        tts = TTS.list_models()[0]
        tts = TTS(tts)

    part_paths = []
    for i, chunk in enumerate(chunks):
        part_file = os.path.join(temp_dir, f"part_{i}.wav")
        # synthesize chunk to file
        tts.tts_to_file(text=chunk, file_path=part_file)
        part_paths.append(part_file)

    # concatenate with pydub
    combined = None
    for p in part_paths:
        seg = AudioSegment.from_wav(p)
        if combined is None:
            combined = seg
        else:
            combined += seg

    combined.export(out_path, format="wav")
    return out_path
