def depeng_meme(name,tags,size):
    if size>=1024:
        return None
    tags_str=' '.join(['#'+t for t in tags ])
    return{
        "name":name,
        'tags':tags_str,
        'size':size
    }
name='cat'
tags=['quit','main']
size=100

meme=depeng_meme(name,tags,size)
print(meme['tags'])