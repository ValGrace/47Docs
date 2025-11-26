import fitz

doc = fitz.open()
page = doc.new_page()

# Define table data
data = [
    ["ID", "Description", "Cost", "Status"],
    ["001", "Item A", "$10.00", "Active"],
    ["002", "Item B with long description", "$20.50", "Inactive"],
    ["003", "Item C", "$5.00", "Pending"],
    ["004", "Item D", "$100.00", "Active"]
]

y = 50
row_height = 30
col_widths = [50, 200, 80, 80]
x_starts = [50, 100, 300, 380]

for row in data:
    for i, text in enumerate(row):
        p = fitz.Point(x_starts[i], y)
        page.insert_text(p, text, fontsize=12)
    y += row_height

doc.save("f:/47Docs/table_test.pdf")
print("Created table_test.pdf")
