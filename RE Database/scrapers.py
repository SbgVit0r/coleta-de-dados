#%%
import requests
from bs4 import BeautifulSoup

def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.residentevildatabase.com/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
    }

    response = requests.get(url, headers=headers)
    return response
# %%
url = 'https://www.residentevildatabase.com/resident-evil-3-1999-ja-tem-data-para-retornar-ao-pc-via-gog/'

response = get_content(url)

if response.status_code != 200:
    print("Deu ruim aí!")
# %%
soup = BeautifulSoup(response.text, features="html.parser")
soup

def get_basic_infos(soup):
    div_page = soup.find('div', class_="td-post-content")
    paragrafo = div_page.find_all('p')[1]
    links = paragrafo.find_all('a')

# %%
data = {}

for i in links:
    k, v = i.text.split('()')
    data[k] = v

data
# %%
