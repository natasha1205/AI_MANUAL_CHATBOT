import streamlit as st
import os
import re
import chromadb

from image_mapping import get_related_images


# ======================================
# PATH
# ======================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database"
)

IMAGE_FOLDER = os.path.join(
    BASE_DIR,
    "images"
)


# ======================================
# LOAD DATABASE
# ======================================

client = chromadb.PersistentClient(
    path=DATABASE_PATH
)


collection = client.get_collection(
    name="manual_library"
)



# ======================================
# SEARCH DATABASE
# ======================================

def search_manual(question):

    result = collection.query(

        query_texts=[
            question
        ],

        n_results=1,

        include=[
            "documents"
        ]

    )


    documents = result.get(
        "documents",
        []
    )


    if documents:

        return documents[0]


    return []



# ======================================
# CLEAN TEXT
# ======================================

def clean_text(text):

    text = re.sub(
        r"No\.\s*:\s*\d+",
        "",
        text
    )


    text = re.sub(
        r"\n+",
        "\n",
        text
    )


    return text.strip()



# ======================================
# EXTRACT INFORMATION
# ======================================

def extract_alarm(text):


    text = clean_text(text)


    data = {

        "alarm":"",
        "description":"",
        "cause":"",
        "screen":"",
        "machine":"",
        "solution":""

    }



    patterns = {


        "alarm":
        r"Alarm Name[:\s]*(.*?)(?=Description|$)",


        "description":
        r"Description[:\s]*(.*?)(?=Cause|$)",


        "cause":
        r"Cause[:\s]*(.*?)(?=Screen Display|Alarm Light|$)",


        "screen":
        r"(?:Screen Display|Alarm Light)[:\s]*(.*?)(?=Machine State|$)",


        "machine":
        r"Machine State(?: After Alarm)?[:\s]*(.*?)(?=Solution|$)",


        "solution":
        r"Solution[:\s]*(.*)"

    }



    for key, pattern in patterns.items():

        result = re.search(

            pattern,

            text,

            re.I | re.S

        )


        if result:

            data[key] = result.group(1).strip()



    return data



# ======================================
# FORMAT ANSWER
# ======================================

def format_answer(documents, language):


    text = "\n".join(
        documents
    )


    data = extract_alarm(
        text
    )


    if language == "Malay":


        answer = f"""

Nama Alarm: {data['alarm']}


Penerangan: {data['description']}


Punca: {data['cause']}


Paparan Skrin: {data['screen']}


Keadaan Mesin: {data['machine']}


Penyelesaian: {data['solution']}

"""


    else:


        answer = f"""

Alarm Name: {data['alarm']}


Description: {data['description']}


Cause: {data['cause']}


Screen Display: {data['screen']}


Machine State: {data['machine']}


Solution: {data['solution']}

"""


    return answer.strip()



# ======================================
# DISPLAY IMAGE
# ======================================

def display_images(question):


    images = get_related_images(
        question
    )


    if not images:

        return



    st.divider()


    st.subheader(
        "Related Image"
    )



    for img in images:


        path = os.path.join(

            IMAGE_FOLDER,

            img

        )


        if os.path.exists(path):


            st.image(

                path,

                width=700

            )




# ======================================
# STREAMLIT UI
# ======================================

st.set_page_config(

    page_title="Machine Manual Assistant",

    layout="centered"

)



st.title(
    "Machine#1 Manual Assistant"
)



language = st.selectbox(

    "Select Language:",

    [
        "English",
        "Malay"
    ]

)



question = st.text_input(

    "Enter your question:"

)



if st.button("Search"):


    if question.strip() == "":


        st.warning(
            "Please enter your question."
        )


    else:


        with st.spinner(
            "Searching manual database..."
        ):


            docs = search_manual(

                question

            )


            if not docs:


                st.error(

                    "No information found in manual."

                )


            else:


                answer = format_answer(

                    docs,

                    language

                )


                st.divider()


                st.subheader(
                    "Answer"
                )


                # IMPORTANT
                # use text not markdown
                st.text(
                    answer
                )


                display_images(

                    question

                )