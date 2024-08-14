import os
from datetime import datetime
from utils.util import fetch_search_results, fetch_article_content, save_articles_to_excel, import_start_urls_from_csv

def main():
    api_key = 'AIzaSyDamCbE1soFmLe9OIbDvll_uEo8LW6N3Yw'
    cx = '638cb048dc6314640'
    input_file_path = 'scraping_sources/sources.csv'   # Corrected path to the CSV file
    output_folder_path = 'output'

    # Import domains from the CSV file
    domains = import_start_urls_from_csv(input_file_path)
    if not domains:
        print("No valid domains found in the CSV file.")
        return

    start_time = datetime.now()
    print(f"Script execution started at: {start_time}")

    # Fetch search results
    query = 'latest tech news'
    links = fetch_search_results(api_key, cx, domains, query)
    print(f"Fetched {len(links)} article links.")

    # Fetch full article content
    articles_with_content = []
    for link in links:
        title, content = fetch_article_content(link)
        if content:
            articles_with_content.append({'link': link, 'title': title, 'content': content})

    # Save articles to separate Excel files in a folder
    save_articles_to_excel(articles_with_content, output_folder_path)

    end_time = datetime.now()
    print(f"Script execution finished at: {end_time}")
    print(f"Total execution time: {end_time - start_time}")

if __name__ == '__main__':
    main()
