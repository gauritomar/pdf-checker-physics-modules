import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

def create_pdf_from_csv(csv_folder, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = []

    csv_files = [os.path.join(csv_folder, file) for file in os.listdir(csv_folder) if file.endswith('.csv')]

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        data = [df.columns.tolist()] + df.values.tolist()

        # Calculate maximum available width for the table
        max_table_width = letter[0] - doc.leftMargin - doc.rightMargin

        # Calculate column widths for the table
        num_cols = len(data[0])
        col_width = max_table_width / num_cols
        col_widths = [col_width] * num_cols

        # Create table
        table = Table(data, colWidths=col_widths)

        # Add style to table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)

        # Calculate row heights based on content
        row_heights = [max([len(str(row[i])) for row in data]) * 12 for i in range(num_cols)]
        table._argH[1:] = row_heights

        elements.append(table)
        elements.append(Spacer(1, 12))

    doc.build(elements)

# Example usage:
csv_folder = 'csv_output'
output_pdf = 'output.pdf'
create_pdf_from_csv(csv_folder, output_pdf)
