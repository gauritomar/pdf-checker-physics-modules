from bs4 import BeautifulSoup
import os
import pandas as pd

def extract_tables_from_html(html_folder):
    html_files = [os.path.join(html_folder, file) for file in os.listdir(html_folder) if file.endswith('.html')]
    dfs = []

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table')
            if table:
                df = pd.read_html(str(table))[0]
                dfs.append(df)
    
    return dfs

# Example usage:
html_folder = 'html_output'
tables = extract_tables_from_html(html_folder)

# Save tables as CSV
output_folder = 'csv_output'
os.makedirs(output_folder, exist_ok=True)

for idx, table in enumerate(tables):
    table.to_csv(os.path.join(output_folder, f"table_{idx + 1}.csv"), index=False)
