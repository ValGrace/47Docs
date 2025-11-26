import fitz
import sys

print(f"PyMuPDF Version: {fitz.__version__}")

try:
    doc = fitz.open("f:/47Docs/test.pdf")
    page = doc[0]
    
    if hasattr(page, "find_tables"):
        print("find_tables is available.")
        tables = page.find_tables()
        print(f"Found {len(tables.tables)} tables.")
        for i, table in enumerate(tables):
            print(f"Table {i}: {len(table.rows)} rows, {len(table.header.cells)} header cells")
            # Print first row cells to see if they match columns
            if table.rows:
                print("Row 1 cells:", [cell for cell in table.rows[0].cells])
    else:
        print("find_tables is NOT available.")
        
except Exception as e:
    print(f"Error: {e}")
