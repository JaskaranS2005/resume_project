from utils.file_extractor import extract_pdf_text

pdf_path = input("Enter PDF path: ")

text = extract_pdf_text(pdf_path)

print("\n--- EXTRACTED TEXT ---\n")
print(text)  # print first 1000 chars
