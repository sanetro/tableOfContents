import sys

def countHashes(word):
    result = 0
    for w in word:
        if w == "#":
            result += 1
    return result

def clearHashes(word):
    return word[countHashes(word)+1:-1]

def findHeaders(content):    
    index = 0
    headers = []
    locked = False
    isMarked = False
        
    for word in content:
        index += 1
        print(word[:3])
        if word[:3] == '```' and not isMarked:
            locked = True
            print("Ping")
        if word[:3] == '```' and isMarked:
            locked = False
            print("Pong")

        
        if "#" in word[0] and not locked:
            headers.append({
                "index" : index,
                "level" : countHashes(word),
                "name" : clearHashes(word)
            })
    return headers

def makeTabs(no):
    return "\t" * no

def numerate(numbers):
    return ".".join(map(str, numbers))

def makeTreeOfContents(doc, content, filename):
    with open(f"output-{filename}", "w") as f:
        current_numbering = [0]
        f.write("# Spis tresci\n")
        for head in doc:
            level = head['level']
            current_numbering = current_numbering[:level]  
            current_numbering[-1] += 1  
            numerating = numerate(current_numbering)
            title = head['name']
            tabs = makeTabs(level)
            tmp = f"{tabs}{numerating}. {title}\n"
            f.write(tmp)
            current_numbering.append(0)  
        for lines in content:
            f.write(lines)

def main():
    if len(sys.argv) != 2:
        print("Use: python <name>.py <name>.md")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            content = f.readlines()
    except FileNotFoundError:
        print(f"Plik '{filename}' nie istnieje.")
        sys.exit(1)

    doc = findHeaders(content)
    makeTreeOfContents(doc, content, filename)

if __name__ == "__main__":
    main()
