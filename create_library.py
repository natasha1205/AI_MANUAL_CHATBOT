import re
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MANUAL_FILE = (
    BASE_DIR /
    "manual" /
    "manual.txt"
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


    if not MANUAL_FILE.exists():

        raise FileNotFoundError(
            "manual.txt not found"
        )


    print(
        "Manual found:",
        MANUAL_FILE
    )


    text = MANUAL_FILE.read_text(
        encoding="utf-8"
    )



    documents = split_alarm_records(
        text
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