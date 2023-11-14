def f(n):
    with open('wiki_dump.xml', 'r') as file:
        for i in range(n):
            line = file.readline()
            print(line)
            
f(1000)
