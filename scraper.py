import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    
    # Send request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Get top-level comment elements (indent = 0)
    elements = soup.find_all("td", class_="ind", style="margin-left:0px")
    
    # Extract comments safely (ignore None values)
    comments = [e.find_next(class_="comment") for e in elements if e.find_next(class_="comment")]

    # Dictionary to count programming languages
    keywords = {
        "python": 20,
        "javascript": 30,
        "typescript": 60,
        "go": 10,
        "c#": 10,
        "java": 15,
        "rust": 0
    }

    # Loop through each comment
    for comment in comments:
        # Convert text to lowercase
        comment_text = comment.get_text().lower()
        
        # Split text into words
        words = comment_text.split(" ")
        
        # Clean words and keep only unique ones
        words = {w.strip(".,/:;!@") for w in words}

        # Check if a keyword exists in the comment
        for k in keywords:
            if k in words:
                keywords[k] += 1

    # Print results
    print(keywords)

    # Create a bar chart
    plt.bar(keywords.keys(), keywords.values())
    
    # Add labels and title
    plt.xlabel("Language")
    plt.ylabel("# of Mentions")
    plt.title("Programming Language Mentions in Comments")
    
    # Show the chart
    plt.show()

if __name__ == "__main__":
    main()