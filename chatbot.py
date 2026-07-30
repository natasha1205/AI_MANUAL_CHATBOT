import streamlit as st
import os
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
# LOAD CHROMA DATABASE
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

        n_results=2,

        include=[
            "documents"
        ]

    )


    documents = result.get(
        "documents",
        []
    )


    if documents and documents[0]:

        return documents[0]


    return []




# ======================================
# OLLAMA ANSWER
# ======================================

def ask_ollama(context, question, language):


    if language == "Malay":

        instruction = """

Jawab dalam Bahasa Melayu sahaja.

Gunakan maklumat daripada manual dan PDF sahaja.

Tukar ayat teknikal kepada ayat mudah difahami operator.

Susun jawapan dalam bentuk point:

Alarm Name:
- 

Description:
-

Cause:
-

Screen Display:
-

Machine State:
-

Solution:
-


Jangan tambah maklumat luar.


"""


    else:


        instruction = """

Answer in English only.

Use information from manual and PDF only.

Change technical sentences into simple words for operators.

Format answer using points:

Alarm Name:
-

Description:
-

Cause:
-

Screen Display:
-

Machine State:
-

Solution:
-


Do not add outside information.


"""



    prompt = f"""

You are a Machine Manual Assistant.


{instruction}


Information from manual/pdf:

{context}


User Question:

{question}


"""



    try:


        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model":"llama3",

                "prompt":prompt,

                "stream":False

            }

        )


        data = response.json()


        return data.get(
            "response",
            ""
        )


    except Exception as e:


        return "Ollama Error: " + str(e)




# ======================================
# DISPLAY IMAGE
# ======================================

def display_images(question, answer):


    search_text = (

        question +

        " " +

        answer

    )


    images = get_related_images(
        search_text
    )


    if not images:

        return



    st.divider()


    st.subheader(
        "Related Image"
    )



    for image in images:


        image_path = os.path.join(

            IMAGE_FOLDER,

            image

        )


        if os.path.exists(image_path):


            st.image(

                image_path,

                width=600

            )





# ======================================
# STREAMLIT UI
# ======================================

st.set_page_config(

    page_title="Machine#1 Manual Assistant",

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
            "Searching manual..."
        ):



            # Search manual + pdf

            docs = search_manual(
                question
            )



            if not docs:


                st.error(

                    "No related information found in manual/pdf."

                )


                # still show image based on question

                display_images(

                    question,

                    ""

                )



            else:



                context = "\n\n".join(
                    docs
                )



                answer = ask_ollama(

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



                # image based on question + answer

                display_images(

                    question,

                    answer

                )