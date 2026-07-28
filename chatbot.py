import re
from pathlib import Path

import streamlit as st

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ===============================
# IMAGE MAPPING
# ===============================

from image_mapping import find_related_image



# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Machine#1 Manual Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("Machine#1 Manual Assistant")



# ===============================
# LANGUAGE
# ===============================

language = st.selectbox(
    "Select Language:",
    [
        "English",
        "Bahasa Melayu"
    ]
)



# ===============================
# PATH
# ===============================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_FOLDER = BASE_DIR / "database"

IMAGE_FOLDER = BASE_DIR / "images"




# ===============================
# EMBEDDING
# ===============================

@st.cache_resource
def load_embedding():

    return HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2",

        encode_kwargs={
            "normalize_embeddings": True
        }

    )





# ===============================
# LOAD DATABASE
# ===============================

@st.cache_resource
def load_database():

    return Chroma(

        collection_name="machine_manual",

        persist_directory=
        str(DATABASE_FOLDER),

        embedding_function=
        load_embedding()

    )



database = load_database()





# ===============================
# SEARCH MANUAL
# ===============================

def search_manual(question):


    results = database.similarity_search(

        question,

        k=1

    )


    if results:

        return results[0]


    return None





# ===============================
# FORMAT OUTPUT
# ===============================

def format_output(text):


    # remove No.

    text = re.sub(

        r"No\.\s*:\s*\d+",

        "",

        text

    )



    fields = [

        "Alarm Name",

        "Description",

        "Cause",

        "Screen Display / Alarm Light",

        "Machine State After Alarm",

        "Solution"

    ]



    for field in fields:


        text = text.replace(

            field + ":",

            "\n\n" + field + ":"

        )



    return text.strip()





# ===============================
# TRANSLATION
# ===============================

def translate_output(text):


    if language == "English":

        return text



    dictionary = {


        "Alarm Name":
        "Nama Alarm",


        "Description":
        "Penerangan",


        "Cause":
        "Punca",


        "Screen Display / Alarm Light":
        "Paparan Skrin / Lampu Alarm",


        "Machine State After Alarm":
        "Keadaan Mesin Selepas Alarm",


        "Solution":
        "Penyelesaian"

    }



    for eng,bm in dictionary.items():


        text=text.replace(

            eng + ":",

            bm + ":"

        )



    return text







# ===============================
# DISPLAY IMAGE
# ===============================

def display_images(question):


    images = find_related_image(question)



    if not images:

        return



    st.subheader(
        "Visual Guide"
    )



    for img in images:


        image_path = IMAGE_FOLDER / img



        if image_path.exists():


            st.image(

                str(image_path),

                caption=img,

                use_container_width=True

            )



        else:


            st.warning(

                f"Image missing: {img}"

            )









# ===============================
# USER INPUT
# ===============================


if language=="English":

    label="Enter your question:"

    button="Search"


else:

    label="Masukkan soalan anda:"

    button="Cari"




question = st.text_input(label)





# ===============================
# SEARCH BUTTON
# ===============================

if st.button(button):


    if question.strip()=="":


        st.warning(

            "Please enter question"

        )


    else:


        with st.spinner(

            "Searching manual..."

        ):



            result = search_manual(question)





        if result:


            answer = format_output(

                result.page_content

            )



            answer = translate_output(

                answer

            )



            # TEXT OUTPUT

            st.write(answer)



            # IMAGE OUTPUT

            display_images(question)





        else:


            st.warning(

                "Information not found in manual"

            )