#!/usr/bin/python
from __future__ import print_function
from conll.util import getfnames,punc
import codecs,os.path

def convert(fof, outfof="", outformat="iob2"):
    """ Given a file or folder of text files, this will convert to conll files.
    Assume that the input is always iob2. 

    """
    
    fnames = getfnames(fof)

    for fname in fnames:    
        with codecs.open(fname,"r", "utf8") as f:
            lines = f.readlines()

        fnonly = os.path.basename(fname)

        outname = os.path.join(outfof, fnonly + ".conll")        
        out = codecs.open(outname, "w", "utf8")
        
        i = 1
        last = ""
        for line in lines:
            line = line.strip()

            if len(line.strip()) == 0:
                out.write(line + "\n")
                last = ""
            else:
                sline = line.split("\t")
                if len(sline) == 1:
                    sline.insert(0, "@@@")
                    
                word,tag = sline
                if outformat == "iob1":
                    prefix = tag[0]
                    label = tag[2:]
                    
                    if tag != "O":
                        if last == label and prefix == "B":
                            prefix = "B"
                        else:
                            prefix = "I"
                        tag = "{}-{}".format(prefix, label)
                    last = label

                #out.write("\t".join([tag.upper(), "0", str(i), "x", "x", word, "x", "x", "0\n"]))
                out.write(" ".join([word, "O", "O", tag.upper() + "\n"]))
                i += 1                            

        out.close()

        print("Wrote to: ", outname)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert a 2-column conll file to N-column conll format. # marks comments which will be ignored.")
    
    parser.add_argument("fof", help="file or folder containing text files.")
    parser.add_argument("--outfof", "-o", help="output file or folder", default="")
    parser.add_argument("--outformat", "-f", help="output format", default="iob2")

    args = parser.parse_args()
    
    convert(args.fof, args.outfof, args.outformat)
    
