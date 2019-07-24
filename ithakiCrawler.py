import requests
from bs4 import BeautifulSoup as BS
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement


class IthakiCrawler:

    def __init__(self):
        self.pageCount = 47
        self.url = "http://www.ithaki.com.tr/kitaplar/page/{}/"
        self.file = None
        self.new_array = []

    def crawler(self):
        # ToDo: Eğer urlList.txt çekilmediyse bu fonksiyonu yorum satırından çıkarın.
        # self.getAllProduct()
        # ToDo: Eğer urlList.txt çekilmediyse bu fonksiyonu yorum satırından çıkarın.
        self.getProductUrlFromList()

    def getProductUrlFromList(self):
        productList = self.readListToFile()

        for link in productList:
            fixedLink = link.replace("\n", "")
            print(fixedLink)
            self.getProductFromUrl(fixedLink)

        self.writeToXML(self.new_array)


    def writeToXML(self, array):
        ithakiProducts = Element('ithaki')
        products = SubElement(ithakiProducts, 'products')
        for i in array:
            product = SubElement(products, 'product')
            SubElement(product, 'BookName', name='BookName').text = i['BookName']
            SubElement(product, 'BookOriginalName', name='BookOriginalName').text = i['BookOriginalName']
            SubElement(product, 'Novelist', name='Novelist').text = i['Novelist']
            SubElement(product, 'Translator', name='Translator').text = i['Translator']
            SubElement(product, 'Editor', name='Editor').text = i['Editor']
            SubElement(product, 'Type', name='Type').text = i['Type']
            SubElement(product, 'PageCount', name='PageCount').text = i['PageCount']
            SubElement(product, 'Price', name='Price').text = i['Price']
            SubElement(product, 'Description', name='Description').text = i['Description']

        output_file = open('ithakiProductList.xml', 'w')
        output_file.write('<?xml version="1.0"?>')
        output_file.write(ElementTree.tostring(ithakiProducts).decode("utf-8"))
        output_file.close()

    def getProductFromUrl(self, url):
        req = requests.get(url)
        soup = BS(req.content, 'lxml')
        content = soup.select("#editionnal-reviews span.detail-desc p")
        bookDesc = soup.select_one(".book-desc")

        if len(content) > 0:
            product = dict(
                BookName=content[0].text.strip().replace('Kitap Adı :', '').strip(),
                BookOriginalName=content[1].text.strip().replace('Kitabın Orjinal Adı :', '').strip(),
                Novelist=content[2].text.strip().replace('Yazar(lar) :', '').strip(),
                Translator=content[3].text.strip().replace('Çevirmen :', '').strip(),
                Editor=content[4].text.strip().replace('Editör :', '').strip(),
                Type=content[5].text.strip().replace('Tür :', '').strip(),
                PageCount=content[6].text.strip().replace('Sayfa Sayısı :', '').strip(),
                Price='0',
                Description=bookDesc.text.strip()
            )
            self.new_array.append(product)

    def getAllProduct(self):
        for page in range(1, self.pageCount):
            searchURL = self.url.format(page)
            self.parser(searchURL)

    def parser(self, url):
        req = requests.get(url)
        soup = BS(req.content, 'lxml')
        li = soup.select("li.product .book-item")
        urlList = []
        for i in li:
            href = i.select_one("a").get('href')
            urlList.append(href)
        self.writeListToFile(urlList)

    @staticmethod
    def writeListToFile(list):
        with open('urlList.txt', 'a+') as file:
            for item in list:
                file.write("%s\n" % item)
    @staticmethod
    def readListToFile():
        with open('urlList.txt', 'r') as file:
            array = file.readlines()
            return array


IthakiCrawler().crawler()
