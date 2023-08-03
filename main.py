from kompas import ScrapKompas

if __name__ == '__main__':
    while True:
        try:
            url = input('\nMasukkan url yang akan di scrapping!\n> ')
            # http://www.kompas.com/global/read/2023/08/02/095400370/wali-kota-di-meksiko-dikecam-karena-hadirkan-penari-striptis-dalam
            ScrapKompas(url)
            print('\nBerhasil')
            break
        except:
            print('Coba lagi')
