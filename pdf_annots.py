import popplerqt5
import PyQt5
import sys

if (len(sys.argv) >= 1):
    pdf_filename = sys.argv[1]
else:
    quit()

pdf_document = popplerqt5.Poppler.Document.load(pdf_filename)
pdf_document.numPages()

for i in range(pdf_document.numPages()):
    annotations = pdf_document.page(i).annotations()
    for ann in annotations:
        if isinstance(ann, popplerqt5.Poppler.TextAnnotation):
            print(ann.contents())
