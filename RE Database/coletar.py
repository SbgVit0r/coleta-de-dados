#%%
import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.residentevildatabase.com/personagens/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=0, i',

}

def get_content(url):
    response = requests.get(url, headers=headers)
    return response

def get_basic_infos(soup):
    div_page = soup.find('div', class_="td-page-content")
    paragrafos = div_page.find_all('p')[1]
    valores = paragrafos.find_all('em')
    data = {}

    for i in valores:
        k, v, *_ = i.text.split(':')
        k = k.strip(' ')
        data[k] = v.strip(' ')
        
    return data

def get_aparicoes(soup):
    items = (soup.find('div', class_='td-page-content').find('h4').find_next().find_all('li'))

    appearences = [i.text for i in items]
    return appearences

def get_personagem_infos(url):
    response = get_content(url)
    if response.status_code != 200:
        print("Deu ruim ae!")
        return {}
    else:
        soup = BeautifulSoup(response.text, features='html.parser')
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
        return data

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_charac = BeautifulSoup(resp.text, features='html.parser')
    anchors = (soup_charac.find('div', class_='td-page-content').find_all('a'))

    links = [i['href'] for i in anchors]
    return links
# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d['link'] = i 
    nome = i.strip('/').split('/')[-1].replace('-',' ').title()
    d['nome'] = nome
    data.append(d)
# %%
df = pd.DataFrame(data)
df

# %%
df[~df['de nascimento'].isna()]
# %%
df.to_parquet('dados_re.parquet', index=False)
# %%
df_novo = pd.read_parquet('../data/dados_re.parquet')
df_novo
# %%
df.to_pickle('../data/dados_re.pkl')

