for i in range(1,3):
    file = open(str(i)+".txt", "r")
    a = file.read()
    file.close()
    f = open(str(i)+".txt", "w+")
    x=str(a[2:len(a)-2])+" 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
    print(x)
    f.write("ball 0.0 0 0.0 "+x)
    f.close()
