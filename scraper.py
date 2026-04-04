import requests
from bs4 import BeautifulSoup

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # find all elements with class="ind" and indent level = 0
    elements = soup.find_all("td", class_="ind", style="margin-left:0px")

    # for each of this elements, find the next element
    comments = [e.find_next(class_="comment") for e in elements]

    print(f"Comments: {len(comments)}")

    # show each comment (job post)
    for comment in comments:
        print(comment.text)
        print("-" * 80)

if __name__ == "__main__":
    main()