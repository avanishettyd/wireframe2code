import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Wireframe2Code - Gemma 4", page_icon="🎨", layout="wide")

st.markdown("## 🎨 Wireframe2Code")
st.markdown("Transform hand-drawn paper sketches into live interactive web pages using **Gemma 4**.")

st.sidebar.title("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👈 Enter your Gemini API Key in the sidebar to get started!")
else:
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader(
        "Upload a photo of your paper sketch or whiteboard wireframe", 
        type=["png", "jpg", "jpeg"]
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
                            "You are an expert Frontend Web Developer. Carefully analyze this hand-drawn wireframe sketch. "
                            "Identify elements like navigation bars, headings, text boxes, buttons, and cards. "
                            "Convert this sketch into fully functional, clean HTML code using Tailwind CSS for styling. "
                            "Output ONLY valid raw HTML code inside standard markdown codeblocks without introductory or concluding filler text."
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
