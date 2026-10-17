import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Wireframe2Code - Gemma 4", page_icon="🎨", layout="wide")
# --- Polished UI Enhancements ---
st.markdown("""
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
        .header-bar {
            background: linear-gradient(135deg, #FF6F61 0%, #FFB199 40%, #D4FC79 80%);
            padding: 2.5rem;
            border-radius: 12px;
            text-align: center;
            color: #fff;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .header-bar h1 { margin: 0; font-size: 3rem; color: white; font-weight: 800; }
        .header-bar p { font-size: 1.1rem; color: rgba(255,255,255,0.9); }
    </style>
    <div class="header-bar">
        <h1>✨ Pixel To Platform</h1>
        <p>Convert your wildest wireframes into responsive, colourful live platforms in seconds.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Modern Dark Glassmorphism Theme */
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #111827 100%);
            color: #e5e7eb;
        }
        
        /* Sleek Glassmorphism Header */
        .header-bar {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            color: #fff;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .header-bar h1 {
            margin: 0;
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header-bar p {
            font-size: 1.1rem;
            color: #9ca3af;
            margin-top: 0.5rem;
        }

        /* 🌟 Super Pretty Glow Up for the Upload Box */
        [data-testid="stFileUploader"] {
            background: rgba(17, 24, 39, 0.8) !important;
            border: 2px dashed #818cf8 !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 0 20px rgba(129, 140, 248, 0.15);
            transition: all 0.3s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #c084fc !important;
            box-shadow: 0 0 25px rgba(192, 132, 252, 0.3);
            transform: translateY(-2px);
        }
        
        /* Style the upload text nicely */
        [data-testid="stFileUploader"] section div p {
            color: #e5e7eb !important;
            font-weight: 500;
        }

        /* Styled Action Buttons */
        .stButton button {
            background: linear-gradient(90deg, #6366f1, #a855f7);
            color: white;
            border-radius: 10px;
            font-weight: 600;
            border: none;
            padding: 0.6rem 1.2rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
primary_color = st.sidebar.color_picker("Brand Primary Color", "#3B82F6")
secondary_color = st.sidebar.color_picker("Secondary Accent Color", "#A78BFA")
bg_color = st.sidebar.color_picker("Background Color", "#0f172a")
text_color = st.sidebar.color_picker("Text Color", "#e5e7eb")
if not api_key:
    st.info("👈 Enter your Gemini API Key in the sidebar to get started!")
else:
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader(
        "Upload Sketch",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        image = Image.open(uploaded_file)
        with col1:
            st.subheader("📷 Hand-Drawn Sketch")
            st.image(image, use_container_width=True)
            generate_btn = st.button("Generate Code 🚀", type="primary", use_container_width=True)

        if generate_btn:
            with col2:
                with st.spinner("Gemma 4 is reading your sketch and writing HTML/Tailwind..."):
                    try:
                        prompt = (
    f"You are an expert Frontend Web Developer. Carefully analyze this hand-drawn wireframe sketch. "
    f"Identify elements like navigation bars, headings, text boxes, buttons, and cards. "
    f"Convert this sketch into fully functional, clean HTML code styled with Tailwind CSS or inline CSS. "
    f"CRITICAL REQUIREMENT: Apply the following exact HEX color palette across the website layout:\n"
    f"CRITICAL REQUIREMENT: Make all text elements directly editableby adding 'contentediable=\"true\"' to them,and include a lightweight JaveScript snippet so user cards and containers can be dragged and repositioned diresctly within the browser view."
    f"- Primary Accent Color (Headers, Navigation, Highlights): {primary_color}\n"
    f"- Secondary / Action Color (Buttons, Links, Active Badges): {secondary_color}\n"
    f"- Background Color (Page Body / Container Backgrounds): {bg_color}\n"
    f"- Text Color (Primary Body Text, Headings): {text_color}\n\n"
    f"Output ONLY valid raw HTML code inside standard markdown codeblocks without introductory or concluding filler text."
)

                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=[image, prompt]
                        )

                        raw_code = response.text.replace("```html", "").replace("```", "").strip()

                        tab1, tab2 = st.tabs(["🌐 Live Interactive Render", "📝 HTML Code"])

                        with tab1:
                            st.components.v1.html(raw_code, height=520, scrolling=True)

                        with tab2:
                            st.code(raw_code, language="html")
                            st.download_button(
                                label="📥 Download HTML File",
                                data=raw_code,
                                file_name="index.html",
                                mime="text/html"
                            )

                    except Exception as e:
                        st.error(f"Error during generation: {e}")
