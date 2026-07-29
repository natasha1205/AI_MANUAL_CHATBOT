import streamlit as st
from pathlib import Path
import re

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from image_mapping import IMAGE_MAP 



# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_FOLDER = BASE_DIR / "database"

IMAGE_FOLDER = BASE_DIR / "images"



# ==========================================
# LOAD DATABASE
# ==========================================

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



# ==========================================
# FORMAT PDF ANSWER
# ==========================================

def clean_pdf_answer(text, question):


    question_words = question.lower().split()


    sentences = re.split(

        r'[\n.]',

        text

    )


    useful = []



    remove_words = [

        "chapter",

        "version",

        "zhafir",

        "plastics machinery",

        "page",

        "manual",

        "contents"

    ]



    for sentence in sentences:


        sentence = sentence.strip()


        if len(sentence) < 40:

            continue



        lower = sentence.lower()



        # remove useless PDF heading

        if any(

            word in lower

            for word in remove_words

        ):

            continue



        # check relevance

        score = 0


        for word in question_words:


            if len(word) > 3 and word in lower:

                score += 1



        if score > 0:

            useful.append(sentence)



    if not useful:


        return "No related information found."



    answer = """

## Related Information

"""



    for item in useful[:6]:


        answer += (

            "• "

            +

            item

            +

            "\n\n"

        )



    return answer




# ==========================================
# SEARCH MANUAL
# ==========================================

def search_manual(question):


    results = db.similarity_search_with_score(

        question,

        k=10

    )



    if not results:


        return "No accurate information found."



    # ======================================
    # ALARM SEARCH FIRST
    # ======================================

    for doc,score in results:


        content = doc.page_content



        if (

            "Alarm Name:" in content

            and

            "Solution:" in content

        ):


            return format_alarm(content)



    # ======================================
    # PDF SEARCH
    # ======================================


    matched_text = ""



    for doc,score in results:


        text = doc.page_content


        question_word = question.lower().split()


        match = 0



        for word in question_word:


            if len(word)>3 and word in text.lower():

                match += 1



        if match >= 1:


            matched_text += (

                text

                +

                "\n"

            )



    if matched_text == "":


        return "No related information found."



    return clean_pdf_answer(

        matched_text,

        question

    )




# ==========================================
# FORMAT ALARM OUTPUT
# ==========================================

def format_alarm(text):


    lines = text.split("\n")


    output = ""



    for line in lines:


        line=line.strip()



        if line=="":

            continue



        # remove No:xxx

        if re.match(

            r"^No\.?\s*:?\s*\d+",

            line,

            re.I

        ):

            continue



        output += (

            line

            +

            "\n\n"

        )



    return output




# ==========================================
# IMAGE FINDER
# ==========================================

def find_image(question):


    images=[]


    question = question.lower()



    for keyword,image_list in IMAGE_MAP.items():


        if keyword.lower() in question:


            for img in image_list:


                if img not in images:


                    images.append(img)



    return images




# ==========================================
# STREAMLIT UI
# ==========================================

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


    if question.strip()=="":


        st.warning(

            "Please enter question"

        )


    else:


        answer = search_manual(question)



        st.subheader(

            "Answer:"

        )



        st.markdown(

            answer

        )



        # image display

        image_list = find_image(question)



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