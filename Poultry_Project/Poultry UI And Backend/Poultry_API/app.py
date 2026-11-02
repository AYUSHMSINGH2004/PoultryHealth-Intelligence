import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os
import io
import base64
import traceback
from dotenv import load_dotenv

# Suppress verbose TensorFlow logging before importing TF
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load environment variables from .env if present
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('Agg') # Forces matplotlib to run headless without a GUI
import matplotlib.pyplot as plt
import PIL.Image
import google.generativeai as genai

app = FastAPI(
    title="PoultryHealth Intelligence API",
    description="Hierarchical Deep Learning and Grounded Generative AI for Poultry Disease Diagnosis"
)

@app.get("/")
async def root():
    return {
        "status": "ok", 
        "system": "PoultryHealth Intelligence",
        "description": "Hierarchical Deep Learning and Grounded Generative AI for Poultry Disease Diagnosis",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    }

# Allow frontend to communicate with this backend across all local and networked ports
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOUNCER_PATH = os.path.join(BASE_DIR, 'poultry_bouncer_final.keras')
DOCTOR_PATH = os.path.join(BASE_DIR, 'poultry_doctor_final.keras')

def get_api_key():
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = get_api_key()
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("[OK] Google Gemini API key configured.")
else:
    print("[WARNING] GEMINI_API_KEY is not set. Please set it in Poultry_API/.env or environment variables.")

