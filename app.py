import os
import pdfplumber
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def read_pdf(file_path, start_page=5, end_page=10):
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page_number in range(start_page, end_page + 1):
            page = pdf.pages[page_number - 1]  # Adjust for 0-indexing
            text.append(page.extract_text())
    return text

def check_grammar_and_facts(text):
    """
    Check grammar and facts using Google Gemini.
    """
    model = genai.GenerativeModel('gemini-pro')
    prompt = '''
    Please analyze the text below, aiming to correct any grammatical errors and factual inaccuracies. Your task is to provide the original line with the mistake indicated within <> followed by its revised version, enhancing clarity and accuracy for physics education. Thank you for improving this learning resource for physics students.

    '''

    mistakes = []
    for i, page in enumerate(text):
        try:
            response = model.generate_content(prompt + page, stream=True)
            response.resolve()  # Resolve the response before accessing attributes
            mistakes.append(response.text)

            # Save mistakes to a text file
            with open(f"page_{i}.txt", "w") as file:
                file.write(response.text)
        except Exception as e:
            print(f"Error processing page {i + 1}: {e}")
            mistakes.append("Error occurred while processing this page.")

    return mistakes



def main(pdf_file_path):
    """
    Main function to read PDF, check grammar and facts, and return mistakes.
    """
    text = read_pdf(pdf_file_path)
    mistakes = check_grammar_and_facts(text)
    for i, mistake in enumerate(mistakes):
        print(f"Mistakes in page {i + 1}: {mistake}")

if __name__ == "__main__":
    pdf_path = "./Physics Module -1 Medical.pdf" 
    if os.path.exists(pdf_path):
        main(pdf_path)
    else:
        print("Error: PDF file not found.")
