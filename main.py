import os
import shutil 
import datetime
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from hashlib import sha1

def file_delete():
    # to-do
    pass

def etc():
    print("no")

if not os.path.isdir("backups"):
    os.mkdir("backups")


# folder_created = None

# try:
#     os.mkdir("test")
# except OSError: # only if OSError is raised
#     print("folder created")
# else:  # only if no errors
#     folder_created = True
# finally:  # no matter what, it will run
#     pass

ARTICLE_FOLDER = "articles"
BACKUP_FOLDER = "backups"

folder_filenames = os.listdir(ARTICLE_FOLDER)

file_hashes = {}
all_filenames = []

for filename in folder_filenames:
    if not filename.endswith("pdf"):
        continue

    # print("Current file", filename)
    contents = open("articles/{}".format(filename), "rb")
    file_contents = contents.read()
    file_hash = sha1(file_contents).hexdigest()

    if file_hash not in file_hashes:
        file_hashes[file_hash] = []

    all_filenames.append(filename)
    file_hashes[file_hash].append(filename)


# for hash in file_hashes:   # same thing as alternative used below
#   file_list = file_hashes[hash]

for hash, file_list in file_hashes.items():
    if len(file_list) == 1:
        continue

    all_pdfs_but_one = file_list[1:]
    for pdf_filename in all_pdfs_but_one:
        all_filenames.remove(pdf_filename)
        shutil.move(f"{ARTICLE_FOLDER}/{pdf_filename}", f"{BACKUP_FOLDER}/{pdf_filename}")

for pdf_file in all_filenames:
    contents = open(f"{ARTICLE_FOLDER}/{pdf_file}", "rb")
    print("Reading", pdf_file)    
    parser = PDFParser(contents)
    doc = PDFDocument(parser)
    metadata = doc.info[0]
    date = metadata["CreationDate"]
    date = date.split(b"+")[0]
    date_obj = datetime.datetime.strptime(date.decode(), "D:%Y%m%d%H%M%S")