def generate_gemini_content(contents):
    """Attempt generation with primary model and gracefully fallback to available alternates."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please add your Gemini API Key in Poultry_API/.env")
    
    genai.configure(api_key=api_key)
    
    primary_model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    models_to_try = [
        primary_model_name,
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.5-flash",
        "gemini-1.5-flash",
    ]
    # Remove duplicates while preserving order
    models_to_try = list(dict.fromkeys([m for m in models_to_try if m]))
    
    last_err = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(contents)
        except Exception as e:
            last_err = e
            print(f"Warning: Model {model_name} failed: {e}. Trying alternate model...")
            continue
    raise last_err

print(f"Loading Keras Models from {BASE_DIR}... (This might take a few seconds)")
model_a_final = tf.keras.models.load_model(BOUNCER_PATH)
model_b_final = tf.keras.models.load_model(DOCTOR_PATH)
print("Models Loaded Successfully!")

# --- UPGRADED VETERINARY KNOWLEDGE BASE (ANTIMICROBIAL STEWARDSHIP COMPLIANT) ---
disease_suggestions = {
    "Healthy": "Status: Clear.\n- Action: No medical intervention required.\n- Prevention: Maintain strict daily biosecurity, ensure dry bedding, and provide ad-libitum access to clean water and balanced feed.",
    "Bumblefoot": "Status: Pododermatitis (Staphylococcal Abscess).\n- Immediate: Move bird to a soft-bedded, dry isolation enclosure.\n- Treatment: Soak affected foot in warm Epsom salt bath (15 min). Cleanse with antiseptic wash, apply topical salve, and bandage securely with vet wrap. Consult a veterinarian if swelling is severe or chronic.\n- Prevention: Inspect roosting perches, remove sharp splinters, and maintain dry, clean coop litter.",
    "CRD": "Status: Chronic Respiratory Disease (Mycoplasma) - HIGHLY CONTAGIOUS.\n- Immediate: Quarantine affected bird immediately far from the main flock to arrest aerosol transmission.\n- Clinical Action: Consult a licensed avian veterinarian for confirmatory diagnosis and lawful prescription antimicrobial therapy. Do not self-administer unguided antibiotics.\n- Biosecurity & Care: Drastically improve coop ventilation to lower ammonia levels. Provide supportive electrolytes in clean water.",
    "Foul Pox": "Status: Viral Cutaneous Dermatosis (Avipoxvirus) - SLOW SPREADING.\n- Immediate: Isolate affected birds to prevent transmission via pecking and mosquito vectors.\n- Treatment: No antiviral cure exists. Apply dilute povidone-iodine to dry cutaneous scabs to avert secondary bacterial dermatitis.\n- Care: Provide warm, stress-free shelter and soft mash feed to encourage nutrition.",
    "Infectious coryza": "Status: Acute Respiratory Bacterial Infection (Avibacterium) - HIGHLY CONTAGIOUS.\n- Immediate: Enforce strict, isolated quarantine immediately.\n- Clinical Action: Consult a licensed avian veterinarian urgently for flock-level diagnostic confirmation and prescription therapy.\n- Warning: Recovered birds frequently remain asymptomatic lifelong carriers. Disinfect feeders, drinkers, and housing thoroughly."
}

doctor_classes = ['Bumblefoot', 'CRD', 'Foul Pox', 'Infectious coryza']
all_classes = ['Healthy'] + doctor_classes
concern_threshold = 5.0 
OPEN_SET_CONFIDENCE_THRESHOLD = 0.40 # 40% maximum softmax probability threshold for abstention 

def image_to_base64(pil_image):
    """Helper function to convert PIL images to Base64 strings for the frontend."""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_str}"

@app.post("/analyze")
async def analyze_poultry(
    image: UploadFile = File(None),
    file: UploadFile = File(None)
):
    try:
        # Check API key first
        api_key = get_api_key()
        if not api_key:
            return {
                "status": "error",
                "message": "Google Gemini API key is missing. Please set GEMINI_API_KEY in Poultry_API/.env or in your environment."
            }

        upload_file = image if image is not None else file
        if upload_file is None:
            return {
                "status": "error",
                "message": "No image file uploaded. Please upload an image using field name 'image' or 'file'."
            }

        # Read the uploaded file into memory
        contents = await upload_file.read()
        pil_img = PIL.Image.open(io.BytesIO(contents)).convert('RGB')
        
        # --- 1. THE MULTIMODAL SECURITY GUARD ---
        try:
            security_prompt = """
            You are an AI security filter for a veterinary application. Look at this image. 
            Is it an image of a whole poultry bird, a specific poultry body part (like a foot, beak, or comb), 
            or a poultry internal organ? 
            You must ignore humans, dogs, cats, cars, and unrelated objects. 
            Reply with exactly one word: 'TRUE' if it is poultry-related, or 'FALSE' if it is not.
            """
            security_response = generate_gemini_content([security_prompt, pil_img])
            if "TRUE" not in security_response.text.strip().upper():
                return {"status": "error", "message": "Access Denied: Image does not appear to contain a poultry bird, body part, or organ."}
        except Exception as filter_err:
            print(f"[SECURITY] Filter warning: {filter_err}. Proceeding to medical pipeline.")

        # --- 2. CUSTOM MEDICAL PIPELINE ---
        img_resized = pil_img.resize((224, 224))
        img_array = tf.keras.utils.img_to_array(img_resized)
        img_array = tf.expand_dims(img_array, 0)
        
        bouncer_prediction = model_a_final.predict(img_array, verbose=0)[0][0] 
        doctor_prediction = model_b_final.predict(img_array, verbose=0)[0]     

        p_sick = float(bouncer_prediction)
        p_healthy = 1.0 - p_sick
        unified_probs = [p_healthy * 100] + [p_sick * float(d_prob) * 100 for d_prob in doctor_prediction]

        detected_conditions = []
        open_set_alert = False
        if p_sick < 0.5:
            final_diagnosis = "Healthy"
            confidence = float(p_healthy * 100)
            active_model = model_a_final
            detected_conditions.append(f"PRIMARY STATUS: Healthy ({confidence:.1f}%)")
        else:
            predicted_index = int(np.argmax(doctor_prediction))
            top_disease_score = float(doctor_prediction[predicted_index])
            final_diagnosis = doctor_classes[predicted_index]
            confidence = float(unified_probs[predicted_index + 1])
            active_model = model_b_final
            if top_disease_score < OPEN_SET_CONFIDENCE_THRESHOLD:
                open_set_alert = True
                detected_conditions.append(f"PRIMARY DIAGNOSIS: {final_diagnosis} ({confidence:.1f}%) [⚠️ ATYPICAL / LOW CONFIDENCE]")
                detected_conditions.append(f"⚠️ ATYPICAL PATHOLOGY ALERT: Doctor confidence ({top_disease_score*100:.1f}%) is below the open-set abstention threshold (40.0%). Presentation may represent an atypical case or unclassified avian condition; clinical laboratory confirmation is recommended.")
            else:
                detected_conditions.append(f"PRIMARY DIAGNOSIS: {final_diagnosis} ({confidence:.1f}%)")

        distribution_dict = {all_classes[i]: round(unified_probs[i], 1) for i in range(5)}

        for i, disease in enumerate(doctor_classes):
            disease_prob = unified_probs[i + 1]
            if disease != final_diagnosis and disease_prob >= concern_threshold:
                detected_conditions.append(f"SECONDARY RISK: {disease} ({disease_prob:.1f}%)")

        # --- 3. THE GROUNDED AI SYNTHESIZER ---
        conditions_str = "\n".join(detected_conditions)
        guidelines_str = "\n".join([f"- {k}: {v}" for k, v in disease_suggestions.items()])
        
        final_medical_report = ""
        try:
            synthesis_prompt = f"""
            You are an Expert Avian Veterinarian AI Consultant. 
            A custom diagnostic computer vision model has output the following probabilities for a bird:
            {conditions_str}
            
            Here are the ONLY approved veterinary guidelines you are allowed to use:
            {guidelines_str}
            
            Task: Write a highly structured, punchy, and attractive medical dashboard. 
            
            CRITICAL RULES:
            1. Do NOT invent new medical advice outside the approved guidelines.
            2. Keep it strictly to short bullet points and bold text. 
            3. TRANSPARENCY RULE: If the 'Healthy' probability is high, but a disease is listed as the 'PRIMARY DIAGNOSIS', you MUST add a brief '⚠️ AI Diagnostic Note' at the very top explaining that while the bird shows signs of health, the cumulative sickness indicators triggered a safety protocol to prioritize the bird's safety.
            4. Use exactly this format:
            
            ### 📊 DIAGNOSTIC BREAKDOWN
            (List the probabilities and add the AI Diagnostic Note here if necessary)
            
            ### 🚨 IMMEDIATE ACTION PLAN
            (Pull the 'Immediate' and 'Warning' steps from the guidelines)
            
            ### 🩺 ONGOING TREATMENT & CARE
            (Pull the 'Treatment', 'Care', and 'Prevention' steps from the guidelines)
            """
            report_response = generate_gemini_content(synthesis_prompt)
            final_medical_report = report_response.text
        except Exception as synth_err:
            print(f"[SYNTHESIZER] Gemini synthesis note: {synth_err}. Using rule-based veterinary summary.")
            curr_advice = disease_suggestions.get(final_diagnosis, "Maintain strict daily biosecurity and monitor flock.")
            final_medical_report = f"### 📊 DIAGNOSTIC BREAKDOWN\n{conditions_str}\n\n### 🚨 IMMEDIATE ACTION PLAN\n- Primary Diagnosis: **{final_diagnosis}** (Confidence: {confidence:.1f}%)\n\n### 🩺 ONGOING TREATMENT & CARE\n{curr_advice}"

        # --- 4. GRAD-CAM HEATMAP ---
        base_layer = [l for l in active_model.layers if 'mobilenet' in l.name.lower()][0]
        last_conv = base_layer.get_layer('out_relu')
        conv_model = tf.keras.Model(base_layer.inputs, last_conv.output)
        classifier_input = tf.keras.Input(shape=last_conv.output.shape[1:])
        x = classifier_input
        for layer in active_model.layers[active_model.layers.index(base_layer)+1:]: 
            x = layer(x)
        classifier_model = tf.keras.Model(classifier_input, x)
        
        with tf.GradientTape() as tape:
            conv_outputs = conv_model(img_array)
            tape.watch(conv_outputs)
            preds = classifier_model(conv_outputs)
            top_class_channel = preds[:, 0] if preds.shape[1] == 1 else preds[:, tf.argmax(preds[0])]
        
        grads = tape.gradient(top_class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = tf.squeeze(conv_outputs[0] @ pooled_grads[..., tf.newaxis])
        heatmap = tf.maximum(heatmap, 0)
        max_heatmap = tf.math.reduce_max(heatmap)
        if max_heatmap != 0:
            heatmap = heatmap / max_heatmap
            
        heatmap_resized = tf.image.resize(heatmap[..., tf.newaxis], (224, 224)).numpy().squeeze()
        jet_heatmap = plt.get_cmap("jet")(np.arange(256))[:, :3][np.uint8(255 * heatmap_resized)]
        superimposed_img_array = np.clip(jet_heatmap * 0.4 + (img_array[0].numpy().astype("uint8") / 255.0), 0, 1)
        
        # Convert superimposed numpy array back to PIL Image for Base64 encoding
        superimposed_pil = PIL.Image.fromarray((superimposed_img_array * 255).astype(np.uint8))

        # --- 5. PACKAGE AND SEND ---
        return {
            "status": "success",
            "system": "PoultryHealth Intelligence",
            "primary_diagnosis": final_diagnosis,
            "confidence": round(confidence, 1),
            "report": final_medical_report,
            "distribution": distribution_dict,
            "open_set_alert": open_set_alert,
            "original_image_base64": image_to_base64(pil_img),
            "heatmap_image_base64": image_to_base64(superimposed_pil)
        }

    except Exception as e:
        traceback.print_exc()
        
        error_str = str(e).lower()
        if "429" in error_str or "quota" in error_str or "resourceexhausted" in error_str:
            return {
                "status": "error", 
                "message": "AI Server is currently busy or rate-limited. Please wait about 60 seconds and try again!"
            }
        
        if "gemini_api_key" in error_str or "api key" in error_str:
            return {
                "status": "error",
                "message": f"Gemini API configuration error: {str(e)}"
            }
            
        return {
            "status": "error",
            "message": f"Analysis error: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    # This runs the server on http://localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)