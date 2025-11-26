import fitz

doc = fitz.open("f:/47Docs/test.pdf")
page = doc[0]
blocks = page.get_text("dict")["blocks"]

print(f"Found {len(blocks)} blocks.")
for i, block in enumerate(blocks[:5]): # Check first 5 blocks
    print(f"Block {i} type: {block['type']}")
    if block['type'] == 0:
        for line in block["lines"]:
            print(f"  Line bbox: {line['bbox']}")
            for span in line["spans"]:
                print(f"    Span: '{span['text']}' bbox: {span['bbox']}")
