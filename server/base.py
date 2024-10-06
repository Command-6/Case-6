from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from datetime import datetime
from io import BytesIO
import psycopg2
import spacy
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
nlp = spacy.load("ru_sentiment_model")
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")
def connect_db():
    conn = psycopg2.connect(
        dbname="Book_Neiro",
        user="postgres",
        password="21042005",
        host="localhost",
        port="5432"
    )
    return conn

class Element:
    def __init__(self, id: int, name: str, author: str, disc: str, file_1: bytes, file_2: bytes, file_3: bytes, date: str, photo: bytes):
        self.id = id
        self.name = name
        self.author = author
        self.disc = disc
        self.file_1 = file_1
        self.file_2 = file_2
        self.file_3 = file_3
        self.date = date
        self.photo = photo



@app.post("/create_element")
async def create_element(name: str, author: str, disc: str, file_1: UploadFile = File(...),  file_2: UploadFile = File(...), file_3: UploadFile = File(...), photo: UploadFile = File(...)):
    conn = connect_db()
    curr = conn.cursor()

    contents = await file_1.read()
    text = contents.decode('utf-8')
    words = text.split()
    word_count = len(words)
    flags_count = word_count/10000
    if (flags_count < 1):
        flags_count = 5
    doc = nlp(text)

    sentences = list(doc.sents)
    print(sentences)
    negative_count = 0
    for sent in sentences:
        doc_sent = nlp(sent.text)
        


        if doc_sent.cats['NEGATIVE'] >= 0.5:
            negative_count += 1

    k = negative_count
    current_datetime = datetime.now()
    print(k)
    print(flags_count)
    if flags_count >= k:
        file_d_1 = contents
        file_d_2 = await file_2.read()
        file_d_3 = await file_3.read()
        photo_d = await photo.read()
        curr.execute("""INSERT INTO books (name, author, disc, file_txt, file_fb2, file_docx, date, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """, (name, author, disc, file_d_1, file_d_2, file_d_3, current_datetime, photo_d))
        conn.commit()
        curr.close()
        conn.close()
        return 1
    else:
        return 0

@app.get("/get_elemets")
async def get_elemets():
    conn = connect_db()
    curr = conn.cursor()

    curr.execute("""SELECT * FROM books""")
    rows = curr.fetchall()
    items = []
    for row in rows:
        item = {
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "disc": row[3],
            "file_1": base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
            "file_2": base64.b64encode(row[5]).decode('utf-8') if row[5] else None,
            "file_3": base64.b64encode(row[6]).decode('utf-8') if row[6] else None,
            "date": row[7],
            "photo": base64.b64encode(row[8]).decode('utf-8') if row[8] else None
        }
        items.append(item)
    curr.close()
    conn.close()
    return items

@app.get("/search_element")
async def search_element(search: str):
    conn = connect_db()
    curr = conn.cursor()
    
    curr.execute("""SELECT * FROM books WHERE name ILIKE %s OR author ILIKE %s""", (search, search))

    rows = curr.fetchall()
    items = []
    for row in rows:
        item = {
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "disc": row[3],
            "file_1": base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
            "file_2": base64.b64encode(row[5]).decode('utf-8') if row[5] else None,
            "file_3": base64.b64encode(row[6]).decode('utf-8') if row[6] else None,
            "date": row[7],
            "photo": base64.b64encode(row[8]).decode('utf-8') if row[8] else None
        }

        items.append(item)
    curr.close()
    conn.close()
    return items

@app.get("/random_element")
async def random_element():
    conn = connect_db()
    curr = conn.cursor()

    curr.execute("""SELECT * FROM books ORDER BY RANDOM() LIMIT 1""")
    rows = curr.fetchall()
    items = []
    for row in rows:
        item = {
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "disc": row[3],
            "file_1": base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
            "file_2": base64.b64encode(row[5]).decode('utf-8') if row[5] else None,
            "file_3": base64.b64encode(row[6]).decode('utf-8') if row[6] else None,
            "date": row[7],
            "photo": base64.b64encode(row[8]).decode('utf-8') if row[8] else None
        }

        items.append(item)
    curr.close()
    conn.close()
    return items
    

    
