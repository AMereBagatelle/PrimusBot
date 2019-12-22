def writeLines(filename, toWrite):
    with open(filename, 'w') as fp:
        fp.writelines()

def readLines(filename):
    with open(filename, 'r') as fp:
        return fp.readlines()

def writeToLineOfFile(filename, line, content):
    with open(filename) as fp:
        lines = fp.readlines()
    if len(lines) == 0:
        lines = content
        with open(filename, 'w') as fp:
            fp.writelines(lines)
    else:
        lines[line] = content
        fp = open(filename, 'w')
        fp.writelines(lines)
        fp.close()
        
def readLineOfFile(filename, line):
    with open(filename) as fp:
        return fp.readlines()[line]