import re

def normalize_text(text: str) -> str:
    """Normalize text by stripping whitespace."""
    text = text.strip()
  #  print(f"After strip: '{text}'")
    text = re.sub(r"[ \t]+", " ", text)
  #  print(f"After collapsing spaces: '{text}'")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
   # print(f"After collapsing newlines: '{text}'")
    return text



# def main():
#     sample_text = """   He  llo, World! 

#         This is a sample text."""
#     normalized = normalize_text(sample_text)
#     print(f"Original: '{sample_text}'")
#     print(f"Normalized: '{normalized}'")
# if __name__ == "__main__":
#         main()