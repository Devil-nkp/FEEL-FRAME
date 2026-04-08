# 🎬 FEEL-FRAME – Emotion-Driven AI Video Generation Platform

FEEL-FRAME is an innovative web application that transforms user emotions and narratives into stunning cinematic AI-generated videos using emotion detection, SDXL image generation, and Stable Video Diffusion technology for immersive visual storytelling.

---

## Overview

This system combines sentiment analysis with multi-stage content generation to create emotionally-resonant visual experiences through AI-powered image and video synthesis triggered by detected emotional context.

Instead of relying solely on static content creation, FEEL-FRAME:

1. Analyzes user emotions and sentiment from text input
2. Generates contextually appropriate visual styles based on detected emotions
3. Creates stunning AI-powered images using Stable Diffusion XL
4. Converts images into cinematic videos with Stable Video Diffusion
5. Enables custom image uploads for personalized storytelling
6. Provides real-time memory optimization for seamless performance
7. Delivers high-quality 1024x576 videos with emotion-driven aesthetics

---

## Architecture

User Text Input & Image Upload
→ Emotion Detection & Analysis (DistilRoBERTa)
→ Style Mapping Based on Detected Emotion
→ AI Image Generation (SDXL)
→ Image Resizing & Optimization (1024x576)
→ Video Generation (Stable Video Diffusion)
→ Output Video Delivery
→ Memory Management & Cleanup

---

## ⚙️ Tech Stack

- **HTML** (89.9%)
- **Python** (10.1%)
- **Flask** (Web Framework)
- **Hugging Face Inference API** (Image & Emotion Models)
- **Stable Diffusion XL** (AI Image Generation)
- **Stable Video Diffusion (SVD)** (Video Generation)
- **DistilRoBERTa** (Emotion Detection)
- **Gradio Client** (Video Generation Integration)
- **Pillow (PIL)** (Image Processing)
- **Python-dotenv** (Environment Configuration)
- **Gunicorn** (Production Server)

---

## Key Features

- **Emotion Detection** – Analyzes user text to detect emotions (joy, sadness, fear, love, anger, neutral)
- **Emotion-Driven Styling** – Automatically applies visual styles matching detected emotions
- **AI Image Generation** – Creates stunning 8K cinematic images from text descriptions
- **Custom Image Upload** – Users can upload their own images for video generation
- **Video Generation** – Converts images into smooth, high-quality MP4 videos
- **Image Optimization** – Automatic resizing to 1024x576 for optimal video quality
- **Memory Management** – Advanced garbage collection for efficient resource utilization
- **Real-Time Processing** – Fast emotion detection and content generation pipeline
- **Responsive UI** – Modern, interactive web interface for seamless user experience
- **JPEG Optimization** – Automatic quality optimization (85%) to reduce file sizes
- **Error Handling** – Robust error handling with graceful fallbacks
- **Static File Management** – Organized generation of videos and images

---

## Live Demo

🔗 Coming Soon

---

## Installation (Local Setup)

```bash
git clone https://github.com/Devil-nkp/FEEL-FRAME.git
cd FEEL-FRAME
pip install -r requirements.txt
```

Set up your environment:

```bash
# Create .env file in the root directory
echo "HF_TOKEN=your_huggingface_token_here" > .env

# Get your Hugging Face token from: https://huggingface.co/settings/tokens
```

Create required directories:

```bash
mkdir -p static/generated
mkdir -p templates
```

Run the application:

```bash
# Development mode
python app.py

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Open your browser at `http://localhost:5000`

---

## Environment Setup

Create a `.env` file in the root directory:

```bash
HF_TOKEN=your_huggingface_api_token
FLASK_ENV=development
FLASK_DEBUG=true
PORT=5000
```

To get a Hugging Face token:
1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "read" access
3. Copy the token to your `.env` file

---

## Project Structure

```
FEEL-FRAME/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── templates/
│   ├── index.html            # Main web interface (89.9% HTML)
│   └── results.html          # Results display page
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   ├── js/
│   │   └── script.js         # Frontend logic
│   └── generated/            # Generated images and videos
└── README.md
```

---

## Emotion-to-Style Mapping

| Emotion | Visual Style |
|---------|-------------|
| **Joy** | Bright, vibrant, warm lighting, happy atmosphere |
| **Sadness** | Rain, dark blue tones, cinematic, gloomy, lonely |
| **Fear** | Misty, horror, dark, cold tones, mysterious |
| **Love** | Romantic, soft focus, pink and red tones, dreamy |
| **Anger** | Intense, red, fire, high contrast, dramatic |
| **Neutral** | Cinematic, photorealistic |

---

## API Endpoints

```
GET  /                    # Home page with main interface
POST /generate            # Generate image and video from text/image
                          # Parameters:
                          #   - text: User's narrative (required)
                          #   - image: Optional uploaded image
                          # Returns: JSON with video URL and detected emotion
```

---

## Usage Example

**Frontend (HTML/JavaScript):**

```javascript
const formData = new FormData();
formData.append('text', 'A beautiful sunset over the ocean');
formData.append('image', imageFile); // Optional

fetch('/generate', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('Video URL:', data.video_url);
    console.log('Detected Emotion:', data.emotion);
    // Display video to user
})
.catch(error => console.error('Error:', error));
```

---

## Key Technologies Explained

### 1. **DistilRoBERTa for Emotion Detection**
- Pre-trained transformer model for emotion classification
- Detects: joy, sadness, fear, love, anger, neutral
- Lightweight and fast inference

### 2. **Stable Diffusion XL (SDXL)**
- State-of-the-art text-to-image generation
- Creates 8K quality cinematic images
- Fine-tuned prompts based on detected emotions

### 3. **Stable Video Diffusion (SVD)**
- Converts images to smooth video sequences
- Generates 10-frame videos at optimal quality
- Processes 1024x576 resolution images

### 4. **Memory Management**
- Garbage collection after each operation
- Image format optimization (JPEG at 85% quality)
- Client session cleanup for production stability

---

## Performance Optimization

- **Image Compression**: JPEG format with 85% quality reduces size without noticeable quality loss
- **Batch Cleanup**: Memory is cleaned between major operations
- **Efficient Resizing**: Lanczos resampling for high-quality image scaling
- **Gradio Client Lifecycle**: Fresh client initialization per request prevents memory leaks

---

## Future Improvements

- Add multiple language support for emotion detection
- Implement video style filters (noir, vintage, futuristic)
- Add music generation based on detected emotions
- Create user accounts and video history
- Implement video sharing and social features
- Add batch processing for multiple videos
- Integrate with cloud storage (AWS S3, Google Cloud)
- Add advanced video editing features
- Implement real-time video preview
- Add subtitle generation based on emotions
- Create mobile app version
- Add animation presets for different emotions

---

## Requirements

- Python 3.8+
- 8GB RAM minimum (16GB recommended for video generation)
- Active internet connection for Hugging Face API
- Hugging Face API token
- 5GB disk space for model caching

---

## Author

**Naveenkumar G** (Devil-nkp)
- Full-Stack Developer
- AI/ML Specialist

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ to transform emotions into cinematic visual stories**
