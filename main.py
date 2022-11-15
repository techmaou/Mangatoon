import time
import csv
import requests as re
from bs4 import BeautifulSoup as bs


class MangaToon:

    def __init__(self, fpage):

        self.comicList = []
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'referer': 'https://mangatoon.mobi/en/genre/comic'
        }

        for i in range(1, fpage):

            url = 'https://mangatoon.mobi/en/genre/comic?page={}'.format(i)
            print(url)

            self.res = re.get(url, headers=headers)

            if self.res.status_code == 200:
                self.getDetails()
            else:
                raise Exception("Sorry. request failed.")
            time.sleep(6)

    def getDetails(self):

        self.soup = bs(self.res.content, "html.parser")

        for item in self.soup.find_all('div', class_='item'):

            comicDetails = {}

            comicDetails['Content Title'] = item.find(
                'div', class_='content-title').text
            comicDetails['Content Watch Count'] = item.find(
                'div', class_='watch-count').text.split('\n')[-2]

            ep = item.find(
                'div', class_='open-episode-count').text.split('.')[-1]
            comicDetails['Content Episodes'] = int(ep)

            comicDetails['Content Tags'] = item.find(
                'div', class_='tags').text.split('/')

            self.comicList.append(comicDetails)

    def saveCSV(self, filename):

        filedsname = [i for i in self.comicList[0]]

        with open('{}.csv'.format(filename), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=filedsname)
            writer.writeheader()
            writer.writerows(self.comicList)
