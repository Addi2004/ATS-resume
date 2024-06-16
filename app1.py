import streamlit as st
import pymongo
import os
from dotenv import load_dotenv
import google.generativeai as genai
import docx2txt
import PyPDF2 as pdf
import json

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

def generate_response_from_gemini(input_text):
    llm = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    output = llm.generate_content(input_text)
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    return docx2txt.process(uploaded_file)

input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

# Initialize MongoDB client
MONGODB_URI = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URI)
db = client['ats_db']
collection = db['evaluation_results']

# Streamlit app
st.set_page_config(page_title="Intelligent ATS", page_icon=":briefcase:", layout="wide")
st.title("🎯 Intelligent ATS - Enhance Your Resume for ATS")

st.sidebar.title("Navigation")
pages = ["Home", "ATS Evaluation"]
selection = st.sidebar.selectbox("Select a page", pages)

if selection == "Home":
    st.header("")
    st.markdown("""
        <div style="text-align: center;">
            <h2>Welcome to Intelligent ATS</h2>
            <p>This application helps you enhance your resume by analyzing it against job descriptions.</p>
            <h3>Features:</h3>
            <ul style="list-style-position: inside; text-align: left; display: inline-block;">
                <li>Upload your resume and job description.</li>
                <li>Get a detailed analysis with a match percentage.</li>
                <li>Receive recommendations and missing keywords.</li>
                <li>Improve your resume to increase your chances of getting hired.</li>
                <li>Navigate to the 'ATS Evaluation' page to get started!</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
elif selection == "ATS Evaluation":
    st.header("ATS Evaluation")
    st.subheader("Enter Job Description and Upload Resume")
    job_description = st.text_area("Paste the Job Description", height=200)
    uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

    submit_button = st.button("Submit")

    if submit_button:
        if uploaded_file is not None:
            with st.spinner("Extracting text from the resume..."):
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf_file(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx_file(uploaded_file)

            with st.spinner("Generating response..."):
                response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))
                response_dict = json.loads(response_text)
                match_percentage = float(response_dict["Job Description Match"].rstrip('%'))

                # Save the result to MongoDB
                result = {
                    "job_description": job_description,
                    "resume_text": resume_text,
                    "match_percentage": match_percentage,
                    "missing_keywords": response_dict["Missing Keywords"],
                    "candidate_summary": response_dict["Candidate Summary"],
                    "experience": response_dict["Experience"]
                }
                collection.insert_one(result)
                st.success("Evaluation result saved to MongoDB")

            st.subheader("📊 ATS Evaluation Result")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Job Description Match Percentage", value=f"{match_percentage}%")
                st.progress(match_percentage / 100)
            with col2:
                st.markdown(f"**Missing Keywords:** {response_dict['Missing Keywords']}")
                st.markdown(f"**Candidate Summary:** {response_dict['Candidate Summary']}")
                st.markdown(f"**Experience:** {response_dict['Experience']}")

            if match_percentage >= 80:
                st.success("**Recommendation: Move forward with hiring.**")
            else:
                st.warning("**Recommendation: Not a Match.**")

            with st.expander("📄 View Uploaded Resume"):
                st.text_area("Resume Text", resume_text, height=200)
            with st.expander("📋 View Job Description"):
                st.text_area("Job Description", job_description, height=200)

# Close MongoDB client connection at the end of the script
client.close()
