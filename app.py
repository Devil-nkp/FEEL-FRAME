import os
import uuid
import shutil
import gc  # Garbage Collector for memory management
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
# SDXL for Image Generation
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
# Emotion Detection Model
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
# Video Generation Space
VIDEO_SPACE = "multimodalart/stable-video-diffusion"

# 4. Ensure directories exist
os.makedirs("static/generated", exist_ok=True)

# 5. Initialize Clients
# We define clients globally, but we will manage their memory usage carefully
hf_client = InferenceClient(token=HF_TOKEN)

def cleanup_memory():
    """Forces Python to release unused memory immediately."""
    gc.collect()

def analyze_emotion(text):
    """Detects the emotion of the user's story."""
    try:
        if not text: return "neutral"
        response = hf_client.text_classification(text, model=EMOTION_MODEL)
        top_emotion = sorted(response, key=lambda x: x['score'], reverse=True)[0]
        
        # Cleanup
        del response
        cleanup_memory()
        
        return top_emotion['label']
    except Exception as e:
        print(f"Emotion Analysis Failed: {e}")
        return "neutral"

def resize_for_video(image_path):
    """
    Resizes image to 1024x576 for SVD.
    Saves as JPEG (smaller) to save RAM during upload.
    """
    img = Image.open(image_path)
    
    # Convert to RGB to ensure we can save as JPG (removes Alpha channel if PNG)
    img = img.convert("RGB")
    
    # Resize using Lanczos for quality
    img = img.resize((1024, 576), Image.Resampling.LANCZOS)
    
    # Save as JPG with optimization to keep file size low
    filename = f"resized_{uuid.uuid4()}.jpg"
    save_path = os.path.join("static/generated", filename)
    img.save(save_path, quality=85, optimize=True)
    
    # Close image to free memory
    img.close()
    cleanup_memory()
    
    return save_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        cleanup_memory() # Start fresh
        
        user_text = request.form.get('text')
        user_image = request.files.get('image')
        
        print(f"🚀 Processing Request...")

        # --- Step A: Analyze Emotion ---
        emotion = analyze_emotion(user_text)
        print(f"🧠 Emotion Detected: {emotion}")

        # --- Step B: Get/Generate Base Image ---
        if user_image:
            base_filename = f"upload_{uuid.uuid4()}.jpg"
            base_path = os.path.join("static/generated", base_filename)
            # Save uploaded file directly
            user_image.save(base_path)
        else:
            style_map = {
                "joy": "bright, vibrant, warm lighting, happy atmosphere",
                "sadness": "rain, dark blue tones, cinematic, gloomy, lonely",
                "fear": "misty, horror, dark, cold tones, mysterious",
                "love": "romantic, soft focus, pink and red tones, dreamy",
                "anger": "intense, red, fire, high contrast, dramatic",
                "neutral": "cinematic, photorealistic"
            }
            style = style_map.get(emotion, "cinematic")
            
            full_prompt = f"{user_text}, {style}, 8k, highly detailed, movie scene"
            print(f"🎨 Generating Image...")
            
            # Generate Image
            generated_img = hf_client.text_to_image(full_prompt, model=IMAGE_MODEL)
            
            base_filename = f"gen_{uuid.uuid4()}.jpg"
            base_path = os.path.join("static/generated", base_filename)
            
            # Save as JPG for smaller size
            generated_img.save(base_path, quality=85)
            
            # Delete object from memory
            del generated_img
            cleanup_memory()

        # --- Step C: Resize for SVD ---
        resized_path = resize_for_video(base_path)

        # --- Step D: Generate Video ---
        print("🎬 Connecting to Video Server (SVD)...")
        
        # Initialize Client freshly for this request
        client = GrClient(VIDEO_SPACE)
        
        result = client.predict(
            handle_file(resized_path), 
            0,                         
            10,                        
            api_name="/video"          
        )
        
        # Cleanup Client immediately
        del client
        cleanup_memory()
        
        # Handle Result
        temp_video_path = result[0]['video']
        final_video_name = f"dream_{uuid.uuid4()}.mp4"
        final_video_path = os.path.join("static/generated", final_video_name)
        
        shutil.move(temp_video_path, final_video_path)
        print(f"✅ Video Saved!")

        return jsonify({
            "status": "success",
            "video_url": f"/static/generated/{final_video_name}",
            "emotion": emotion
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        # Final cleanup no matter what
        cleanup_memory()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
