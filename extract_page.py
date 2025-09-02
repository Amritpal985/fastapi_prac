from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("sample.pdf")
writer = PdfWriter()

writer.add_page(reader.pages[15])
writer.add_page(reader.pages[16])

with open("extracted_page.pdf", "wb") as output_pdf:
    writer.write(output_pdf)

print("Pages extracted successfully.")