import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to extract text from PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Split extracted text into smaller chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

# Create a FAISS vector store from text chunks
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Generate an advanced conversational chain for Q&A
def get_advanced_conversational_chain():
    prompt_template = """
    Give the response based on the PDF and intelligently answer the questions based on the PDF.
    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Handle user input to retrieve relevant information from PDFs
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        if not docs:
            st.write("No relevant information found.")
            return

        chain = get_advanced_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

        st.write("Reply: ", response["output_text"])
        collect_feedback(response["output_text"])

    except ValueError as e:
        st.error(f"Error loading vector store: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Collect user feedback on the AI response
def collect_feedback(response):
    feedback = st.text_area("Provide feedback on the response:")
    if st.button("Submit Feedback"):
        with open("feedback.txt", "a") as f:
            f.write(f"Response: {response} | Feedback: {feedback}\n")
        st.success("Thank you for your feedback!")

# Display PDF metadata in the sidebar
def display_pdf_metadata(pdf_docs):
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        metadata = pdf_reader.metadata
        st.write(f"Title: {metadata.get('/Title', 'Unknown')}")
        st.write(f"Author: {metadata.get('/Author', 'Unknown')}")
        st.write(f"Number of Pages: {len(pdf_reader.pages)}")

# Main page layout
def homepage():
    st.markdown('<h1 class="title-style">AI Interviewer Beta</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Welcome to the AI Interviewer Beta!</h2>', unsafe_allow_html=True)
    st.write("This tool helps you prepare for interviews by generating job-specific questions, offering feedback, and simulating realistic interview scenarios.")
    st.image("https://image.shutterstock.com/image-photo/job-interview-concept-professional-interviewer-260nw-1037430767.jpg", use_column_width=True)

    st.markdown('<h3 class="subtitle-style">Tool Overview</h3>', unsafe_allow_html=True)
    st.write("This AI Interviewer covers several aspects including behavioral, professional, and resume-based questions.")

# Behavioral Interview Screen
def behavioral_screen():
    st.markdown('<h1 class="title-style">Behavioral Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice for behavioral questions typically asked in interviews.</h2>', unsafe_allow_html=True)

    # Button to start the behavioral interview
    if st.button("Start Behavioral Interview", key="behavioral", help="Click to begin behavioral interview"):
        st.success("Behavioral interview started!")

        # Start PDF chatbot process
        user_question = st.text_input("Ask a Question from the PDF Files")
        if user_question:
            user_input(user_question)

        with st.sidebar:
            st.title("Menu:")
            pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text.strip():
                        st.error("No text found in the provided PDF files.")
                        return
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    display_pdf_metadata(pdf_docs)
                    st.success("Done")

# Professional Interview Screen
def professional_screen():
    st.markdown('<h1 class="title-style">Professional Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice for professional questions based on your selected role.</h2>', unsafe_allow_html=True)

    if st.button("Start Professional Interview", key="professional", help="Click to begin professional interview"):
        st.success("Professional interview started!")
        st.info("**Question:** What technical challenges have you faced in your previous projects, and how did you solve them?")

# Resume-based Interview Screen
def resume_screen():
    st.markdown('<h1 class="title-style">Resume-based Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice questions based on your resume.</h2>', unsafe_allow_html=True)

    if st.button("Start Resume Interview", key="resume", help="Click to begin resume-based interview"):
        st.success("Resume-based interview started!")
        st.info("**Question:** Can you explain a project from your resume in detail? What challenges did you encounter?")

# Create the navigation menu on the left sidebar with icons and improved look
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation Options",
        options=["🏠 Homepage", "📝 Behavioral Screen", "💼 Professional Screen", "📄 Resume Screen"],
        icons=["house", "chat-left-dots", "briefcase", "file-earmark-person"],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"background-color": "#333333"},  # Darker sidebar background
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "color": "white", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

# Main Content Logic
if selected == "🏠 Homepage":
    homepage()
elif selected == "📝 Behavioral Screen":
    behavioral_screen()
elif selected == "💼 Professional Screen":
    professional_screen()
elif selected == "📄 Resume Screen":
    resume_screen()

# Footer
st.markdown("""
<hr style="border:2px solid #4CAF50">
<p style="text-align:center; color: #f5f5f5;">Powered by OpenAI | Streamlit | FAISS | Langchain | © 2024 AI Interviewer</p>
""", unsafe_allow_html=True)
