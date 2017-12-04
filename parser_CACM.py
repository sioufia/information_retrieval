"""File that's gonna parse the CACM collection into different files. One file correspond to one document"""

def append_doc(doc_number,content):
    filename="CACM_traite/CACM_" + doc_number +'.txt'
    with open(filename, 'a') as f:
        f.write(content)
    f.close()

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

with open("CACM/cacm.all", "r") as f:
    doc_number = '0'
    doc_section = '0'
    for line in f:
        if check_section_line(line):
            doc_section = str(line[:2])
            if check_start_document(line):
                doc_number = str(line[3:])
                filename="CACM_traite/CACM_" + doc_number +'.txt'
                with open(filename, 'a') as f2:
                    f2.write(line)
                f2.close() 
            if doc_section in [".T",".W",".K"]:
                append_doc(doc_number,line)
        elif doc_section in [".I",".T",".W",".K"]:
            append_doc(doc_number,line)

