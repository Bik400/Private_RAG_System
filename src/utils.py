import logging 
import re
from typing import List

from src.constants import LOG_FILE_PATH

def setup_logging() -> None:
    """
    Configure basic logging settings 
    """
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )


def clean_text(text: str) -> str:
    """
    Cleans OCR-extracted text by removing uneccessary newlines, hyphens, and correcting common OCR mistakes

    Args:
        text (str) -> The text to clean 
    
    Returns:
        str -> The cleaned text
    """

    # Remove hyphens at line breaks
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Replace newlines within sentences with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n+", "\n", text)

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    cleaned_text = text.strip()
    logging.info("Text cleaned.")
    return cleaned_text

def chunk_text(text: str, chunk_size: int, overlap: int = 100) -> List[str]:
    """
    Splits text into chunks with a specified overlap

    Args:
        text (str) -> The text to split up
        chunk_size (int) -> The number of tokens in each chunk
        overlap (int) -> The number of tokens to overlap between chunks
    
    Returns:
        List[str] -> A list of text chunks
    """

    # Clean text before chunking
    text = clean_text(text)
    logging.info("Text prepared for chunking.")

    # Tokenize the text into words
    tokens = text.split(" ")

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size                # Calculate end position
        chunk_tokens = tokens[start:end]        # Get tokens for this chunk
        chunk_text = " ".join(chunk_tokens)      # Join the tokens together
        chunks.append(chunk_text)               # Add chunk to result
        start = end - overlap   # Move back 
    
    logging.info(
        f"Split text into {len(chunks)} chunks with chunk size {chunk_size} and overlap {overlap}."
    )

    return chunks

