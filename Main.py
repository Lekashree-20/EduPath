import os
import streamlit as st
import requests
import json
from fpdf import FPDF
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Set your Hyperleap API key
API_KEY = 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='

# Define Streamlit app title
st.title("Syllabus and Content Generator")

# Ask the user to input their role (Student, Researcher, or Teacher)
user_role = st.sidebar.radio("Select User Role", ("Student", "Researcher", "Teacher"))

# Define the Streamlit app mode
app_mode = st.sidebar.radio("Select Mode", ("Syllabus Generator", "Content Generator"))
syllabus_topics = []

# Define the API endpoint for prompts
SYLLABUS_API_URL = 'https://api.hyperleap.ai/prompts'
CONTENT_API_URL = 'https://api.hyperleap.ai/prompts'

if app_mode == "Syllabus Generator":
    st.header("Syllabus Generator")

    # List of subjects
    subjects = ["Artificial Intelligence", "Data Science", "Machine Learning", "Civil Engineering"]  # Add more subjects as needed

    # Dropdown to select subject
    subject_name = st.sidebar.selectbox("Select Subject", subjects)

    # Generate syllabus based on selected subject
    if subject_name:
        st.session_state.subject_name = subject_name  # Save subject name to session state

        # Create payload for syllabus generation
        payload = {
            "promptId": "81590497-4e97-42e3-b8d7-901c65d24f1f",
            "promptVersionId": "989d1c23-1cb3-4092-ba9b-4fcd456fdd08",
            "replacements": {
                "subject": subject_name
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'x-hl-api-key': API_KEY
        }

        # Function to fetch syllabus data
        def fetch_syllabus_data():
            response = requests.post(SYLLABUS_API_URL, json=payload, headers=headers)
            return response

        # Fetch and display the syllabus
        res = fetch_syllabus_data()
        if res.status_code == 200:
            try:
                res_json = res.json()
                course_data = json.loads(res_json["choices"][0]["message"]["content"])
                st.session_state['course_data'] = course_data

                # Display the generated syllabus
                st.header(subject_name)
                for chapter in course_data[0]["chapters"]:
                    st.markdown(f"### {chapter['chapterName']}")
                    for subtopic in chapter["subTopics"]:
                        st.markdown(f"- {subtopic}")

                # Store syllabus topics for content generation
                syllabus_topics = [subtopic for chapter in course_data[0]["chapters"] for subtopic in chapter["subTopics"]]
                st.session_state.syllabus_topics = syllabus_topics
            except (json.JSONDecodeError, KeyError) as e:
                st.error(f"Failed to parse syllabus data: {str(e)}")
        else:
            st.error(f"Failed to fetch syllabus data. Status code: {res.status_code}")

elif app_mode == "Content Generator":
    st.header("Content Generator")

    # Retrieve syllabus topics from session state
    syllabus_topics = st.session_state.get("syllabus_topics", [])
    subject_name = st.session_state.get("subject_name", "")

    if not subject_name:
        st.warning("Please generate a syllabus first in the 'Syllabus Generator' mode.")
    else:
        # List of subtopics
        subtopics = syllabus_topics if syllabus_topics else ["Subtopic 1", "Subtopic 2", "Subtopic 3"]  # Use syllabus topics if available, else default subtopics

        # Dropdown to select subtopic
        subtopic_name = st.sidebar.selectbox("Select Subtopic", subtopics)

        # Generate content based on selected subtopic
        if subtopic_name:
            # Create payload for content generation
            payload = {
                "promptId": "f937db13-4d95-43f0-9e71-1dda1dc146ea",
                "promptVersionId": "2e58658d-e8ca-44ee-814e-29c4a81095be",
                "replacements": {
                    "subtopic": subtopic_name,
                    "subject": subject_name
                }
            }

            headers = {
                "accept": "application/json",
                "x-hl-api-key": API_KEY,
                "content-type": "application/json"
            }

            # Function to fetch content data
            def fetch_content_data():
                response = requests.post(CONTENT_API_URL, data=json.dumps(payload), headers=headers)
                return response

            # Fetch and display the content
            res = fetch_content_data()
            if res.status_code == 200:
                try:
                    res_json = res.json()
                    content_data = json.loads(res_json["choices"][0]["message"]["content"])

                    # Display the generated content
                    st.header(subtopic_name)
                    st.write(content_data)

                    # Save the content to a PDF file
                    pdf_file_path = "generated_content.pdf"
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, content_data)
                    pdf.output(pdf_file_path)

                    # Provide download button for the generated PDF
                    with open(pdf_file_path, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(label="Download Generated PDF", data=pdf_bytes, file_name="generated_content.pdf", mime="application/pdf")
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Failed to parse content data: {str(e)}")
            else:
                st.error(f"Failed to fetch content data. Status code: {res.status_code}")

# Function to extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to get vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index.pickle")

# Function to create conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to process user input
def process_user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

# Main function
def main():
    st.header("Do you have any doubts? ")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        response = process_user_input(user_question)
        st.write("Reply: ", response)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()
