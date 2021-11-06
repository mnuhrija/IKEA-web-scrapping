import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm 

baseurl= 'https://www.ikea.co.id'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

productlinks= []

for i in range(1,12):
    r= requests.get('https://www.ikea.co.id/in/produk/kursi-makan')
    soup= BeautifulSoup(r.content, 'html.parser')
    productlist= soup.find_all('div', class_='itemInfo')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

productlist= []
for link in tqdm(productlinks, desc= 'Saving Data Product'):
    r= requests.get(link, headers=header)
    soup=BeautifulSoup(r.content, 'html.parser')

    productname= soup.find('h6', class_='display-7').text #productname
    productdescription= soup.find('h1', class_='itemFacts font-weight-normal').text #productdescription
    price= soup.find('p', class_= 'itemBTI display-6').text.strip() #price
    try:
        soldquantity= soup.find_all('p', class_= 'partNumber')[1].text #soldquantity
    except:
        soldquantity= 'No Data'
        
    chairIkea= {
        'product_name': productname,
        'product_description': productdescription,
        'price': price,
        'sold':soldquantity
        }
    productlist.append(chairIkea)

chair_df= pd.DataFrame(productlist)
print(chair_df.head(10))
chair_df.to_csv('IKEA_product.csv', index=False)