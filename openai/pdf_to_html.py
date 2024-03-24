from openai import OpenAI
import os
import pdfplumber
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Prompt for text analysis
prompt = '''
    Please analyze the text below, aiming to correct any grammatical errors and factual inaccuracies. Your task is to return a json containing the list of mistakes and errors. The first key should be "incorrect" containing the mistake in the original line, the second key being "type" which contains the type of mistake, and the third key being "corrected" which has the corrected fixed line. Thank you for improving this learning resource for physics students.
'''

def extract_html(text, output_path):
    """
    Extract HTML from the text using OpenAI's GPT-3.
    """
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Here is the page of text:{text}"}
        ]
    )

    html = completion.choices[0].message.content
    # Write HTML to file
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)
    print(f"HTML saved to {output_path}")

def read_pdf(file_path, start_page=5, end_page=10, output_folder="html_output"):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with pdfplumber.open(file_path) as pdf:
        for page_number in range(start_page, end_page + 1):
            page = pdf.pages[page_number - 1]  # Adjust for 0-indexing
            text = page.extract_text()
            output_path = os.path.join(output_folder, f"page_{page_number}.html")
            extract_html(text, output_path)

if __name__ == "__main__":
    pdf_path = "./Physics Module -1 Medical.pdf" 
    if os.path.exists(pdf_path):
        read_pdf(pdf_path)
    else:
        print("Error: PDF file not found.")
