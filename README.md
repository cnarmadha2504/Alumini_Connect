# 🎓 Alumni Connect — AI-Powered Alumni Chatbot
An AI-powered **Alumni Chatbot** designed to help educational institutions quickly access and analyze alumni information.
The project combines **FAQ retrieval, Retrieval-Augmented Generation (RAG), and structured alumni data analysis** to provide answers about alumni services, records, placements, companies, departments, and career status.
## 📌 Problem Statement
Educational institutions often need information about previous students for:
* Alumni activities
* Placement reports
* Academic requirements
* Accreditation documentation
* Department-level analysis
* Alumni engagement
* Career and employment tracking
Collecting this information manually from different sources can be time-consuming.
This project provides a conversational interface to make alumni information easier to access.

## 🚀 Features
### 1. Alumni FAQ
Answers common alumni-related questions such as:
* How can I update my contact information?
* How can I obtain my transcript?
* Are networking events available?
* How can I join the alumni mentorship program?
* How can I get an alumni ID card?
### 2. RAG-Based Question Answering
The chatbot uses:
* FAISS vector database
* Hugging Face embeddings
* LangChain
* Gemini
to retrieve relevant information and generate contextual responses.
### 3. Structured Alumni Records
The system uses a CSV dataset containing alumni records with information such as:
* Alumni ID
* Graduation year
* Name
* Department
* Company
* Career status
### 4. Alumni Data Queries
Users can ask questions such as:
```text
How many alumni graduated in 2016?
How many alumni are working at Infosys?
How many CSE students were placed?
How many alumni are seeking opportunities?
Which companies have alumni from 2018?
```
### 5. Simple Streamlit Interface
The application provides a simple web interface where users can enter questions and receive answers.
## 🏗️ System Architecture
```text
                    USER QUESTION
                         │
                         ▼
                  Question Router
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             FAQ         RAG      RECORDS
              │          │          │
              ▼          ▼          ▼
        FAQ Dataset     FAISS     Pandas
                         │
                       Gemini
              └──────────┼──────────┘
                         ▼
                      ANSWER
```
## 🛠️ Technologies Used
| Technology   | Purpose                  |
| ------------ | ------------------------ |
| Python       | Application development  |
| Streamlit    | Web interface            |
| LangChain    | LLM and RAG workflow     |
| FAISS        | Vector similarity search |
| Gemini       | AI response generation   |
| Hugging Face | Text embeddings          |
| Pandas       | Alumni data processing   |
| CSV          | FAQ and alumni datasets  |

## 📂 Project Structure

```text
Alumini_Connect/
│
├── main.py
├── langchain_helper.py
├── alumni_faq.csv
├── alumni_records_560.csv
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```
### File Description
**`main.py`**
Streamlit application and question-routing logic.
**`langchain_helper.py`**
Contains the RAG, FAISS, Gemini, embeddings, and alumni-data functions.
**`alumni_faq.csv`**
Contains frequently asked alumni questions and answers.
**`alumni_records_.csv`**
Contains the alumni records used for structured queries and analysis.
**`.env.example`**
Template for configuring the Gemini API key.
### 💬 Example Questions
```text
How do I update my contact information?
How can I get a copy of my transcript?
How many alumni graduated in 2016?
How many alumni are working at Infosys?
How many CSE students were placed?
How many alumni are seeking opportunities?
```
## 📊 Data Analysis
The chatbot can perform basic analysis of alumni records, including:
* Year-wise alumni counts
* Company-wise counts
* Department-wise counts
* Placement-related counts
* Career-status analysis
* Year and company filtering

## 🎯 Purpose

The main objective of this project is to reduce the time required for academicians and institutions to search for alumni-related information.
It can support activities such as:
* Alumni coordination
* Placement analysis
* Academic reporting
* Accreditation documentation
* Alumni engagement
* Institutional data analysis
## 🔮 Future Enhancements
* Alumni registration and profile updates
* Authentication
* Live alumni database integration
* Alumni dashboard
* Placement analytics and visualizations
* Company-wise and department-wise charts
* Advanced natural-language filtering
* Multilingual chatbot support
* Deployment to a cloud platform
* Integration with institutional alumni databases

## 👩‍💻 Author

**Narmadha V**

M.Sc. Computer Science | AI | Machine Learning | Data Science | IoT

---

### Suggested GitHub repository description

> **AI-powered Alumni Chatbot using Python, Streamlit, LangChain, FAISS, Gemini, Hugging Face Embeddings and Pandas for alumni FAQs, RAG-based Q&A and structured alumni data analysis.**
