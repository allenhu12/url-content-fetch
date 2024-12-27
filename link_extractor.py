from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
from pathlib import Path
import logging
import requests
import time

def setup_logging():
    """Configure logging for the script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def read_html_file(file_path):
    """
    Read HTML file and return its content
    
    Args:
        file_path (str): Path to the HTML file
        
    Returns:
        str: HTML content
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logging.error(f"Error reading file: {e}")
        raise

def extract_links(html_content, base_url=''):
    """
    Extract all links from HTML content
    
    Args:
        html_content (str): HTML content to parse
        base_url (str): Base URL for converting relative URLs to absolute
        
    Returns:
        set: Set of unique URLs found in the HTML
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href:
                # Handle relative URLs if base_url is provided
                if base_url and not href.startswith(('http://', 'https://')):
                    href = urljoin(base_url, href)
                links.add(href)
                
        return links
    except Exception as e:
        logging.error(f"Error parsing HTML: {e}")
        raise

def save_links(links, output_file):
    """
    Save extracted links to a text file
    
    Args:
        links (set): Set of links to save
        output_file (str): Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for link in sorted(links):
                file.write(f"{link}\n")
        logging.info(f"Successfully saved {len(links)} links to {output_file}")
    except IOError as e:
        logging.error(f"Error writing to output file: {e}")
        raise

def fetch_url_content(url, api_key):
    """
    Fetch content from URL using the Jina API
    
    Args:
        url (str): URL to fetch
        api_key (str): Jina API key
        
    Returns:
        str: Response content or error message
    """
    try:
        jina_url = f'https://r.jina.ai/{url}'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return f"Error fetching URL: {str(e)}"

def process_links_file(input_file, output_file, api_key):
    """
    Process links from input file and save responses to output file
    
    Args:
        input_file (str): Path to file containing URLs
        output_file (str): Path to save fetched content
        api_key (str): Jina API key
    """
    try:
        # Read URLs from input file
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        # Process each URL and save responses
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, url in enumerate(urls, 1):
                logging.info(f"Processing URL {i}/{len(urls)}: {url}")
                
                # Add divider
                divider = f"\n{'='*80}\nURL {i}: {url}\n{'='*80}\n"
                f.write(divider)
                
                # Fetch and save content
                content = fetch_url_content(url, api_key)
                f.write(content + "\n")
                
                # Add small delay to avoid overwhelming the API
                time.sleep(1)
                
        logging.info(f"Successfully processed {len(urls)} URLs and saved to {output_file}")
    except Exception as e:
        logging.error(f"Error processing links: {e}")
        raise

def main():
    """Main function to run the link extractor"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract links from HTML file and fetch their content')
    parser.add_argument('input_file', help='Path to input HTML file')
    parser.add_argument('output_file', help='Path to output text file for links')
    parser.add_argument('--base-url', help='Base URL for relative links', default='')
    parser.add_argument('--api-key', help='Jina API key', required=True)
    parser.add_argument('--fetch-content', help='Fetch content for extracted links', action='store_true')
    
    args = parser.parse_args()
    
    setup_logging()
    
    try:
        # Read HTML file
        html_content = read_html_file(args.input_file)
        
        # Extract links
        links = extract_links(html_content, args.base_url)
        
        # Save links to output file
        save_links(links, args.output_file)
        
        # If fetch-content flag is set, process the links
        if args.fetch_content:
            fetched_content_file = 'fetched_content.txt'
            process_links_file(args.output_file, fetched_content_file, args.api_key)
        
    except Exception as e:
        logging.error(f"Script execution failed: {e}")
        exit(1)

if __name__ == '__main__':
    main()