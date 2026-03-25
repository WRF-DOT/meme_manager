import aiosqlite
import asyncio

async def test():
    try:
        # 直接用当前目录下的文件
        conn = await aiosqlite.connect("test.db")
        print("✓ 连接成功")
        
        await conn.execute("CREATE TABLE test (id INTEGER)")
        print("✓ 创建表成功")
        
        await conn.commit()
        await conn.close()
        print("✓ 全部成功")
        
    except Exception as e:
        print(f"✗ 失败：{e}")

asyncio.run(test())