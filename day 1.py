name='DDD'
print(name)
print(type(name))
tags=[1,2,3]
print(tags)
tags.append(4)#append是添加到列表的最后
print(tags)
#列表的常见用法
tags.insert(0,0)#tags.insert(位置，内容)在指定位置添加指定内容
print(tags)
tags.remove(0)#remove删除列表中指定内容
print(tags)
last=tags.pop()#删除最后一个并返回
print(last)
print(tags)
print(len(tags))#len获取列表长度
#字典
meme={
    'name':'cat',
    'tags':['可爱','难受']              #建立映射
}
print(meme['name'])
print(meme['tags'])                    #键是常量，所以要加引号'tags',变量不用加
meme['kind']=['故事','情绪']
meme['name']='dogs'
print(meme)
#字典的值可以是任何内容，甚至是另外一个嵌套字典
meme['likes']=likes={
    'time':1,
    'number':['1','2']
}
print(meme['likes']['time'])           #要选择一个字典里嵌套的字典需要再加一个括号
#在要描述一个对象的多个值时可以用
#配置信息
#列表对应用一个类型的多组数据，字典是一个对象的多个属性
#函数
def message():
    print('图片已保存')                 #python中严格缩进，函数内容要缩进
message()                              #（）代表执行，没有括号就是不执行
# print(massage)
def message_save(DDD):
    print(f"已保存在:{DDD}")            #要在格式化字符串前面加上f不然只会当作普通字符串输出
message_save("endplice")
def add(a,b):
    print(f"{a}+{b}={a+b}")
    c=a+b
    return c                           #return代表返回值
add(1,2)
answer=add(3,7)
print(answer)
#if
if 1+1==2:
    print("ture")                      #:后代表下面是要执行的代码块，   tab缩进表明有缩进的都属于他要用的代码，python不使用{}来包裹

import os   # 导入操作系统模块

filename = "cat.jpg"

if os.path.exists(filename):
    print(f"{filename} 存在")
else:
    print(f"{filename} 不存在")
#for循环
tags = ["睡觉", "搞笑", "猫"]

for tag in tags:                       #for变量in可迭代对象
    print(tag)                         #每次执行的代码
word = "hello"

for letter in word:                    #遍历字符串
    print(letter)

for tags in meme:                      #遍历键
    print(tags)
# for value in meme['kind']:             不能这么写，这么写返回的是字符串，会变成遍历字符串
#     print(value)
for value in meme.values():
    print(value)
for key, value in meme.items():
    print(f"{key}:{value}")
# range(5) 生成 0,1,2,3,4
for i in range(5):
    print(i)

# range(1, 5) 生成 1,2,3,4
for i in range(1, 5):
    print(i)

# range(1, 10, 2) 生成 1,3,5,7,9（步长2）
for i in range(1, 10, 2):
    print(i)
