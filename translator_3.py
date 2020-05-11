import requests
from bs4 import BeautifulSoup
import sys

class Translator():
    def __init__(self):
        return

    def welcome(self):
        args = sys.argv
        self.lang_list = [
            'null',
            'arabic', 
            'german', 
            'english', 
            'spanish', 
            'french', 
            'hebrew', 
            'japanese', 
            'dutch', 
            'polish', 
            'portuguese', 
            'romanian', 
            'russian', 
            'turkish'
            ]
        for i in self.lang_list:
            if i == args[1]:
                self.f = args[1]
        for i in self.lang_list:
            if i == args[2]:
                self.t = args[2]
            elif args[2] == 'all':
                self.t = 0
        self.word = args[3].lower()
        self.tall = []
        try:
            if self.t == 0:
                for i in self.lang_list[1:]:
                    self.choice = f'https://context.reverso.net/translation/{self.f}-{i}/{self.word}'
                    self.tall.append(self.choice)
                self.tall.remove(f'https://context.reverso.net/translation/{self.f}-{self.f}/{self.word}')
            else:
                try:
                    self.choice = f'https://context.reverso.net/translation/{self.f}-{self.t}/{self.word}'
                    self.tall.append(self.choice)
                except AttributeError:
                    print(f'Sorry, the program doesn\'t support {args[1]}')
        except AttributeError:
                    print(f'Sorry, the program doesn\'t support {args[2]}')

    def scrapping(self):
        for j in self.tall:
            self.filex = open(f'{self.word}.txt', 'a')
            # Language Title
            self.k = j.replace(f'https://context.reverso.net/translation/{self.f}-', '').split('/')[0].title()
            self.URL = j
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            try:
                html = requests.get(self.URL, headers=headers)
            except requests.ConnectionError:
                print('Something wrong with your internet connection')
                break

            # print(str(html.status_code) + ' OK') # Status page
            soup = BeautifulSoup(html.content, 'html.parser')
            # Return translated words
            words = soup.find('div', id='translations-content')
            self.t_words = []
            try:
                for i in words.find_all('a', class_='translation'):
                    self.t_words.append(i.text.strip())
                print()
                self.t_words.append('\n')
                print(self.k + ' Translations:')
                self.filex.write(self.k + ' Translations: \n')
                x = self.t_words[:5]
                for i in x:
                    print(i)
                    self.filex.write(f'{i} \n')
                print()
                self.t_words.append('\n')
            except AttributeError:
                print(f'Sorry, unable to find {self.word}')
                break
            # Return translated examples
            phrase = soup.find('section', id='examples-content')
            pr = []
            for i in phrase.find_all('div', class_='example'):
                for j in i.find_all('div', class_='src ltr'):
                    first = j.text.strip()
                    pr.append(first)
                for k in i.find_all('div', class_='trg ltr'):
                    second = k.text.strip()
                    pr.append(second)
            print(self.k + ' Examples:')
            self.filex.write(self.k + ' Examples: \n')
            for i in range(0, len(pr) // 2, 2):
                print(pr[i])
                self.filex.write(f'{pr[i]} \n')
                print(pr[i + 1])
                self.filex.write(f'{pr[i + 1]} \n')
                if i == 8:
                    break
                else:
                    print()
                    self.t_words.append('\n')
            self.filex.close()


trans = Translator()
trans.welcome()
trans.scrapping()