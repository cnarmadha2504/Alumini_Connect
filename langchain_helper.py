import os
from dotenv import load_dotenv
import pandas as pd

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA

load_dotenv()

DATASET_PATH = "alumni_faq.csv"
VECTORDB_PATH    = "faiss_index"
ALUMNI_DATA_PATH = "alumni_records.csv"

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.1,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


FAQ_PATH="alumni_faq.csv"
def get_faq_answer(question):
    df = pd.read_csv(FAQ_PATH)
    question = question.lower().strip()
    for _, row in df.iterrows():
        prompt = str(row["prompt"]).lower().strip()
        if question == prompt:
            return row["response"]
    return None

def get_alumni_data():
    return pd.read_csv(ALUMNI_DATA_PATH)
def count_alumni(year=None, company=None, status=None, department=None):
    df = get_alumni_data()
    if year is not None:
        df = df[df["year"] == int(year)]
    if company is not None:
        df = df[df["company"].str.lower() == company.lower()]
    if status is not None:
        df = df[df["status"].str.lower() == status.lower()]
    if department is not None:
        df = df[df["department"].str.lower() == department.lower()]
    return len(df)


def create_vector_db():
    loader = CSVLoader(file_path=DATASET_PATH, source_column="prompt")
    data = loader.load()
    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
    vectordb.save_local(VECTORDB_PATH)


def get_qa_chain():
    vectordb = FAISS.load_local(
        VECTORDB_PATH, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectordb.as_retriever(search_kwargs={"score_threshold": 0.7})
    prompt_template = """Given the following context and a question, generate an
    answer based on this context only. Use info about alumni current status, records
     and services where relevant. In the answer, try to provide as
    much text as possible from the "response" section in the source document
    context without making major changes. If the answer is not found in the
    context, say "I don't know." Don't make up an answer.

    CONTEXT: {context}
    QUESTION: {question}"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )
    return chain


if __name__ == "__main__":
    if not os.path.exists(VECTORDB_PATH):
        create_vector_db()
    chain = get_qa_chain()
    result = chain("hello?")
    print(result["result"])