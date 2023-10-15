"""
This script performs post processing on a rendered Quarto site by doing
  - adding canonical url tags to pages
  - stripping index.html from urls in the sitemap
  - stripping index.html from urls in redirects
"""

from xml.dom.minidom import parse, parseString
from urllib.parse import urlparse
import warnings
import os 

site_dir = '_site'
sitemap_file = '_site/sitemap.xml'

document = parse(sitemap_file)
locs = document.getElementsByTagName('loc')
urls = [l.firstChild.nodeValue for l in locs]

print()
print('Adding canonical url tags to pages...')
for url in urls:
    
    path = site_dir + urlparse(url).path
    # strip index.html from canonical url
    if url[-10:] == 'index.html':
       url = url[:-10]
      #  print(f'{url}')
    canonical_tag = f'<link rel="canonical" href="{url}" />'

    # Read in the file
    with open(path, 'r') as file :
      filedata = file.read()

    if not filedata.__contains__('<link rel="canonical"'):
        print(f'Adding canonical tag to file: {path}')
        # Replace the target string
        filedata = filedata.replace('</head>', canonical_tag +'\n</head>')
        # Write the file out again
        with open(path, 'w') as file:
          file.write(filedata)
    else:
        warnings.warn(f'{path} already contains canonical tag. Skipping this file.')

# Remove index.html from urls in the sitemap
print()
print('Stripping index.html from urls in the sitemap...')
with open(sitemap_file, 'r') as file :
  filedata = file.read()
filedata = filedata.replace('index.html', '')
with open(sitemap_file, 'w') as file:
  file.write(filedata)


# Remove index.html from redirects
print()
print('Removing index.html from redirect target urls...')
list_subfolders_with_paths = [f.path for f in os.scandir(site_dir) if f.is_dir()]
for subfolder_with_path in list_subfolders_with_paths:
  if 'index.html' in os.listdir(subfolder_with_path):
    # print(f"Reading: {os.path.join(subfolder_with_path, 'index.html')}")
    with open(os.path.join(subfolder_with_path, 'index.html'), 'r') as file :
      filedata = file.read()
    if '<title>Redirect</title>' in filedata:
       filedata = filedata.replace('index.html', '')
       print(f'Editing target url in redirect at {os.path.join(subfolder_with_path, "index.html")}')
       with open(os.path.join(subfolder_with_path, 'index.html'), 'w') as file :
          file.write(filedata)
      

# Add umami tracking script to redirect pages
print()
print('Adding umami tracking script to redirect URLs...')
with open(os.path.join('includes', 'umami.html'), 'r') as file :
  umami_text = file.read()
list_subfolders_with_paths = [f.path for f in os.scandir(site_dir) if f.is_dir()]
for subfolder_with_path in list_subfolders_with_paths:
  if 'index.html' in os.listdir(subfolder_with_path):
    # print(f"Reading: {os.path.join(subfolder_with_path, 'index.html')}")
    with open(os.path.join(subfolder_with_path, 'index.html'), 'r') as file :
      filedata = file.read()
    if '<title>Redirect</title>' in filedata:
       filedata = filedata.replace('</head>', umami_text + '\n</head>')
       print(f'Adding umami script to {os.path.join(subfolder_with_path, "index.html")}')
       with open(os.path.join(subfolder_with_path, 'index.html'), 'w') as file :
          file.write(filedata)
      