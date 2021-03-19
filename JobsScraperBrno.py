# Stahne "Python Brno" z jobs.cz a ulozi do Xls
# dle predlohy: scrapeindeed - https://github.com/jhnwr/scrapeindeed
# https://www.jobs.cz/prace/brno/?q%5B%5D=python&employer=direct&page=1&locality%5Bradius%5D=10
# page 1 - 4
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
  url = f'https://cz.indeed.com/jobs?q=python&l=brno&start={page}'
  url = f'https://www.jobs.cz/prace/brno/?q%5B%5D=python&employer=direct&page={page}&locality%5Bradius%5D=10'
  r = requests.get(url, headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

def transform(soup):
  divs = soup.find_all('div', class_='standalone search-list__item')
  for item in divs:
    # print(item)
    try:
      title = item.find('a').text.strip()
    except:
      continue
    if (title == ''):
      continue
    try:
      company = item.find('div', class_='search-list__main-info__company').text.strip()
    except:
      company = ''
    try:
      salary = item.find('span', class_='label label--success').text.strip()
    except:
      salary = ''
    href = '' + item.find('a').get("href") + ''
    dtm = item.find('span', class_='label-added').text.strip()
    try:
      datum = item.find('span', {"class": "label-added", "data-label-added-valid-from": True})['data-label-added-valid-from']
    except:
      datum = ''
    # Datum 2021-03-02T01:44:18+01:00 - pryc "T" a  +01:00
    datum = datum.replace("+01:00", "").replace("T", "  ")
    # Job
    job = {
        'Title': title,
        'Company': company,
        'Salary': salary,
        'Link': href,
        'Kdy': dtm,
        'Date Add': datum,
        # 'item': item,
    }
    joblist.append(job)
  return

joblist = []

for i in range(1, 5, 1):
  print(f'Getting page, {i}')
  c = extract(i)
  transform(c)

df = pd.DataFrame(joblist)
df.drop_duplicates(inplace=True)
df.to_excel('zzJobsPython-Brno.xlsx', index=False)
df.to_csv('zzJobsPython-Brno.csv', index=False)

print('OkDone.')
