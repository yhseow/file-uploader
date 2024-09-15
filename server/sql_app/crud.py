from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
from . import models, schemas

def get_list_upload_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.upload_file).offset(skip).limit(limit).all()

def get_upload_file(db: Session, id: int):
    return db.query(models.upload_file).filter(models.upload_file.id == id).first()


def get_list_upload_files_by_owner(db: Session, parent_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.upload_file).filter(models.upload_file.parent_id == parent_id).offset(skip).limit(limit).all()

def create_upload_file(db: Session, old_name, new_name, type='INPUT', parent_id=0):
    new_file = models.upload_file(old_name=old_name,new_name=new_name, type=type, parent_id=parent_id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def delete_upload_files(db: Session, id: int):
    uf = get_upload_file(db, id)
    if not uf:
        raise HTTPException(status_code=404, detail="Upload file not found")
    output = get_list_upload_files_by_owner(db, id)
    for f in output:
        print(f.new_name)
        if os.path.exists('./static/' + f.new_name):
            os.remove('./static/' + f.new_name)
    if os.path.exists('./static/' + uf.new_name):
        os.remove('./static/' + uf.new_name)
        
    delete_query = models.upload_file.__table__.delete().where(models.upload_file.parent_id == id)
    db.execute(delete_query)
    db.delete(uf)
    db.commit()
    return { "ok": True }