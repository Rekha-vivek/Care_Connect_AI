from backend import view_doctors, book_appointment, get_patient

print(view_doctors())

book_appointment("A100", "P001", "D001", "2026-03-26")

print(get_patient("P001"))