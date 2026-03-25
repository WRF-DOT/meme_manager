#数据库模块
import aiosqlite
import os
from pathlib import Path
DATABASE = Path(__file__).parent/"memes.db"

async def get_db():
    conn=await aiosqlite.connect(str(DATABASE))
    conn.row_factory=aiosqlite.Row
    return conn

async def init_db():
    conn=await get_db() 
    
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS images(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                filepath TEXT NOT NULL,
                size_kb INTEGER,
                created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        ''')
        await conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON images(created_at)')
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_filename ON images(filename)")
        await conn.commit()
        print("数据库初始化完成")
    except aiosqlite.Error as e:
        print(f"数据库初始化失败：{e}")
        await conn.rollback()
    finally:
        await conn.close()
if __name__=='__main__':
    import asyncio
    asyncio.run(init_db())