import streamlit as st
from PyPDF2 import PdfReader
import sqlite3

st.set_page_config(page_title="AI Study Assistant")

st.title("📚 AI Study Assistant")

uploaded_file = st.file_uploader(
    "Upload your PDF Notes",
    type="pdf"
)

if uploaded_file is not None:

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    st.success("PDF Uploaded Successfully!")

    word_count = len(text.split())
    char_count = len(text)
    page_count = len(pdf_reader.pages)

    # Save to database
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO uploads(filename,pages,words) VALUES(?,?,?)",
        (
            uploaded_file.name,
            page_count,
            word_count
        )
    )

    conn.commit()
    conn.close()

    st.subheader("📊 PDF Statistics")

    st.write(f"Pages : {page_count}")
    st.write(f"Words : {word_count}")
    st.write(f"Characters : {char_count}")

    st.subheader("📄 Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=250
    )

    st.subheader("📝 Summary")

    sentences = text.split('.')
    summary = '. '.join(sentences[:5])

    st.success(summary)

    st.subheader("❓ Quiz Questions")

    words = text.split()

    for i in range(min(5, len(words)//10)):
        st.write(
            f"Q{i+1}: Explain '{words[i*10]}'?"
        )

# Upload History
st.subheader("📚 Upload History")

conn = sqlite3.connect("study.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM uploads")

rows = cursor.fetchall()

for row in rows:
    st.write(row)

conn.close()