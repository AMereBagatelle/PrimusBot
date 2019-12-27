def writeLines(filename, toWrite):
    with open(filename, 'w') as fp:
        fp.writelines()

def readLines(filename):
    with open(filename, 'r') as fp:
        return fp.readlines()

def writeToLineOfFile(filename, line, content):
    content = content + '\n'
    with open(filename) as fp:
        lines = fp.readlines()
    if len(lines) == 0:
        lines = content
        with open(filename, 'w') as fp:
            fp.writelines(lines)
    else:
        if (len(lines) - 1) < line:
            lines.append(content)
        else:
            lines[line] = content
        fp = open(filename, 'w')
        fp.writelines(lines)
        fp.close()
        
def readLineOfFile(filename, line):
    with open(filename) as fp:
        return fp.readlines()[line]

def writeStr(filename, toWrite):
    with open(filename, 'w') as fp:
        fp.write(toWrite)

def readStr(filename, toWrite):
    with open(filename) as fp:
        return fp.read()