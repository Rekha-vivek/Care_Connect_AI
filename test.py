from ocr import extract_text_from_image
text = extract_text_from_image("medical_report.png")

print("===== OCR OUTPUT =====")
print(text)