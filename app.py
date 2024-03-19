#%%

import requests
from bs4 import BeautifulSoup
import urllib
import os

#%%

def import_documents(url):
    # Create the directory to store the documents found
    if not os.path.exists('Documents'):
        os.makedirs('Documents')

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

    # Download each PDF file
    for link in pdf_links:
        pdf_url = link['href']
        pdf_filename = pdf_url.split('/')[-1]
        pdf_path = os.path.join('Documents', pdf_filename)
        pdf_url = urllib.parse.urljoin(url, pdf_url.replace(' ', '%20'))
        print("Downloading:", pdf_filename)
        with open(pdf_path, 'wb') as f:
            f.write(requests.get(pdf_url).content)

def main():
    # Set URLs of WCA's documents page and Regulations/Guidelines
    urls = [
        'https://www.worldcubeassociation.org/documents',
        'https://www.worldcubeassociation.org/regulations/',
        'https://www.worldcubeassociation.org/regulations/guidelines.html'
    ]

    for url in urls:
        import_documents(url)

    print('\n 🎉 All Documents have been downloaded! 🎉')


if __name__ == '__main__':
    main()



# %%




'''
TODO:

- Add Regulations, Guidelines, Crash Course?

'''