import re
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader


# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MANUAL_FOLDER = (
    BASE_DIR /
    "manual" 
)

DATABASE_FOLDER = (
    BASE_DIR /
    "database"
)



# ==========================================
# EXTRACT FIELD
# ==========================================

def extract_field(text, field):

    pattern = (
        rf"{field}\s*:\s*(.*)"
    )

    result = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if result:
        return result.group(1).strip()

    return ""



# ==========================================
# SPLIT MANUAL RECORD
# ==========================================

def split_alarm_records(text):

    records = []


    # Every alarm starts with Alarm Name
    parts = re.split(
        r"(?=Alarm Name:)",
        text
    )


    for part in parts:


        if "Alarm Name:" not in part:
            continue



        alarm_name = extract_field(
            part,
            "Alarm Name"
        )


        description = extract_field(
            part,
            "Description"
        )


        cause = extract_field(
            part,
            "Cause"
        )


        solution = extract_field(
            part,
            "Solution"
        )


        # Create searchable keywords

        search_text = (
            alarm_name
            + " "
            + description
            + " "
            + cause
            + " "
            + solution
        ).lower()



        document = Document(

            page_content=
            part.strip(),


            metadata={

                "alarm_name":
                alarm_name,


                "search_text":
                search_text

            }

        )


        records.append(document)



    return records




# ==========================================
# CREATE DATABASE
# ==========================================

def main():


    print("Program started...")


documents = []

# ============================
# Load manual.txt
# ============================

txt_file = MANUAL_FOLDER / "manual.txt"

if txt_file.exists():

    print("Loading manual.txt")

    text = txt_file.read_text(
        encoding="utf-8"
    )

    documents.extend(
        split_alarm_records(text)
    )


# ============================
# Load PDF manual
# ============================

pdf_files = list(
    MANUAL_FOLDER.glob("*.pdf")
)


for pdf in pdf_files:

    print(
        "Loading PDF:",
        pdf.name
    )

    loader = PyPDFLoader(
        str(pdf)
    )

    pdf_documents = loader.load()


    documents.extend(
        pdf_documents
    )



print(
    "Total documents:",
    len(documents)
)


print(
        "Alarm records found:",
        len(documents)
    )



embedding = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2",

        encode_kwargs={
            "normalize_embeddings": True
        }

    )



if DATABASE_FOLDER.exists():

        print(
            "Removing old database..."
        )

        shutil.rmtree(
            DATABASE_FOLDER
        )



print(
        "Creating database..."
    )


Chroma.from_documents(

        documents=documents,

        embedding=embedding,

        collection_name=
        "machine_manual",

        persist_directory=
        str(DATABASE_FOLDER)

    )


print(
        "Database created successfully"
    )



if __name__ == "__main__":

    main()