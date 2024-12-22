from bs4 import BeautifulSoup
import requests
import argparse
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_headlines(url):
    """
    Fetch headlines from the given URL.
    
    :param url: Website URL to scrape.
    :return: List of headline strings.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    # Extract all <h2> tags (or adjust the selector based on the site's structure)
    headlines = soup.find_all('h2')
    # Filter out empty or irrelevant headlines
    return [headline.get_text(strip=True) for headline in headlines if headline.get_text(strip=True)]

def save_to_file(headlines, filename):
    """
    Save the list of headlines to a text file.
    
    :param headlines: List of headlines to save.
    :param filename: Name of the file to save to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Latest BBC News Headlines:\n\n")
            for i, headline in enumerate(headlines, start=1):
                file.write(f"{i}. {headline}\n")
        logging.info(f"Headlines successfully saved to {filename}")
    except Exception as e:
        logging.error(f"An error occurred while saving to file: {e}")

def display_headlines(headlines):
    """
    Display headlines in the terminal.
    
    :param headlines: List of headlines to display.
    """
    print("\nLatest BBC News Headlines:\n")
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape and save BBC News headlines.")
    parser.add_argument(
        "-n", "--num_headlines", type=int, default=10,
        help="Number of headlines to fetch (default: 10)."
    )
    parser.add_argument(
        "-f", "--filename", type=str,
        default=f"bbc_headlines_{datetime.now().strftime('%Y%m%d')}.txt",
        help="File to save headlines (default: bbc_headlines_<date>.txt)."
    )
    args = parser.parse_args()

    # Step 1: Define the target URL
    website_url = "https://www.bbc.com/news"
    logging.info("Fetching headlines from BBC News...")

    # Step 2: Fetch headlines
    headlines = fetch_headlines(website_url)

    # Step 3: Handle results
    if headlines:
        # Limit the number of headlines based on user input
        limited_headlines = headlines[:args.num_headlines]
        display_headlines(limited_headlines)
        save_to_file(limited_headlines, args.filename)
    else:
        logging.warning("No headlines found or an error occurred.")
