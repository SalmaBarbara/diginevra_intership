import requests
import json
import csv
import pandas as pd
from newspaper import Article
import logging
import os 

def fetch_search_results(api_key, cx, sites, query, date_restrict='d1'):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    links = []

    for site in sites:
        url = f"{base_url}?key={api_key}&cx={cx}&q={query} site:{site}&dateRestrict={date_restrict}&num=10"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()
            print("API Response:")
            print(json.dumps(response_data, indent=4))  # Pretty print the JSON response

            if 'items' in response_data:
                for item in response_data['items']:
                    if 'link' in item:
                        links.append(item['link'])
        
        except requests.exceptions.RequestException as e:
            print(f"Request Exception for site {site}: {e}")

    return links

def fetch_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None, None

def import_start_urls_from_csv(file_path):
    start_urls = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0].startswith('http'):  # Ensure the row is not empty and is a valid URL
                    start_urls.append(row[0])
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
    return start_urls

def save_articles_to_excel(articles, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for i, article in enumerate(articles):
        title = article['title']
        content = article['content']
        file_name = f"Article_{i+1}.xlsx"
        file_path = os.path.join(folder_path, file_name)
        
        df = pd.DataFrame({'Title': [title], 'Content': [content]})
        
        try:
            df.to_excel(file_path, index=False)
            print(f"Saved article '{title}' to file '{file_name}'.")
        except Exception as e:
            logging.error(f"Error saving article '{title}' to file '{file_name}': {e}")