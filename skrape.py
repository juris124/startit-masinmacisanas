import requests
from bs4 import BeautifulSoup as bs
import csv
import time

URL = 'https://www.ss.lv/lv/transport/cars/today-5/filter/'
LAPAS = 'lapas/'
DATI = 'dati/'

# rezultats = requests.get(URL)
# print (rezultats.status_code)
# print(rezultats.text)

def saglaba(url, datne):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(datne, 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)

#saglaba(URL, LAPAS + '01_pirma_lapa.html')

def info(datne):
    dati = []
    with open(datne, 'r', encoding="UTF-8") as f:
        html = f.read()
    # print(html)
    # paarveertiisim html saturu par labu zupu
    zupa = bs(html, "html.parser")
    galvena = zupa.find(id = 'page_main')
    tabulas = galvena.find_all("table") # atgiež to sarakstu kur atrod elementu, tā kā ir saraksts, tad tas būs indksēts
    
    # for tabula in tabulas:
    #     print(tabula)
    #     print("=============================")
    #     print("=============================")
    #     print("=============================")
    #print(tabulas[2])
    #print(galvena)
    auto_tabula = tabulas[2]
    rindas = auto_tabula.find_all("tr")

    for rinda in rindas[1:-1]:
        lauki = rinda.find_all("td")
        auto = {}
        
        auto["saite"] = lauki[1].find("a")["href"]
        auto["bilde"] = lauki[1].find("img")["src"]
        auto["apraksts"] = lauki[2].find("a").text.replace("\n", " ")

        lauki[3].br.replace_with("!")

        auto["marka"] = lauki[3].text.replace("!", " ")
        auto["razotajs"] = lauki[3].text.split("!")[0]
        auto["modelis"] = lauki[3].text.split("!")[1]
        auto["gads"]  = lauki[4].text

        tilpums = lauki[5].text        
        
        if tilpums[-1] == "D":
            auto["dzinejs"] = "Dīzelis"
            auto["tilpums"] = tilpums[:-1]
        elif tilpums[-1] == "H":
            auto["dzinejs"] = "Hibrīds"
            auto["tilpums"] = tilpums[:-1]
        else:
            auto["dzinejs"] = "Benzīns"
            auto["tilpums"] = tilpums

        if not lauki[6].text == "-":
            auto["nobraukums"] = lauki[6].text.replace(" tūkst.", " 000 km")
        else:
            continue
            # šis kā alternatīva
            auto["nobraukums"] = ""


        auto["cena"] = lauki[7].text.replace(" €", "").replace(",", "")

        #cena = lauki[7].text.replace(" €", "").replace(",", "")
        #print(cena)

        #nobraukums = lauki[6].text.replace(" tūkst.", "")
        #print(nobraukums)

        
        
        #apraksts = lauki[2].find("a").text.replace("\n", " ")       
        #modelis = lauki[3].text.split("!")[1]
        

        print(auto)
        print("=================================================================")
        dati.append(auto)
        #print(dati)
    return dati


        # for lauks in lauki:
        #     print(lauks)
        #     print("=====================================")
        
        #exit()
        
        # print(rinda)
        # print("======================")
        # print("======================")


def saglaba_datus(dati):
    with open(DATI + 'ss_auto.csv', 'w', encoding='UTF-8', newline="") as f:
        kolonu_nosaukumi = ['razotajs', 'modelis', 'marka', 'gads', 'dzinejs', 'tilpums', 'nobraukums', 'cena', 'apraksts', 'bilde', 'saite']
        w = csv.DictWriter(f, fieldnames = kolonu_nosaukumi)
        w.writeheader()
        for auto in dati:
            w.writerow(auto)

d1 = info(LAPAS + "01_pirma_lapa.html")
print(d1)
saglaba_datus(d1)


# lapu vilksana
def atvelkam_lapas(cik):
    datne = "{}page1.html".format(LAPAS)
    saglaba(URL, datne)
    time.sleep(2)

    for i in range(2, cik + 1):
        url = "{}page{}.html".format(URL, i)
        datne = "{}page{}.html".format(LAPAS, i)
        print(url)        
        print(datne)
        saglaba(url, datne)
        time.sleep(5)

# sho jaapalaizj tikai 1 reizi, lai nevelk !!!!!!!!!!!!!!
#atvelkam_lapas(50)

# d3 = info(LAPAS + "page3.html")
# print(d3)

def izvelkam_datus(cik):
    visi_dati = []
    for i in range(1,cik+1):
        datne = "{}page{}.html".format(LAPAS, i)
        datnes_dati = info(datne)
        visi_dati += datnes_dati
    saglaba_datus(visi_dati)
izvelkam_datus(50)