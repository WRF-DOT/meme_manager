from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from pathlib import Path
app = FastAPI()

UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get('/')
def root():
    return{'message':'表情包管理工具'}
@app.get("/meme/{meme_id}")
def get_meme(meme_id: int):
    return {"meme_id": meme_id, "name": f"表情包{meme_id}"}

@app.post('/upload')
async def upload_imgs(file:UploadFile=File(...)):

    content=await file.read()
    MAX_SIZE=5*1024*1024
    if len(content)>MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f'文件过大,最大支持5MB,当前文件大小{len(content)/1024/1024:.2f}MB'
        )
    if not file.content_type.startswith('image/') :
        raise HTTPException(
            status_code=400,
            detail=f'只允许上传文件,当前文件类型为{file.content_type}'
        )   

    file_extensiom=os.path.splitext(file.filename)[1]
    uniqed_nime=uuid.uuid4().hex
    file_name=(f'{uniqed_nime}{file_extensiom}')
    file_path=UPLOAD_DIR/file_name
    with open(file_path,'wb')as f:
        f.write(content)
    return{
        "filename":file_name,
        'origai_name':file.filename,
        'path':str(file_path) ,
        'size.kb':len(content)//1024,
        'contedt_type':file.content_type
    }
@app.get('/images/{filename}')
def get_image(filename:str):
    file_path=UPLOAD_DIR/filename
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f'您查找的{filename}不存在'
        )
    return FileResponse(
        file_path
    )
