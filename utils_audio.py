# utils_audio.py
from pydub import AudioSegment

def concat_wavs(wav_paths, out_path):
    combined = None
    for p in wav_paths:
        seg = AudioSegment.from_file(p)
        combined = seg if combined is None else combined + seg
    combined.export(out_path, format="wav")
    return out_path
