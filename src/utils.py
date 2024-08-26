import re

def extract_cookie(text):
    """Extracts a Roblox security cookie or any other cookie from text enclosed in triple backticks."""
    print(f"Extracting cookie from text: {text}")  # Debugging
    match = re.search(r'```([A-Fa-f0-9]{100,})```', text)
    if match:
        print(f"Cookie extracted: {match.group(1)}")  # Debugging
        return match.group(1)
    print("No cookie found in the text.")  # Debugging
    return None
