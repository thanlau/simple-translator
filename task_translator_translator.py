import requests
import argparse
from bs4 import BeautifulSoup
class trans:
    def __init__(self):
        self.url = None
        self.translator = {"1":"arabic",
                      "2":"german",
                      "3":"english",
                      "4":"spanish",
                      "5":"french",
                      "6":"hebrew",
                      "7":"japanese",
                      "8":"dutch",
                      "9":"polish",
                      "10":"portuguese",
                      "11":"romanian",
                      "12":"russian",
                      "13":"turkish"}

    def read_input(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('orgin_lang')
        parser.add_argument('dest_lang')
        parser.add_argument('words')
        args = parser.parse_args()
        self.orgin = args.orgin_lang
        self.dest = args.dest_lang
        self.words = args.words
        if self.dest == 'all':
            for k in self.translator:
                if self.translator[k].lower() == self.orgin:
                    continue
                self.execute_command(self.orgin, self.translator[k], self.words)
        else:
            if self.orgin not in self.translator.values():
                print("Sorry, the program doesn't support {}".format(self.orgin))
                return
            if self.dest not in self.translator.values():
                print("Sorry, the program doesn't support {}".format(self.dest))
                return
            self.execute_command(self.orgin, self.dest, self.words)
        with open('{}.txt'.format(self.words), 'r', encoding = 'utf-8') as file:
            print(file.read())

    def menu(self):
        print('''Hello, you're welcome to the translator. Translator supports: 
        1. Arabic
        2. German
        3. English
        4. Spanish
        5. French
        6. Hebrew
        7. Japanese
        8. Dutch
        9. Polish
        10. Portuguese
        11. Romanian
        12. Russian
        13. Turkish
        Type the number of your language:''')
        from_ = input()
        print("Type the number of a language you want to translate to or '0' to translate to all languages:")
        to_ = input()
        print("Type the word you want to translate:")
        word = input()
        if to_ == '0':
            for k in self.translator:
                if k == from_:
                    continue
                self.execute_command(from_, k, word)
        else:
            self.execute_command(from_, to_, word)
        with open('{}.txt'.format(word), 'r', encoding = 'utf-8') as file:
            print(file.read())


    def execute_command(self, from_, to_, word):
        self.url = "https://context.reverso.net/translation/{}-{}/{}".format(from_.lower(), to_.lower(),word)
        print(self.url)
        print_lang = to_
        try:
            words, sentences = self.handler()
        except:
            return
        # print("Context examples:\n")
        self.save_res(words,sentences, print_lang, word)


    def save_res(self, words, sentences, print_lang, word):
        title_tran= print_lang+" Translations:"
        title_ex= print_lang+" Example:"
        with open('{}.txt'.format(word), 'a+', encoding = 'utf-8') as file:
            file.write(str(title_tran)+'\n')
            file.write(words[0]+'\n')
            file.write(str(title_ex)+'\n')
            file.write(sentences[0]+':\n')
            file.write(sentences[1]+'\n')
            # file.seek(0)
            # for _ in file:
            #     print(file.readline())
        # for i in range(0,5):
        #     print(words[i])
        # for i in range(0, 11, 2):
        #     print(sentences[i])
        #     print(sentences[i+1]+"\n")


    def handler(self):
        header = {"User-Agent":"Chrome/87.0.4280.88"}
        try:
            r = requests.get(self.url, headers=header)
        except ConnectionError:
            print("Something wrong with your internet connection")
            return
        if r.status_code != 200:
            print("Sorry, unable to find {}".format(self.words))
            return
        # print('Translations')
        soup = BeautifulSoup(r.content, 'html.parser')
        words = soup.select('#translations-content .translation')
        examples = soup.select('#examples-content .example .text')
        res=[]
        res1=[]
        for i in words:
            res.append((i.text.strip()))
        for i in examples:
            res1.append(i.text.strip())
        return res, res1

if __name__ == '__main__':
    trans().read_input()

