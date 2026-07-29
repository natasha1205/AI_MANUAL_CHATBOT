import shutil
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader



# =====================================
# PATH
# =====================================

BASE_DIR = Path(__file__).resolve().parent

MANUAL_FOLDER = BASE_DIR / "manual"

DATABASE_FOLDER = BASE_DIR / "database"




# =====================================
# CLEAN PDF TEXT
# =====================================

def clean_pdf_text(text):


    # remove new line

    text = text.replace(
        "\n",
        " "
    )


    # remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    )



    remove_words = [

        "Injection Molding Machine",

        "Chapter",

        "V3.0",

        "Zhafir",

        "Plastics Machinery",

        "Page"

    ]



    for word in remove_words:


        text = text.replace(

            word,

            ""

        )



    # remove page number

    text = re.sub(

        r"\b\d+-\d+\b",

        "",

        text

    )



    # remove function keys

    text = re.sub(

        r"F[1-8]",

        "",

        text

    )


    return text.strip()





# =====================================
# LOAD TXT
# =====================================

def load_txt():


    documents=[]


    txt_file = MANUAL_FOLDER / "manual.txt"



    if txt_file.exists():


        print(
            "Loading manual.txt"
        )



        text = txt_file.read_text(

            encoding="utf-8"

        )



        parts = text.split(

            "Alarm Name:"

        )



        for part in parts:


            if part.strip()=="":

                continue



            content = (

                "Alarm Name:"

                +

                part

            )



            documents.append(


                Document(

                    page_content=content,

                    metadata={

                        "source":"manual.txt"

                    }

                )

            )



    return documents





# =====================================
# LOAD PDF
# =====================================

def load_pdf():


    documents=[]



    pdf_files=list(

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



        pages = loader.load()



        print(

            "PDF pages:",

            len(pages)

        )




        for page in pages:



            cleaned = clean_pdf_text(

                page.page_content

            )



            if len(cleaned)>100:



                documents.append(


                    Document(

                        page_content=cleaned,

                        metadata={

                            "source":"PDF",

                            "file":pdf.name

                        }

                    )

                )



    return documents





# =====================================
# CREATE DATABASE
# =====================================

def main():


    print(
        "Program started..."
    )



    documents=[]



    txt_documents = load_txt()


    pdf_documents = load_pdf()



    documents.extend(

        txt_documents

    )


    documents.extend(

        pdf_documents

    )



    print(

        "TXT documents:",

        len(txt_documents)

    )


    print(

        "PDF documents:",

        len(pdf_documents)

    )


    print(

        "Total documents:",

        len(documents)

    )



    embedding = HuggingFaceEmbeddings(


        model_name=

        "sentence-transformers/all-MiniLM-L6-v2",


        encode_kwargs={

            "normalize_embeddings":True

        }


    )



    if DATABASE_FOLDER.exists():


        print(

            "Deleting old database..."

        )


        shutil.rmtree(

            DATABASE_FOLDER

        )



    Chroma.from_documents(


        documents,


        embedding,


        collection_name=

        "machine_manual",


        persist_directory=

        str(DATABASE_FOLDER)

    )



    print(

        "Database created successfully"

    )




if __name__=="__main__":

    main()