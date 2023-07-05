"""
This script adds canonical url tags to pages in a Quarto website.
Place the script in the root of the project and run it post render.
"""

from xml.dom.minidom import parse, parseString
from urllib.parse import urlparse
import warnings

site_dir = '_site'
sitemap_file = 'sitemap.xml'

document = parse(site_dir + '/' + sitemap_file)
locs = document.getElementsByTagName('loc')
urls = [l.firstChild.nodeValue for l in locs]

for url in urls:
    
    path = site_dir + urlparse(url).path
    cannonical_tag = f'<link rel="canonical" href="{url}" />'

    # Read in the file
    with open(path, 'r') as file :
      filedata = file.read()

    if filedata.__contains__('<link rel="canonical"'):
        warnings.warn(f'{path} already contains canonical tag. Skipping this file.')
    else:
        print(f'{path} adding canonical tag.')
        # Replace the target string
        filedata = filedata.replace('</head>', cannonical_tag +'\n</head>')

        # Write the file out again
        with open(path, 'w') as file:
          file.write(filedata)