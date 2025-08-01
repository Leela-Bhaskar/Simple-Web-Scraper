#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys

def scrape_blog_titles(url: str):
    """
    Scrapes all the blog post titles from a given blog URL.

    This function requires the 'requests' and 'beautifulsoup4' libraries.
    You can install them using pip:
    pip install requests beautifulsoup4

    Args:
        url: The full URL of the blog's main page or archive page.
    """
    print(f"--- Scraping titles from: {url} ---")

    try:
        # Step 1: Send an HTTP GET request to the URL
        # The headers help mimic a real browser visit.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Step 2: Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Step 3: Find the HTML elements containing the blog post titles.
        # This is the part you will most likely need to customize for each site.
        # Use your browser's "Inspect" tool to find the right tag and attributes.
        # UPDATED: As of late 2024/early 2025, titles are in <a> tags with a specific `data-event-click` attribute.
        # We find all `a` tags and then filter them based on the attribute containing 'post-title'.
        
        # Find all link elements first
        all_links = soup.find_all('a')
        title_elements = []

        # Filter links to find the ones that are likely article titles
        for link in all_links:
            # This is a more robust way to check for a partial match in an attribute
            if link.has_attr('data-event-click') and 'post-title' in link['data-event-click']:
                # The actual title text is usually within an h3 or h2 inside the link
                title_container = link.find(['h2', 'h3'])
                if title_container:
                    title_elements.append(title_container)


        if not title_elements:
            print("\nCould not find any post titles using the specified selector.")
            print("The website's HTML structure may have changed, or the selector is incorrect.")
            print("Please inspect the blog's HTML and adjust the script.")
            return

        # Step 4: Extract the text from the found elements and print them.
        print("\n--- Found Titles ---")
        for index, title_element in enumerate(title_elements):
            # .get_text(strip=True) cleans up whitespace
            title_text = title_element.get_text(strip=True)
            print(f"{index + 1}: {title_text}")
        print("--------------------")


    except requests.exceptions.RequestException as e:
        print(f"\n--- ERROR ---", file=sys.stderr)
        print(f"An error occurred while trying to fetch the URL: {e}", file=sys.stderr)
        print("Please check the URL and your internet connection.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main function to run the scraper.
    """
    # --- IMPORTANT ---
    # This URL is for Wired's "most recent" page. The scraper is now
    # tailored to this specific page's HTML structure.
    target_url = "https://www.wired.com/most-recent/"

    # You could also get the URL from the command line like this:
    # if len(sys.argv) > 1:
    #     target_url = sys.argv[1]
    # else:
    #     print("Usage: python scraper.py <URL>", file=sys.stderr)
    #     sys.exit(1)

    scrape_blog_titles(target_url)


if __name__ == "__main__":
    main()
