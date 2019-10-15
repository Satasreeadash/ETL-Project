from bs4 import BeautifulSoup as bs
import requests

def price_searcher(product):
    product = str(product)
    query_url = 'https://www.google.com/search?tbm=shop&q=' + product
    response = requests.get(query_url)
    soup = bs(response.text, 'html.parser')

    item = soup.findAll('div', {'class': 'pslires'})
    mydict = {}

    for x in range(len(item)):
        image = item[x].findAll('div', {'class': 'psliimg'})
        image_link = image[0].find('img')['src']

        link = item[x].findAll("div", {"class": "A8OWCb"})
        for x in range(len(link)):
            link2 = link[x].findAll('div')
            if 'from' in link2[1].text:
                continue
            else:
                mydict[link2[1].text] = [link2[0].text]
            mydict[link2[1].text].append(image_link)

    sum1 = 0
    count = 0
    values = []
    for key in mydict:
        strings = mydict[key][0].split()
        number = strings[0][1:]
        number = number.replace(',','')
        number = float(number)
        if number != 0:
            sum1 += number
            count+= 1
        if len(strings) > 1:
            values.append(number)
            values.append(strings[1])
            values.append(mydict[key][1])
            mydict[key] = values
        else:
            values.append(number)
            values.append('new')
            values.append(mydict[key][1])
            mydict[key] = values
        values = []
    if count == 0:
        average = 0
    else:
        average = sum1 / count

    removes = []
    for key in mydict:
        if mydict[key][0] < average*0.25:
            removes.append(key)

    for x in range(len(removes)):
        del mydict[removes[x]]


    return mydict
