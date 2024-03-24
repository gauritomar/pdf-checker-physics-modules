import os
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Function to read JSON files from a folder
def read_json_files(folder):
    json_data = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename)) as file:
                json_data.append(json.load(file))
    return json_data

# Folder containing JSON files
folder_path = "json_output"

# Read JSON files from the folder
json_data = read_json_files(folder_path)

# Create PDF
pdf_filename = "json_data_reportlab.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
table_data = [["Correct", "Incorrect", "Type"]]

# Populate table data
for data in json_data:
    table_data.append([data["correct"], data["incorrect"], data["type"]])

# Create table
table = Table(table_data)

# Add style to table
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

table.setStyle(style)

# Add table to the PDF
doc.build([table])

print(f"PDF generated: {pdf_filename}")
