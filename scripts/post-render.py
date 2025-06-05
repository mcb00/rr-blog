"""
This script performs post processing on a rendered Quarto site by doing
  - adding canonical url tags to pages
  - stripping index.html from urls in the sitemap
"""

from xml.dom.minidom import parse
from urllib.parse import urlparse
import warnings
import os

SITE_DIR = '_site'
SITEMAP_FILE = os.path.join(SITE_DIR, 'sitemap.xml')

def add_canonical_tags(urls: list):
    """
    Adds canonical URL tags to HTML pages based on a list of URLs.
    Handles cases where sitemap URLs might refer to directories or already contain index.html.
    """
    print('\nAdding canonical url tags to pages...')
    for url in urls:
        parsed_path = urlparse(url).path

        # Determine the full file path.
        # If the sitemap URL points to a directory (e.g., /about/),
        # assume the corresponding file is index.html within that directory.
        if parsed_path == '/' or parsed_path == '':
            # This is the root of the site, which is a directory. Skip as a file.
            continue
        elif parsed_path.endswith('/'):
            file_path = os.path.join(SITE_DIR, parsed_path, 'index.html')
        else:
            file_path = os.path.join(SITE_DIR, parsed_path)

        # Check if the constructed path is actually a file
        if not os.path.isfile(file_path):
            warnings.warn(f'Skipping {file_path} as it is not a file or does not exist.')
            continue

        print(f'Processing: {file_path}')

        # Prepare the canonical URL (strip index.html if present in the original URL)
        canonical_url = url
        if canonical_url.endswith('index.html'):
            canonical_url = canonical_url[:-10]
        canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'

        try:
            # Read in the file
            with open(file_path, 'r', encoding='utf-8') as file:
                filedata = file.read()

            if '<link rel="canonical"' not in filedata:
                print(f'Adding canonical tag to file: {file_path}')
                # Replace the target string
                filedata = filedata.replace('</head>', canonical_tag + '\n</head>')
                # Write the file out again
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(filedata)
            else:
                warnings.warn(f'{file_path} already contains canonical tag. Skipping this file.')
        except Exception as e:
            warnings.warn(f"Error processing {file_path}: {e}")

def strip_index_html_from_sitemap(sitemap_path: str):
    """
    Removes 'index.html' from URLs within the sitemap.xml file.
    """
    print('\nStripping index.html from urls in the sitemap...')
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as file:
            filedata = file.read()

        # Only replace if 'index.html' is present to avoid unnecessary file writes
        if 'index.html' in filedata:
            filedata = filedata.replace('index.html', '')
            with open(sitemap_path, 'w', encoding='utf-8') as file:
                file.write(filedata)
        else:
            print(f"'{sitemap_path}' already stripped of 'index.html'.")
    except Exception as e:
        warnings.warn(f"Error stripping index.html from sitemap {sitemap_path}: {e}")

if __name__ == "__main__":
    if not os.path.exists(SITEMAP_FILE):
        warnings.warn(f"Sitemap file not found at {SITEMAP_FILE}. Skipping post-render operations.")
    else:
        try:
            document = parse(SITEMAP_FILE)
            locs = document.getElementsByTagName('loc')
            urls = [l.firstChild.nodeValue for l in locs]

            add_canonical_tags(urls)
            strip_index_html_from_sitemap(SITEMAP_FILE)

        except Exception as e:
            print(f"An error occurred during post-render processing: {e}")