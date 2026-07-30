import streamlit as st
import os
import re
import chromadb
import requests

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
# CHROMA DATABASE
# ======================================

client = chromadb.PersistentClient(
    path=DATABASE_PATH
)


collection = client.get_collection(
    name="manual_library"
)



# ======================================
# SEARCH MANUAL + PDF
# ======================================

def search_manual(question):


    result = collection.query(

        query_texts=[
            question
        ],

        n_results=5,

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
        r"No\.\s*:\s*\S+",
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
# OLLAMA AI ANSWER
# ======================================

def ask_ai(context, question, language):


    if language == "Malay":


        instruction = """

Jawab dalam Bahasa Melayu sahaja.

Gunakan maklumat manual dan PDF sahaja.

Tukar ayat teknikal kepada ayat mudah yang operator boleh faham.

Jangan tambah maklumat luar.

Format jawapan:


Nama Alarm:

Penerangan:

Punca:

Paparan Skrin:

Keadaan Mesin:

Penyelesaian:


"""


    else:


        instruction = """

Answer in English only.

Use only information from manual and PDF.

Convert technical sentences into simple operator language.

Do not add outside information.


Answer format:


Alarm Name:

Description:

Cause:

Screen Display:

Machine State:

Solution:


"""



    prompt = f"""

You are a Machine Manual Assistant.


{instruction}


Manual/PDF Information:


{context}



User Question:


{question}


"""



    try:


        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model":"llama3.1",

                "prompt":prompt,

                "stream":False

            }

        )


        result = response.json()


        return result["response"]



    except Exception as e:


        return f"Ollama Error: {e}"



# ======================================
# DISPLAY IMAGE
# ======================================

def display_images(question, answer):


    images = get_related_images(

        question + " " + answer

    )


    if not images:

        return



    st.divider()


    st.subheader(
        "Related Image"
    )



    for img in images:


        img_path = os.path.join(

            IMAGE_FOLDER,

            img

        )


        if os.path.exists(img_path):


            st.image(

                img_path,

                use_container_width=True

            )



# ======================================
# STREAMLIT SETTINGS
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



# ======================================
# SEARCH BUTTON
# ======================================

if st.button("Search"):


    if question.strip() == "":


        st.warning(

            "Please enter your question."

        )


    else:



        with st.spinner(

            "Searching manual..."

        ):



            docs = search_manual(

                question

            )



            if not docs:


                st.error(

                    "No related information found in manual."

                )


            else:



                context = "\n\n".join(

                    docs

                )



                answer = ask_ai(

                    context,

                    question,

                    language

                )



                st.divider()


                st.header(

                    "Answer"

                )


                st.markdown(

                    answer

                )



                display_images(

                    question,

                    answer

                )