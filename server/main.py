from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

import uuid
import pandas as pd
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount('/static',StaticFiles(directory="static"),name="static")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/upload-file')
def add_file(type='INPUT', parent_id=0, db:Session=Depends(get_db),file:UploadFile=File(...)):
    fname, ext = os.path.splitext(file.filename)
    
    text = str(uuid.uuid4().hex) + ext
    old_name = file.filename
    contents = file.file.read()
    with open(f"./static/"+text,'wb') as f:
        f.write(contents)
    return crud.create_upload_file(db, old_name=old_name,new_name=text, type=type, parent_id=parent_id)


@app.get("/upload-files", response_model=list[schemas.upload_file])
async def get_list(db:Session=Depends(get_db)):
    return crud.get_list_upload_files(db)


@app.get("/upload-files/{parent_id}", response_model=list[schemas.upload_file])
async def get_list(parent_id: int, db:Session=Depends(get_db)):
    return crud.get_list_upload_files_by_owner(db, parent_id)


@app.get("/download-file",)
async def download_file(input_id: int, db:Session=Depends(get_db)):
    input_file = crud.get_upload_file(db, input_id)
    return FileResponse(path='./static/' + input_file.new_name, filename=input_file.old_name, media_type="application/png")


@app.delete("/upload-file/{input_id}",)
async def delete_upload_files(input_id: int, db:Session=Depends(get_db)):
    crud.delete_upload_files(db, input_id)
# @app.post("/upload")
# async def upload_excel_parser(file: UploadFile = File(...)):
#     content = await file.read()
#     df = pd.read_excel(BytesIO(content))
#     return "success"


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0',port=5000)