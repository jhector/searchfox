import json
import sys
import mmap
import os.path

mozSearchPath = sys.argv[1]
indexPath = sys.argv[2]

f = None
mm = None
crossrefs = {}

def load(indexPath):
    global f, mm

    f = open(os.path.join(indexPath, 'crossref'))
    mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    f.close()

    key = None
    pos = 0

    while True:
        line = mm.readline()
        if line == '':
            break

        if key == None:
            pos += len(line)
            key = line.strip()
        else:
            value = line.strip()
            s = "{},{}".format(pos, pos + len(value))
            crossrefs[key] = s
            key = None
            pos += len(line)

def lookup(symbol):
    s = crossrefs.get(symbol)
    if s == None:
        return {}

    (startPos, endPos) = s.split(',')
    (startPos, endPos) = (int(startPos), int(endPos))

    data = mm[startPos:endPos]
    result = json.loads(data)
    f.close()
    return result
