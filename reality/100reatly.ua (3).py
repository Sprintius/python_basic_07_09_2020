# coding:utf8
import pprint

import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool
import gspread
import datetime



def get_html(url):
    r=requests.get(url)
    return r.text

def get_page(html):
    soup=BS(html,'html.parser')
    div=soup.find('div',class_="pager pager-short pager-top")
    li=div.find('li', class_="pager-item hidem")
    max_page=li.find('a').text
    return max_page

# def get_usa(url):
#     html=get_html(url)
#
#     soup=BS(html,'html.parser')
#     div=soup.find('div',class_='bank-currency__info-val').text
#     div=div.replace('1 USD = ','')
#     div=div.replace(' UAH ','')
#     div=div.replace(',','.')
#     return div




def get_content(html):
    #usa_price = get_usa('https://www.sravni.ru/valjuty/konverter-dollara-k-grivne/')

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
        #usa=str(round(float(price)/float(usa_price)))
        usa=item.find('div',class_='usd-price-value').text
        i=usa.find('$')
        usa=usa[0:i]
        usa=usa.replace(' ','')
        sprice = sprice.replace('.',',')
        square = square.replace('.', ',')

        link = item.find('a', class_='image-field__link').get('href')


        info=item.find('div',class_='object-card-options')

        if info!=None:
            info=info.find('div',class_='object-profile object-info-item')
            if info!=None:
                info=info.find('a').text

            else:
                info='Не известно'
        else:
            info='Не известно'


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
                int(price),
                int(sprice),
                int(usa)

            ]
        )
    return all_content

def make_all(url):
    html = get_html(url)
    content = get_content(html)
    return content

def get_GogleSheets(content):

    name=[['Адрес','Ссылка','Регион','Регион-1','Тип','Площадь в м²','Цена','Цена за м²','Цена в долларах','Как меняется цена']]

    gs = gspread.service_account(filename='sheets.json')
    sh = gs.open_by_key('1H8pa2oKL7XGWY1QTBRy14Vd1m9wpI_fio_LHjDMxppE')
    worksheet = sh.get_worksheet(-1)
    values = worksheet.get_all_values()
    new_worksheet=sh.add_worksheet(str(datetime.datetime.today()),rows=10,cols=20)

    worksheet.format('A2:F50000', {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})
    for i in range(0,len(content)):
        for j in range(1, len(values)):
            if  content[i][0] == values[j][0] and content[i][1] == values[j][1] and content[i][2] == values[j][2] and content[i][3] == values[j][3]  and content[i][5] == values[j][5]:
                if int(content[i][8])>int(values[j][8]):
                    if len(content[i])==9:
                        content[i].append('+++++++Ценна увеличилась, была - '+values[j][8])
                if int(content[i][8])==int(values[j][8]):
                    if len(content[i]) == 9:
                        content[i].append('Ценна не изменилась')
                if int(content[i][8])<int(values[j][8]):
                    if len(content[i]) == 9:
                        content[i].append('-------Ценна уменьшилась, была - '+values[j][8])
    content = sorted(content, key=lambda x: x[2])
    new_worksheet.update('A1:J1', name)
    new_worksheet.update('A2:J50000',content)







def main():


    url='https://100realty.ua/realty_search/nonlive/sale/cur_3/kch_2'
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