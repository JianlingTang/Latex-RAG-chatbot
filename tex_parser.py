import re
import json
from typing import List, Dict
import glob

def clean_latex_text(text: str) -> str:
    # Remove LaTeX commands like \label{}, \cite{}, \ref{}, etc.
    text = re.sub(r'\\(label|cite|ref|eqref)\{.*?\}', '', text)
    # Remove inline formatting like \textbf{}, \emph{}, etc.
    text = re.sub(r'\\\w+\{.*?\}', '', text)
    # Remove any remaining backslash commands
    text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
    # Clean up whitespace
    return re.sub(r'\s+', ' ', text).strip()

def extract_chunks(tex_text: str) -> List[Dict[str, str]]:
    """
    Parses LaTeX content and extracts sections, text blocks, and equations.
    Returns a list of dictionaries with keys: section, text, equation
    """
    sections = re.split(r'\\section\*?\{(.+?)\}', tex_text)
    chunks = []

    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        content = sections[i + 1]

        # Extract equations from equation and align environments
        eq_pattern = r'\\begin\{(?:equation|align)\*?\}(.*?)\\end\{(?:equation|align)\*?\}'
        equations = re.findall(eq_pattern, content, re.DOTALL)
        text_blocks = re.split(eq_pattern, content, flags=re.DOTALL)

        eq_idx = 0
        for idx, text in enumerate(text_blocks):
            if idx % 2 == 0:
                cleaned_text = clean_latex_text(text)
                if cleaned_text:
                    chunks.append({
                        "section": section_title,
                        "text": cleaned_text,
                        "equation": ""
                    })
            else:
                clean_eq = clean_latex_text(equations[eq_idx])
                if clean_eq:
                    chunks.append({
                        "section": section_title,
                        "text": "",
                        "equation": clean_eq
                    })
                eq_idx += 1

    return chunks

def save_chunks_to_json(chunks: List[Dict[str, str]], output_path: str = "chunks.json") -> None:
    with open(output_path, 'w') as f:
        json.dump(chunks, f, indent=2)

if __name__ == "__main__":
    tex_files = glob.glob("*.tex")
    for texfile in tex_files:
        with open(texfile, "r") as f:
            tex_content = f.read()
        parsed_chunks = extract_chunks(tex_content)
        save_chunks_to_json(parsed_chunks)
