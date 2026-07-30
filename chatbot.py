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
# LOAD CHROMA DATABASE
# ======================================

client = chromadb.PersistentClient(
    path=DATABASE_PATH
)


collection = client.get_collection(
    name="manual_library"
)


# ======================================
# CHECK USER QUESTION
# ======================================

def validate_question(question):


    question = question.lower().strip()


    # General greetings / unrelated words

    invalid_questions = [

        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "help",
        "test"

    ]


    for word in invalid_questions:


        if question == word:

            return False



    # Minimum length

    if len(question.split()) < 3:

        return False



    # Machine related keywords

    machine_keywords = [

        "alarm",
        "error",
        "fault",
        "machine",
        "motor",
        "sensor",
        "temperature",
        "pressure",
        "hydraulic",
        "servo",
        "pump",
        "valve",
        "reset",
        "replace",
        "change",
        "maintenance",
        "problem",
        "issue",
        "screen",
        "display",
        "safety",
        "gate",
        "controller",
        "barrel",
        "mold"

    ]



    for keyword in machine_keywords:


        if keyword in question:

            return True



    return False

# ======================================
# SEARCH MANUAL + PDF
# ======================================

def search_manual(question):


    result = collection.query(

        query_texts=[
            question
        ],

        n_results=1,

        include=[
            "documents",
            "metadatas"
        ]

    )


    documents = result.get(
        "documents",
        []
    )


    metadatas = result.get(
        "metadatas",
        []
    )


    if documents and documents[0]:

        return documents[0], metadatas[0]


    return [], []







# ======================================
# CLEAN TEXT
# ======================================

def clean_text(text):


    text = re.sub(

        r"\n{2,}",

        "\n",

        text

    )


    text = text.replace(
        "\t",
        " "
    )


    return text.strip()





# ======================================
# EXTRACT ALARM INFORMATION
# ======================================

def extract_alarm(text):


    alarm = ""
    description = ""
    cause = ""
    screen = ""
    machine = ""
    solution = ""



    # Remove page number

    text = re.sub(

        r"No\.\s*:\s*\d+",

        "",

        text

    )



    # Alarm Name

    match = re.search(

        r"Alarm Name[:\s]*(.*?)(?=Description|$)",

        text,

        re.I | re.S

    )


    if match:

        alarm = match.group(1).strip()




    # Description

    match = re.search(

        r"Description[:\s]*(.*?)(?=Cause|$)",

        text,

        re.I | re.S

    )


    if match:

        description = match.group(1).strip()




    # Cause

    match = re.search(

        r"Cause[:\s]*(.*?)(?=Screen Display|Alarm Light|$)",

        text,

        re.I | re.S

    )


    if match:

        cause = match.group(1).strip()




    # Screen Display

    match = re.search(

        r"(?:Screen Display|Alarm Light)[:\s]*(.*?)(?=Machine State|$)",

        text,

        re.I | re.S

    )


    if match:

        screen = match.group(1).strip()




    # Machine State

    match = re.search(

        r"Machine State(?: After Alarm)?[:\s]*(.*?)(?=Solution|$)",

        text,

        re.I | re.S

    )


    if match:

        machine = match.group(1).strip()




    # Solution

    match = re.search(

        r"Solution[:\s]*(.*)",

        text,

        re.I | re.S

    )


    if match:

        solution = match.group(1).strip()




    return {

        "alarm":alarm,

        "description":description,

        "cause":cause,

        "screen":screen,

        "machine":machine,

        "solution":solution

    }





def format_answer(documents, language):

    text = "\n".join(documents)

    text = clean_text(text)

    data = extract_alarm(text)


    if language == "Malay":

        answer = f"""
Nama Alarm: {data["alarm"]}

Penerangan: {data["description"]}

Punca: {data["cause"]}

Paparan Skrin: {data["screen"]}

Keadaan Mesin: {data["machine"]}

Penyelesaian: {data["solution"]}
"""


    else:

        answer = f"""
Alarm Name: {data["alarm"]}

Description: {data["description"]}

Cause: {data["cause"]}

Screen Display: {data["screen"]}

Machine State: {data["machine"]}

Solution: {data["solution"]}
"""


    return answer




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


        img_path=os.path.join(

            IMAGE_FOLDER,

            img

        )


        if os.path.exists(img_path):


            st.image(

                img_path,

                use_container_width=True

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


    if question.strip()=="":


        st.warning(
            "Please enter your question."
        )


    elif not validate_question(question):


        st.warning(
            "Please ask a more specific question related to the machine manual. Example: 'How to reset safety gate alarm?'"
        )


    else:

        with st.spinner(
            "Searching manual database..."
        ):


            docs, source = search_manual(
                question
            )


            if not docs:


                st.error(
                    "No related information found in manual."
                )


            else:


                answer = format_answer(
                    docs,
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