# Open the file
with open('your_large_file.xml', 'r') as file:
    # Read and print the first 1000 lines
    for i in range(1000):
        line = file.readline()
        print(line)
