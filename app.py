import streamlit as st
import requests
from io import BytesIO

st.set_page_config(page_title="AI Visual Studio", page_icon="🎨", layout="centered")

st.title("🎨 AI Visual Generator & Enhancer")
st.write("Generate high-fidelity event graphics and visuals directly using free open inference models.")

st.markdown("""
<style>
    
    .main {
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    
    .header-card {
        background: linear-gradient(135deg, #1e1e2f 0%, #11111d 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-card h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .header-card p {
        color: #a0a5b5;
        font-size: 1rem;
        margin-bottom: 0;
    }
    
    
    .stTextArea label, .stSelectbox label {
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        letter-spacing: 0.3px;
    }

    
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        transform: translateY(-1px);
    }
    
    
    .image-card {
        background: #181b23;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 1.5rem;
    }
</style>

<!-- Header Markup -->
<div class="header-card">
    <h1>🎨 AI Visual Studio</h1>
    <p>Generate high-fidelity event graphics and visuals directly using free open inference models.</p>
</div>
""", unsafe_allow_html=True)

visual_prompt = st.text_area(
    "Visual Concept / Prompt:", 
    "Futuristic glowing neon lines with sleek dark metal background, high quality event poster, 8k resolution",
    height=100
)

col1, col2 = st.columns(2)
with col1:
    width = st.selectbox("Image Width:", [512, 768, 1024], index=0)
with col2:
    height = st.selectbox("Image Height:", [512, 768, 1024], index=0)

enhance_quality = st.checkbox("Apply HD Quality & Detail Enhancement", value=True)

if st.button("Generate & Enhance Visual", type="primary"):
    if not visual_prompt.strip():
        st.error("Please enter a visual concept prompt!")
    else:
        with st.spinner("Processing image generation & enhancement..."):
            try:
               
                prompt_text = visual_prompt
                if enhance_quality:
                    prompt_text += ", 8k resolution, highly detailed, sharp focus"
                
                encoded_prompt = requests.utils.quote(prompt_text)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                
               
                res = requests.get(image_url, timeout=40)
                
                if res.status_code == 200 and "image" in res.headers.get("Content-Type", ""):
                    st.success("Generation Complete!")
                    st.image(res.content, caption=f"Generated Asset ({width}x{height})", use_container_width=True)
                    
                   
                    st.download_button(
                        label="📥 Download High-Res Poster Image",
                        data=res.content,
                        file_name="generated_poster.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"Failed to fetch image. Status code: {res.status_code}")

            except Exception as e:
                st.error(f"Request Failed: {e}")