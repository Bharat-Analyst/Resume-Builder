import streamlit as st
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from docx import Document
import fitz  # PyMuPDF

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    return keywords

def plot_wordcloud(keywords, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

def keyword_comparison(jd_keywords, resume_keywords):
    jd_set = set(jd_keywords)
    resume_set = set(resume_keywords)
    missing_keywords = jd_set - resume_set
    return missing_keywords

def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    full_text = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text.append(page.get_text())
    return '\n'.join(full_text)

st.title('Resume Keyword Optimization App')

st.write("""
### Objective
Help users optimize their resumes for job applications.
""")

st.header('1. Job Description')
job_description = st.text_area("Paste the job description here:")

st.header('2. Upload Resume')
uploaded_file = st.file_uploader("Choose your resume file", type=["txt", "docx", "pdf"])
resume_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        resume_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = read_docx(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        resume_text = read_pdf(uploaded_file)

st.header('Or Paste Resume Text')
pasted_resume_text = st.text_area("Paste your resume text here:")

if pasted_resume_text:
    resume_text = pasted_resume_text

if st.button('Analyze Keywords'):
    if job_description and resume_text:
        # Extract keywords
        jd_keywords = extract_keywords(job_description)
        resume_keywords = extract_keywords(resume_text)
        
        # Compare keywords
        missing_keywords = keyword_comparison(jd_keywords, resume_keywords)
        
        st.subheader('Job Description Keywords')
        st.write(jd_keywords)
        plot_wordcloud(jd_keywords, 'Job Description Keywords')
        
        st.subheader('Resume Keywords')
        st.write(resume_keywords)
        plot_wordcloud(resume_keywords, 'Resume Keywords')
        
        st.subheader('Missing Keywords')
        st.write(missing_keywords)
        
        # AI-driven suggestions (basic implementation)
        st.subheader('AI-driven Suggestions')
        suggestions = "Consider adding the following keywords to your resume: " + ', '.join(missing_keywords)
        st.write(suggestions)
    else:
        st.write("Please provide both the job description and resume text.")
