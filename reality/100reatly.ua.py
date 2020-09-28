# coding:utf8
import pprint

import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool
import gspread
import time



def get_html(url):
    r=requests.get(url)
    return r.text

def get_page(html):
    soup=BS(html,'html.parser')
    div=soup.find('div',class_="pager pager-short pager-top")
    li=div.find('li', class_="pager-item hidem")
    max_page=li.find('a').text
    return max_page

def get_content(html):
    soup = BS(html, 'html.parser')
    div_items = soup.find('div', id='realty-search-results')

    items = div_items.find_all('div', class_="object-common-wrapper")
    all_content = []
    for item in items:
        address = item.find('div', class_='object-address')
        region = item.find('div', class_='object-region')
        region_1 = region.find('a').next_sibling
        region=region.find('a').text
        info = item.find('div',class_='object-card-options')
        square = item.find('div', class_='object-square object-info-item').find('div', class_='value')
        square = square.text
        square = square.replace('м²', '')
        price = item.find('div', class_='cost-field').find('span').text
        price = price.replace('грн.', '')
        price = price.replace('грн./месяц', '')
        price = price.replace('/месяц', '')
        price = price.replace('/квартал', '')
        price = price.replace('*', '')
        price = price.replace('грн./квартал', '')
        price = price.replace(' ', '')
        sprice = str(round(float(price)/float(square)))
        sprice = sprice.replace('.',',')
        square = square.replace('.', ',')

        link = item.find('a', class_='image-field__link').get('href')
        if info!=None:
            info=info.find('div',class_='object-profile object-info-item')
            if info!=None:
                info=info.find('a').text

        if region_1.next_sibling != None:
            region_1 = region_1.next_sibling.text
        else:
            region_1 = ''
        if region.count('район')>0 or region.count('(центр)')>0 or region.count('область')>0:
            region_1=region
            region=''

        all_content.append(

            [
                address.find('a').text,
                'https://100realty.ua' + link,
                region_1,
                region,
                info,
                square,
                price,
                sprice

            ]
        )
    return all_content

def make_all(url):
    html = get_html(url)
    content = get_content(html)
    return content

def get_GogleSheets(content):
    name=[['Адрес','Ссылка','Регион','Регион-1','Тип','Площадь в м²','Цена','Цена за м²','Как меняется цена']]

    gs = gspread.service_account(filename='sheets.json')
    sh = gs.open_by_key('1d90kPpKzBVJ9e8UO7k1h2CL2aPE4omSw9HMW1zlNF8c')
    worksheet = sh.sheet1
    values = worksheet.get_all_values()
    new_worksheet=sh.add_worksheet(str(round(time.time())),rows=10,cols=20)

    worksheet.format('A2:F50000', {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})
    for i in range(0,len(content)):
        for j in range(1, len(values)):
            if  content[i][0] == values[j][0] and content[i][1] == values[j][1] and content[i][2] == values[j][2] and content[i][3] == values[j][3] and content[i][5] == values[j][5]:
                if int(content[i][6])>int(values[j][6]):
                    if len(content[i])==8:
                        content[i].append('+++++++Ценна увеличилась, была - '+values[j][6])
                if int(content[i][6])==int(values[j][6]):
                    if len(content[i]) == 8:
                        content[i].append('Ценна не изменилась')
                if int(content[i][6])<int(values[j][6]):
                    if len(content[i]) == 8:
                        content[i].append('-------Ценна уменьшилась, была - '+values[j][6])
    worksheet.update('A1:I1', name)
    new_worksheet.update('A1:I50000',values)
    content = sorted(content, key=lambda x: x[2])
    worksheet.update('A2:I50000', content)





def main():
    url='https://100realty.ua/realty_search/nonlive/sale/prof_5079,16797716,285212683,5081,385875992,33754437,201326922,20536,201326921/f_first/cur_3/kch_2'
    html=get_html(url)
    pages=get_page(html)
    all_link=[]
    all_content=[]
    for i in range(0,int(pages)):
        all_link.append(url+'?page='+str(i))
    with Pool(10) as p:
        all_content.extend(p.map(make_all,all_link))
    new_content=[]
    for i in all_content:
       new_content.extend(i)
    get_GogleSheets(new_content)

if __name__ == '__main__':
    main()