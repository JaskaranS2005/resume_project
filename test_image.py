from utils.file_extractor import extract_image_text

img_path = input("Enter Image path: ")

text = extract_image_text(img_path)

print("\n--- EXTRACTED TEXT ---\n")
print(text[:1000])
