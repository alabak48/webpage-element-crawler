
import requests
from bs4 import BeautifulSoup


def poberi(url):

    try:
        page = requests.get(url)
        if page.history:
            print("Request was redirected")
            for resp in page.history:
                print(resp.status_code, resp.url)
            print("Final destination:")
            print(page.status_code, page.url)
        else:
            print("Request was not redirected")

        soup = BeautifulSoup(page.content, 'html.parser')
        elementi = soup.html.findAll()
        # print(lay_content)
        el = ['html', ]  # we already include the html tag
        for n in elementi:
            if n.name not in el:
                print('element: ', n.name)
                # print(type(n.attrs))
                # print('atributi: ', n.attrs)
                for key in n.attrs:
                    print('atribut: ', key, ', vrijednost: ', n.attrs[key])
    except:
        print('Greška pri dohvaćanju')




if __name__ == '__main__':
    # ovdje će se dovući popis
    # moramo paziti da prođemo i s http i https isto tako www. i bez www. (ovo je iskustvo s prethodnih pobiranja)
    poberi('http://ffos.hr')

