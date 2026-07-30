import os
import shutil
import chromadb


from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


from langchain_huggingface import HuggingFaceEmbeddings



# ======================================
# PATH
# ======================================


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


MANUAL_FOLDER = os.path.join(
    BASE_DIR,
    "manual"
)


TXT_PATH = os.path.join(
    MANUAL_FOLDER,
    "manual.txt"
)


PDF_PATH = os.path.join(
    MANUAL_FOLDER,
    "operation_manual.pdf"
)



DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database"
)




# ======================================
# DELETE OLD DATABASE
# ======================================


if os.path.exists(DATABASE_PATH):

    print("Removing old database...")

    shutil.rmtree(
        DATABASE_PATH
    )




# ======================================
# LOAD TXT + PDF
# ======================================


documents = []



# ---------- TXT ----------


if os.path.exists(TXT_PATH):

    print("Loading manual.txt...")

    txt_loader = TextLoader(

        TXT_PATH,

        encoding="utf-8"

    )


    txt_documents = txt_loader.load()


    for doc in txt_documents:

        if doc.page_content.strip():

            doc.metadata["source"] = "manual.txt"

            documents.append(doc)



else:

    print(
        "manual.txt not found"
    )




# ---------- PDF ----------


if os.path.exists(PDF_PATH):

    print(
        "Loading operation_manual.pdf..."
    )


    pdf_loader = PyPDFLoader(
        PDF_PATH
    )


    pdf_documents = pdf_loader.load()



    for doc in pdf_documents:


        # remove empty pages

        if doc.page_content.strip():


            doc.metadata["source"] = (
                "operation_manual.pdf"
            )


            documents.append(doc)



else:


    print(
        "operation_manual.pdf not found"
    )





print(
    "\nTotal documents:",
    len(documents)
)




# ======================================
# SPLIT DOCUMENTS
# ======================================


splitter = RecursiveCharacterTextSplitter(

    chunk_size=800,

    chunk_overlap=150

)



chunks = splitter.split_documents(
    documents
)




# remove empty chunks


clean_chunks = []


for doc in chunks:


    text = doc.page_content.strip()


    if text:


        clean_chunks.append(doc)



chunks = clean_chunks



print(

    "Created chunks:",

    len(chunks)

)




# ======================================
# EMBEDDING MODEL
# ======================================


print(
    "Loading embedding model..."
)


embedding_model = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"

)




# ======================================
# CREATE CHROMA
# ======================================


client = chromadb.PersistentClient(

    path=DATABASE_PATH

)



collection = client.create_collection(

    name="manual_library"

)

# ======================================
# INSERT DATA
# ======================================

print(
    "Creating vector database..."
)



for index, doc in enumerate(chunks):


    text = doc.page_content.strip()



    if text == "":

        continue



    collection.add(

        ids=[

            str(index)

        ],


        documents=[

            text

        ],



        metadatas=[

            {

                "source":

                doc.metadata.get(
                    "source",
                    "unknown"
                )

            }

        ]

    )

print(
    "\nLibrary created successfully"
)

print(
    "Total stored:",
    collection.count()
)