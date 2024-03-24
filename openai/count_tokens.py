def count_tokens(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        # Split the text into tokens (words) using whitespace as delimiter
        tokens = text.split()
        num_tokens = len(tokens)
        return num_tokens

if __name__ == "__main__":
    file_path = "output.txt"  # Replace with the path to your text file
    num_tokens = count_tokens(file_path)
    print(f"Number of tokens in the file: {num_tokens}")
