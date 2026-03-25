import database
from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from pathlib import Path
app = FastAPI()
@app.on_event("startup")
async def startup_event():
    await database.init_db()

UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get('/')                                                               #测试api链接
def root():
    return{'message':'表情包管理工具'}
@app.get("/meme/{meme_id}")                                                 #测试获取返回值
def get_meme(meme_id: int):
    return {"meme_id": meme_id, "name": f"表情包{meme_id}"}

@app.post('/upload')                                                      #  图片获取
async def upload_imgs(file:UploadFile=File(...)):

    content=await file.read()                                               #读取图片，只能读取一次，类似指针，读取后就指向后面读不了了
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
    conn=await database.get_db()
    try:
        await conn.execute('''
            INSERT INTO images(filename,original_name,filepath,size_kb)
            VALUES(?,?,?,?)               

            ''',(file_name,file.filename,str(file_path),len(content)//1024))
        await conn.commit()
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500,detail=f'保存失败{str(e)}')
    finally:
        await conn.close()
        
    return{
        "filename":file_name,
        'original_name':file.filename,
        'path':str(file_path) ,
        'size_kb':len(content)//1024,
        'content_type':file.content_type
    }

@app.get('/images')
async def list_images():
    conn = await database.get_db()
    try:
        cursor=await conn.execute("SELECT* FROM images ORDER BY created_at DESC")
        images= await cursor.fetchall()
        result=[]
        for img in images:
            result.append({
                'id':img['id'],
                'filename':img['filename'],
               'original_name':img['original_name'],
               'size_kb':img['size_kb'],
               'created_at':img['created_at'],
               'url':f'/images/{img['filename']}'
            }

            )
        return{'imanges':result,"count":len(result)}
    finally:
        await conn.close()
@app.delete('/images/{image_id}')
async def delete_image(image_id:int):
    conn=await database.get_db()
    try:
        cursor =await conn.execute('SELECT * FROM images WHERE id = ?',(image_id,))
        image = await cursor.fetchone()

        if not image:
            raise HTTPException(status_code=404,detail=f"图片id:{image_id}不存在")
        file_path=Path(image["filepath"])
        if file_path.exists():
            file_path.unlink()
        await conn.execute("DELETE FROM images WHERE id = ?",(image_id,))
        await conn.commit()
        return{'success':'true','message':f'已删除{image['original_name']}'}
    finally:
        await conn.close()


@app.get('/images/{filename}')      #通过指定名称查找图片
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
