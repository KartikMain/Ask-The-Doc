import streamlit as st
import os
from modules.text_extractor import extract_text
from modules.summarizer import summarize_text
from modules.qa_system import answer_question
from modules.tts import text_to_speech

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Ask The Doc", layout="centered")
st.title("🧠 Ask The Doc (Offline Version)")
st.write("Upload a file, get a summary, ask questions — all offline and free.")

uploaded_file = st.file_uploader("Upload File (PDF, Word, TXT, or Image)", type=["pdf", "docx", "txt", "jpg", "png"])

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully!")

    # Extract and show text
    text = extract_text(file_path)
    st.subheader("📄 Extracted Text")
    st.text_area("Extracted content", text, height=300)

    # Generate summary automatically
    with st.spinner("Generating summary..."):
        try:
            summary = summarize_text(text)
            st.subheader("📝 Summary")
            st.write(summary)

            audio_path = text_to_speech(summary, "summary.mp3")
            st.audio(audio_path)
        except Exception as e:
            st.error(f"❌ Summary generation failed: {e}")
            summary = ""

    # Q&A based on summary only
st.markdown("---")
st.subheader("❓ Ask a Question (Based on Full Text)")
question = st.text_input("Type your question")

if st.button("Get Answer") and question:
    with st.spinner("Answering..."):
        try:
            answer = answer_question(text, question)  # using full text now
            st.subheader("💡 Answer")
            st.write(answer)

            answer_audio = text_to_speech(answer, "answer.mp3")
            st.audio(answer_audio)
        except Exception as e:
            st.error(f"❌ Failed to answer: {e}")
