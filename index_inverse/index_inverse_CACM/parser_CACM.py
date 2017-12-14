"""File that's gonna parse the CACM collection into a dictionnary. One file correspond to one document"""

def check_start_document(line):
    if line[:2] == ".I":
        return True
    else:
        return False

def check_section_line(line):
    D = [".B",".A",".N",".X",".C",".I",".T",".W",".K"]
    if line[:2] in D:
        return True
    else:
        return False

def parser():
    with open("././CACM/cacm.all", "r") as f:
        doc_number = '0'
        doc_section = '0'
        D = {}
        for line in f:
            if check_section_line(line):
                doc_section = str(line[:2])
                if check_start_document(line):
                    doc_number = (str(line[3:]))[:-1]
                    D[doc_number] = "" 
            elif doc_section in [".I",".T",".W",".K"]:
                D[doc_number] += " " + line[:-1]
        return D

