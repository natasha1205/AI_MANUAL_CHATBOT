import streamlit as st
from pathlib import Path
import re

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from image_mapping import IMAGE_MAP



# ==================================================
# PATH
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_FOLDER = BASE_DIR / "database"

IMAGE_FOLDER = BASE_DIR / "images"



# ==================================================
# LOAD DATABASE
# ==================================================

@st.cache_resource
def load_database():

    embedding = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2",

        encode_kwargs={
            "normalize_embeddings": True
        }

    )


    db = Chroma(

        collection_name="machine_manual",

        persist_directory=str(DATABASE_FOLDER),

        embedding_function=embedding

    )


    return db



db = load_database()



# ==================================================
# PDF SIMPLE FORMATTER
# ==================================================

def simplify_pdf(text, question):


    text = text.replace("\n", " ")


    question = question.lower()



    if (
        "maintenance" in question
        or
        "check" in question
        or
        "daily" in question
        or
        "operation" in question
    ):


        return """

## Maintenance Checklist

Purpose:
To ensure the machine is safe and ready before operation.


Checklist:

• Check machine condition before starting.

• Check machine parts according to the maintenance checklist.

• Check safety devices and abnormal conditions.

• Ensure safe machine operation before production.

"""



    sentences = re.split(
        r"\.",
        text
    )


    useful = []


    for sentence in sentences:


        sentence = sentence.strip()


        if len(sentence) < 40:

            continue



        remove_words = [

            "chapter",

            "version",

            "page",

            "zhafir",

            "plastics machinery"

        ]


        if any(

            word in sentence.lower()

            for word in remove_words

        ):

            continue



        useful.append(sentence)



    if not useful:

        return "No accurate information found."



    answer = """

## Information

"""


    for item in useful[:5]:


        answer += (

            "• "

            + item

            + ".\n\n"

        )


    return answer





# ==================================================
# SEARCH FUNCTION
# ==================================================

def search_manual(question):


    results = db.similarity_search_with_score(

        question,

        k=5

    )


    if not results:

        return "No accurate information found."



    # =====================================
    # PRIORITY 1
    # ALARM DATABASE
    # =====================================

    for doc, score in results:


        content = doc.page_content


        if (

            "Alarm Name:" in content

            and

            "Solution:" in content

        ):


            return content





    # =====================================
    # PRIORITY 2
    # PDF
    # =====================================

    doc, score = results[0]


    return simplify_pdf(

        doc.page_content,

        question

    )





# ==================================================
# ALARM FORMAT
# ==================================================

def format_alarm(text):


    lines = text.split("\n")


    output = []


    for line in lines:


        line = line.strip()


        if line == "":

            continue



        # Remove No information
        if re.match(

            r"^No\.?\s*[:.]?\s*\d+[-]?\d*",

            line,

            re.I

        ):

            continue



        output.append(line)



    return "\n\n".join(output)





# ==================================================
# IMAGE FINDER
# ==================================================

def find_image(answer):


    images = []


    answer_lower = answer.lower()



    for keyword, image_list in IMAGE_MAP.items():


        if keyword.lower() in answer_lower:


            for img in image_list:


                if img not in images:

                    images.append(img)



    return images





# ==================================================
# STREAMLIT UI
# ==================================================

st.set_page_config(

    page_title="Machine Manual Assistant"

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

            "Please enter question"

        )


    else:


        answer = search_manual(question)



        st.subheader(

            "Answer:"

        )



        # Only format alarm output

        if "Alarm Name:" in answer:


            answer = format_alarm(answer)



        st.markdown(answer)



        # =================================
        # IMAGE DISPLAY
        # =================================

        image_list = find_image(answer)



        if image_list:


            st.subheader(

                "Visual Guide"

            )


            for img in image_list:


                image_path = IMAGE_FOLDER / img


                if image_path.exists():


                    st.image(

                        str(image_path),

                        use_container_width=True

                    )