import requests
from bs4 import BeautifulSoup

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # Fix element extraction (indent = 0)
    elements = soup.find_all("td", class_="ind", style="margin-left:0px")

    # Extract comments with None check
    comments = [e.find_next(class_="comment") for e in elements if e.find_next(class_="comment")]

    # Map of technologies
    keywords = {
        "python": 0,
        "javascript": 0,
        "typescript": 0,
        "go": 0,
        "c#": 0,
        "java": 0,
        "rust": 0
    }

    # Process comments
    for comment in comments:
        comment_text = comment.get_text().lower()

        # Split into words
        words = comment_text.split(" ")

        # Clean + convert to set (unique words)
        words = {w.strip(".,/:;!@") for w in words}

        # Count once per comment
        for k in keywords:
            if k in words:
                keywords[k] += 1

    # Final result
    print(keywords)

if __name__ == "__main__":
    main()