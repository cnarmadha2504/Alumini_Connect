import streamlit as st
import pandas as pd
import re

from langchain_helper import (
    get_qa_chain,
    create_vector_db,
    get_faq_answer,
    get_alumni_data
)


# --------------------------------
# Load alumni records
# --------------------------------

ALUMNI_DATA_PATH = "alumni_records.csv"


def load_alumni_data():

    return pd.read_csv(ALUMNI_DATA_PATH)


# --------------------------------
# Detect DATA questions
# --------------------------------

def is_data_question(question):

    q = question.lower()

    keywords = [
        "how many",
        "count",
        "number of",
        "who are",
        "working in",
        "work in",
        "placed",
        "placement",
        "batch"
    ]

    has_year = bool(
        re.search(r"\b(19|20)\d{2}\b", q)
    )

    df = load_alumni_data()

    companies = df["company"].dropna().unique()

    has_company = any(
        str(company).lower() in q
        for company in companies
    )

    return (
        any(keyword in q for keyword in keywords)
        or has_year
        or has_company
    )


# --------------------------------
# Answer DATA questions
# --------------------------------

def answer_data_question(question):

    df = load_alumni_data()

    q = question.lower()

    # Find year
    year_match = re.search(
        r"\b(19|20)\d{2}\b",
        q
    )

    year = None

    if year_match:

        year = int(year_match.group())

        df = df[
            df["year"] == year
        ]


    # Find company
    company = None

    for company_name in df["company"].dropna().unique():

        company_name = str(company_name)

        if company_name.lower() in q:

            company = company_name

            df = df[
                df["company"].str.lower()
                == company_name.lower()
            ]

            break


    # Placement
    placed = False

    if (
        "placed" in q
        or "placement" in q
    ):

        placed = True

        df = df[
            df["status"].str.lower()
            == "placed"
        ]


    # Department
    department = None

    for dept in df["department"].dropna().unique():

        dept = str(dept)

        if dept.lower() in q:

            department = dept

            df = df[
                df["department"].str.lower()
                == dept.lower()
            ]
            break
    # WHO questions
    if "who" in q:
        if len(df) == 0:
            return "No matching alumni records were found."
        result = (
            f"Found {len(df)} matching alumni:\n\n"
        )
        for _, row in df.iterrows():
            result += (
                f"- {row['name']} — "
                f"{row['company']} "
                f"({row['year']})\n"
            )
        return result
    # COUNT questions
    if (
        "how many" in q
        or "count" in q
        or "number of" in q
    ):
        count = len(df)
        description = []
        if year:
            description.append(
                f"{year} batch"
            )
        if company:
            description.append(
                f"working at {company}"
            )
        if placed:
            description.append(
                "placed"
            )
        if department:
            description.append(
                f"from {department}"
            )
        if description:
            return (
                f"There are **{count} alumni** "
                f"matching: "
                f"{', '.join(description)}."
            )
        return (
            f"There are **{count} alumni records**."
        )
    return None
# --------------------------------
# STREAMLIT UI
# --------------------------------
st.title("🎓 Alumni Chatbot")
st.write(
    "Ask about alumni FAQs, general information, "
    "or alumni statistics."
)
# Create knowledgebase button
btn = st.button(
    "Search"
)
if btn:
    with st.spinner(
        "Creating knowledgebase..."
    ):
        create_vector_db()
    st.success(
        "Knowledgebase created successfully!"
    )
# Question
question = st.text_input(
    "Question:"
)
if question:
    # =========================================
    # 1. FAQ
    # =========================================
    faq_answer = get_faq_answer(question)
    if faq_answer:
        st.subheader("FAQ Answer")
        st.write(faq_answer)

    # =========================================
    # 2. ALUMNI RECORDS / DATA
    # =========================================
    elif is_data_question(question):
        answer = answer_data_question(
            question
        )
        if answer:
            st.subheader(
                "Alumni Records Answer"
            )
            st.write(answer)
        else:
            st.warning(
                "No matching alumni records found."
            )
    # =========================================
    # 3. RAG
    # =========================================
    else:
        chain = get_qa_chain()
        response = chain.invoke({
            "query": question
        })
        st.subheader(
            "RAG Answer"
        )
        st.write(
            response["result"]
        )