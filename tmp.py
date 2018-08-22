def iter(f):
    while True:
        line=f.readline()
        if line==b"":
            break
        yield line 
    return
f=open("Dataset/Data-9000","rb")
for x in iter(f):
    print(x)