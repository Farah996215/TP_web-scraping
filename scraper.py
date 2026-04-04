import requests
from bs4 import BeautifulSoup

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    elements = soup.find_all("td", class_="ind", style="margin-left:0px")

    comments = [e.find_next(class_="comment") for e in elements if e.find_next(class_="comment")]

    keywords = {"python": 0, "javascript": 0, "typescript": 0, "go": 0, "c#": 0, "java": 0, "rust": 0 }

    for comment in comments:
        comment_text = comment.get_text().lower()
        words = comment_text.split()

        for word in words:
            if word in keywords:
                keywords[word] += 1

    print(keywords)

if __name__ == "__main__":
    main()