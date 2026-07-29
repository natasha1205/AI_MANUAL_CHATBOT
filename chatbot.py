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

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2",

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
# CLEAN PDF OUTPUT
# ==================================================

def clean_pdf(text):


    remove_patterns = [

        r"Injection Molding Machine Chapter.*",

        r"Chapter \d+",

        r"V\d+\.\d+",

        r"Page \d+",

        r"Zhafir",

        r"Plastics Machinery",

    ]


    for pattern in remove_patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.I
        )


    text = text.replace(
        "\n",
        " "
    )


    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()



# ==================================================
# FORMAT PDF ANSWER
# ==================================================

def simplify_pdf(text, question):


    text = clean_pdf(text)


    question = question.lower()



    # Maintenance

    if (
        "maintenance" in question
        or
        "check" in question
        or
        "operation" in question
    ):


        return f"""

## Maintenance Information


**Purpose**

The machine must be checked before operation to ensure safe operation.


**Required Check**

• Check machine condition before starting.

• Check all items listed in the maintenance checklist.

• Check safety devices and abnormal conditions.

• Ensure the machine is ready before production.


"""



    sentences = re.split(
        r"\.",
        text
    )


    useful=[]


    for sentence in sentences:


        sentence = sentence.strip()


        if len(sentence)<40:

            continue


        useless_words=[

            "version",

            "chapter",

            "page",

            "manual"

        ]


        if any(
            x in sentence.lower()
            for x in useless_words
        ):

            continue



        useful.append(sentence)



    if not useful:

        return "No accurate information found."



    answer="""

## Information Found


"""


    for item in useful[:5]:


        answer += (

            "• "
            +
            item
            +
            ".\n\n"

        )


    return answer





# ==================================================
# SEARCH ENGINE
# ==================================================

def search_manual(question):


    results = db.similarity_search_with_score(

        question,

        k=5

    )



    if not results:

        return "No accurate information found."



    # DEBUG

    print("\nQUESTION:",
          question)


    for doc,score in results:

        print(
            "\nSCORE:",
            score
        )

        print(
            doc.page_content[:200]
        )



    # ==================================
    # ALARM FIRST
    # ==================================

    for doc,score in results:


        content = doc.page_content


        if (

            "Alarm Name:" in content

            and

            "Solution:" in content

        ):

            return content




    # ==================================
    # PDF
    # ==================================

    doc,score = results[0]


    return simplify_pdf(

        doc.page_content,

        question

    )





# ==================================================
# ALARM FORMAT
# ==================================================

def format_alarm(text):


    lines=text.split("\n")


    output=[]


    for line in lines:


        line=line.strip()


        if line=="":

            continue



        if line.lower().startswith(
            "no:"
        ):

            continue



        output.append(
            line
        )



    return "\n\n".join(output)





# ==================================================
# IMAGE SEARCH
# ==================================================

def find_image(answer):


    images=[]


    answer=answer.lower()



    for keyword,image_list in IMAGE_MAP.items():


        if keyword.lower() in answer:


            for img in image_list:


                if img not in images:

                    images.append(img)



    return images





# ==================================================
# STREAMLIT UI
# ==================================================

st.set_page_config(

    page_title=
    "Machine Manual Assistant"

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


        answer = search_manual(
            question
        )



        st.subheader(
            "Answer:"
        )



        if "Alarm Name:" in answer:


            answer=format_alarm(
                answer
            )


        st.markdown(
            answer
        )



        images=find_image(
            answer
        )


        if images:


            st.subheader(
                "Visual Guide"
            )


            for img in images:


                path=IMAGE_FOLDER/img


                if path.exists():


                    st.image(

                        str(path),

                        use_container_width=True

                    )