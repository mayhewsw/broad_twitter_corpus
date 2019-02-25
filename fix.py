with open("f.conll") as f:
    lines = f.readlines()

with open("f.conll.fix", "w") as out:
    nextI = False
    for line in lines:
        sline = line.split()
        if len(sline) == 2:
            word,tag = sline
            
            if nextI:
                tag = "I" + tag[1:]
                nextI = False
                
            if word == "@" and tag != "O":
                nextI = True

            out.write("{} {}\n".format(word,tag))
        else:
            out.write(line)
                      
