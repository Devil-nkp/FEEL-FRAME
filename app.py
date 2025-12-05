import os
import uuid
import shutil
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
from gradio_client import Client as GrClient, handle_file
from PIL import Image
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# 2. Setup Flask App
app = Flask(__name__)

# 3. Configuration
# We use SDXL for high-quality image generation
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
# We use a distinct model for emotion detection
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
# The video generation space
VIDEO_SPACE = "multimodalart/stable-video-diffusion"

# 4. Ensure directories exist
os.makedirs("static/generated", exist_ok=True)

# 5. Initialize Hugging Face Client
hf_client = InferenceClient(token=HF_TOKEN)

def analyze_emotion(text):
    """Detects the emotion of the user's story."""
    try:
        if not text: return "neutral"
        # Call the API for text classification
        response = hf_client.text_classification(text, model=EMOTION_MODEL)
        # Sort by highest score
        top_emotion = sorted(response, key=lambda x: x['score'], reverse=True)[0]
        return top_emotion['label']
    except Exception as e:
        print(f"Emotion Analysis Failed: {e}")
        return "neutral"

def resize_for_video(image_path):
    """
    SVD requires specific dimensions (1024x576).
    This function resizes the input to prevent errors.
    """
    img = Image.open(image_path)
    # Resize using Lanczos for high quality
    img = img.resize((1024, 576), Image.Resampling.LANCZOS)
    
    # Save with unique name
    filename = f"resized_{uuid.uuid4()}.png"
    save_path = os.path.join("static/generated", filename)
    img.save(save_path)
    return save_path

@app.route('/')
def home():
    """Serves the HTML page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Main Logic: Emotion -> Image -> Video"""
    try:
        user_text = request.form.get('text')
        user_image = request.files.get('image')
        
        print(f"🚀 Processing Request: {user_text[:50]}...")

        # --- Step A: Analyze Emotion ---
        emotion = analyze_emotion(user_text)
        print(f"🧠 Emotion Detected: {emotion}")

        # --- Step B: Get/Generate Base Image ---
        if user_image:
            # User uploaded an image
            base_filename = f"upload_{uuid.uuid4()}.png"
            base_path = os.path.join("static/generated", base_filename)
            user_image.save(base_path)
        else:
            # Generate image from text using SDXL
            style_map = {
                "joy": "bright, vibrant, warm lighting, happy atmosphere",
                "sadness": "rain, dark blue tones, cinematic, gloomy, lonely",
                "fear": "misty, horror, dark, cold tones, mysterious",
                "love": "romantic, soft focus, pink and red tones, dreamy",
                "anger": "intense, red, fire, high contrast, dramatic",
                "surprise": "surreal, wide angle, dramatic lighting",
                "neutral": "cinematic, photorealistic, balanced lighting"
            }
            style = style_map.get(emotion, "cinematic")
            
            full_prompt = f"{user_text}, {style}, 8k, highly detailed, masterpiece, movie scene"
            print(f"🎨 Generating Image with prompt: {full_prompt}")
            
            generated_img = hf_client.text_to_image(full_prompt, model=IMAGE_MODEL)
            
            base_filename = f"gen_{uuid.uuid4()}.png"
            base_path = os.path.join("static/generated", base_filename)
            generated_img.save(base_path)

        # --- Step C: Resize for SVD ---
        # This is critical for the video model to accept the image
        resized_path = resize_for_video(base_path)

        # --- Step D: Generate Video ---
        print("🎬 Sending to Video Server (SVD)...")
        
        # Initialize Gradio Client (No token needed for public space usually, helps avoid version errors)
        client = GrClient(VIDEO_SPACE)
        
        result = client.predict(
            handle_file(resized_path), # Input Image
            0,                         # Motion Bucket ID
            10,                        # FPS
            api_name="/video"          # Endpoint
        )
        
        # result[0]['video'] is a temp path. Move it to our static folder.
        temp_video_path = result[0]['video']
        final_video_name = f"dream_{uuid.uuid4()}.mp4"
        final_video_path = os.path.join("static/generated", final_video_name)
        
        shutil.move(temp_video_path, final_video_path)
        print(f"✅ Video Saved: {final_video_path}")

        return jsonify({
            "status": "success",
            "video_url": f"/static/generated/{final_video_name}",
            "emotion": emotion,
            "image_url": f"/static/generated/{base_filename}"
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
