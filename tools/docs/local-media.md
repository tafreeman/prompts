# Local Media (`local_media.py`)

> **Multi-modal AI for image generation, speech-to-text, and upscaling** - All local, no API keys required.

---

## ⚡ Quick Start

```powershell
# Generate image
python tools/local_media.py image "A sunset over mountains" -o sunset.png

# Transcribe audio
python tools/local_media.py transcribe recording.wav -o transcript.txt

# Upscale image
python tools/local_media.py upscale low_res.png -o high_res.png
```

---

## Capabilities

| Feature | Model | Hardware | Output |
|---------|-------|----------|--------|
| Image Generation | Stable Diffusion | GPU | PNG/JPG |
| Speech-to-Text | Whisper | CPU | TXT/SRT |
| Image Upscaling | ESRGAN | GPU | PNG |

---

## Image Generation (Stable Diffusion)

### CLI Usage

```powershell
# Basic generation
python tools/local_media.py image "A sunset over mountains" -o sunset.png

# Custom dimensions
python tools/local_media.py image "Cyberpunk city" --width 768 --height 512

# More inference steps (higher quality, slower)
python tools/local_media.py image "Fantasy landscape" --steps 75

# Negative prompt
python tools/local_media.py image "A cat" --negative "blurry, low quality"

# With seed for reproducibility
python tools/local_media.py image "Abstract art" --seed 42
```

### Python API

```python
from tools.local_media import generate_image

# Basic generation
generate_image("A cat wearing a hat", output_path="cat.png")

# With options
generate_image(
    prompt="A futuristic city skyline",
    output_path="city.png",
    width=768,
    height=512,
    steps=50,
    negative_prompt="blurry, distorted"
)
```

---

## Speech-to-Text (Whisper)

### CLI Usage

```powershell
# Basic transcription
python tools/local_media.py transcribe recording.wav -o transcript.txt

# Specify language
python tools/local_media.py transcribe audio.mp3 --language en

# Different model size (tiny, base, small, medium, large)
python tools/local_media.py transcribe meeting.wav --model medium

# Output with timestamps (SRT format)
python tools/local_media.py transcribe video.mp4 --srt -o subtitles.srt
```

### Model Sizes

| Model | Size | Speed | Accuracy | VRAM |
|-------|------|-------|----------|------|
| `tiny` | 39M | Fastest | Lower | 1GB |
| `base` | 74M | Fast | Good | 1GB |
| `small` | 244M | Medium | Better | 2GB |
| `medium` | 769M | Slow | High | 5GB |
| `large` | 1550M | Slowest | Best | 10GB |

### Python API

```python
from tools.local_media import transcribe_audio

# Basic transcription
text = transcribe_audio("meeting.wav")
print(text)

# With options
text = transcribe_audio(
    audio_path="interview.mp3",
    model_size="small",
    language="en"
)
```

---

## Image Upscaling (ESRGAN)

### CLI Usage

```powershell
# 4x upscale
python tools/local_media.py upscale low_res.png -o high_res.png

# Specify scale factor
python tools/local_media.py upscale photo.jpg --scale 2 -o photo_2x.png
```

### Python API

```python
from tools.local_media import upscale_image

# Basic upscale (4x)
upscale_image("photo.jpg", output_path="photo_4x.png")

# Custom scale
upscale_image("image.png", output_path="image_2x.png", scale=2)
```

---

## Supported Formats

### Input Formats

| Type | Formats |
|------|---------|
| Audio | .wav, .mp3, .m4a, .flac, .ogg |
| Image | .png, .jpg, .jpeg, .webp, .bmp |
| Video | .mp4 (audio extraction only) |

### Output Formats

| Type | Formats |
|------|---------|
| Image | .png, .jpg |
| Text | .txt, .srt |

---

## Model Cache Location

Models are cached at:

```
~/.cache/aigallery/
```

---

## Troubleshooting

### "CUDA out of memory"

```powershell
# Use smaller steps
python tools/local_media.py image "..." --steps 25

# Use smaller dimensions
python tools/local_media.py image "..." --width 512 --height 512
```

### "Whisper model not found"

```powershell
# Models are downloaded automatically on first use
# Check cache:
dir $HOME\.cache\aigallery\whisper-*
```

### Slow generation

- Use GPU if available (CUDA/DirectML)
- Reduce inference steps (`--steps 25`)
- Use smaller model for Whisper (`--model tiny`)

---

## See Also

- [local-model.md](./local-model.md) - Text generation with ONNX
- [../README.md](../README.md) - Tools overview
