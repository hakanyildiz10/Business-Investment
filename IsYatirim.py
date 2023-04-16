import requests
from bs4 import BeautifulSoup
import time
import re

class Hisse:
    def __init__(self):
        self.dongu=True

    def program(self):
        secim=self.menu()

        if secim=="1":
            print("Güncel fiyatlar aliniyor.\n")
            time.sleep(3)
            self.guncelFiyat()      

        if secim=="2":
            print("Künye bilgileri aliniyor.\n")
            time.sleep(3)
            self.kunye() 

        if secim=="3":
            print("Cari değerler aliniyor.\n")
            time.sleep(3)
            self.cariDeger()

        if secim=="4":
            print("Getiri bilgileri aliniyor.\n")
            time.sleep(3)
            self.getiri()

        if secim=="5":
            print("Endeks ağirlik oranlari  aliniyor.\n")
            time.sleep(3)
            self.dahilEndeks()    

        if secim=="6":
            print("Otomasyondan çikiliyor.Teşekkürler.")
            time.sleep(3)
            self.cikis()                  

    def menu(self):
        def kontrol(secim):
            if re.search("[^1-6]",secim):
                raise Exception("Lütfen 1 ve 6 arasinda geçerli bir seçim yapiniz.")
            elif len(secim)!=1:
                raise Exception("Lütfen 1 ve 6 arasinda geçerli bir seçim yapiniz.")
        while True:
            try:
                secim=input("Merhaba, Anlaşilir Ekonomi otomasyon sistemine hoşgeldniz\n\nLütfen yapmak istediğiniz işlemi seciniz\n\n[1]Güncel Fiyat\n[2]Şirket Künyesi\n[3]Cari Değerler\n[4]Getiri Rakamlari\n[5]Şirketin dahil olduğu endeksler\n[6]Çikiş\n\n")
                kontrol(secim)
            except Exception as hata:
                print(hata) 
                time.sleep(3)
            else:
                break 
        return secim
    
    def guncelFiyat(self):
        while True:                              #kişiden girişte şirkey ismi istenir, eğer sitede yoksa tekrardan istenir
            try:                                  #kişinin verdiği şirket ismi olmamasından kaynaklı hata çevirir
                sirket=input("Lütfen şirket adi giriniz: ")

                url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"

                parser=BeautifulSoup(requests.get(url).content,"html.parser")  #burada html kodlarını aldıktan sonra aşağıdaki fiyat değişkeni ile a href etiketini find ile aldık, bu etikette şirket isimleri yazıyor

                fiyat=parser.find("a",{"href":"/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(sirket.upper())}).parent.parent.find_all("td")    #bu boşluğa hisse senedleri yazılacak, hisse kodunun tanınması için de senet isimleri büyük harf olmalı upper ile bunu sağladık, aranan değerler a etiketinin parent i olan td lerde olduğu için parent.find dedik, 0. endex hisse adı olduğu için yanındaki diğer indexlerdeki bilgileri aşağıda aldık
                bilgi1=fiyat[1].string                #hisse 0. index olduğu için son fiyat 1. index oldu ve köşeli paranteze yazıldı
                bilgi2=fiyat[2].span.string           #değişim % td classındaki span etiketi içindeki -1,25 değerinin yazılı olduğu bölümü çektik(bu değer site güncellendikçe değişir)
                bilgi3=fiyat[3].string
                bilgi4=fiyat[4].string
                bilgi5=fiyat[5].string 

                print(f"Son fiyat:{bilgi1}\nDeğişim(%):{bilgi2.lstrip()}\rDeğişim(TL):{bilgi3}\nHacim(TL):{bilgi4}\nHacim(Adet):{bilgi5}") 
                
            except AttributeError:            #bulunamayan bir şirket adı girildiğinde python da böyle bir hata döner
                print("Hatali bir şirket adi girdiniz.")
                break

        self.menuDon() 

    def kunye(self):
        while True:                             
            try:                               
                sirket=input("Lütfen şirket adi giriniz: ")

                url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(sirket)

                parser=BeautifulSoup(requests.get(url).content,"html.parser")  

                künye=parser.find("div",{"id":"ctl00_ctl58_g_6618a196_7edb_4964_a018_a88cc6875488"}).find_all("tr")    #şirket künyesine sağ tıklayıp edit inspect deyip html kodları çıkınca div etiketinde şirket künyesinin id si olduğu görülür ve onu yapıştırdık, bu id unvan,kuruluş gibi bütün tr yapılarını içinde barındırıyor
                for i in künye:
                    bilgi1=i.th.string               #tr class içindeki th ın string ini aldık
                    bilgi2=i.td.string 
                    print(f"{bilgi1}:{bilgi2}")
                break
    
            except AttributeError:           
                print("Hatali bir şirket adi girdiniz.")
                break

        self.menuDon() 

    def cariDeger(self):
        while True:                             
            try:                               
                sirket=input("Lütfen şirket adi giriniz: ")

                url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(sirket)

                parser=BeautifulSoup(requests.get(url).content,"html.parser")  

                cariDeger=parser.find("div",{"id":"ctl00_ctl58_g_76ae4504_9743_4791_98df_dce2ca95cc0d"}).find_all("tr")    #div class box content etiketi altındaki tr leri çekmek istiyoruz
                for i in cariDeger:
                    bilgi1=i.th.string               #tr etiketi içindeki th ler arasına sol taraftaki string ler yazılmış
                    bilgi2=i.td.string               #td ler arasına da sayısal ifadeler yazılmış
                    print(f"{bilgi1}:{bilgi2}")
                break
    
            except AttributeError:           
                print("Hatali bir şirket adi girdiniz.")
                break

        self.menuDon() 

    def getiri(self):
        while True:                             
            try:                               
                sirket=input("Lütfen şirket adi giriniz: ")

                url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(sirket)

                parser=BeautifulSoup(requests.get(url).content,"html.parser")  

                getiri=parser.find("div",{"id":"ctl00_ctl58_g_aa8fd74f_f3b0_41b2_9767_ea6f3a837982"}).find("table").find("tbody").find_all("tr")     #div class box content etiketi altındaki tr leri çekmek istiyoruz, önce table ı bulduk sonra table içindeki tbody yi bulduk, oradaki tr leri çekeceğiz
                
                for i in getiri:                 #tbody altında 3 tane tr etiketleri var, hepsini for döngüsüyle çekiyoruz
                    bilgi=i.find_all("td")              
                    print(f"Birim:{bilgi[0].string} Günlük(%):{bilgi[1].string} Haftalik(%):{bilgi[2].string} Aylik(%):{bilgi[3].string} Yil içi Getiri(%):{bilgi[4].string}") #thead etiketi yazıldı, 
                break
    
            except AttributeError:           
                print("Hatali bir şirket adi girdiniz.")
                break

        self.menuDon() 

    def dahilEndeks(self):
        while True:                             
            try:                               
                sirket=input("Lütfen şirket adi giriniz: ")

                url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(sirket)

                parser=BeautifulSoup(requests.get(url).content,"html.parser")  

                dahilEndeks=parser.find("div",{"id":"ctl00_ctl58_g_655a851d_3b9f_45b0_a2d4_b287d18715c9"}).find("table").find("tbody").find("tr").find_all("td")         #bir tane table var o yüzden find ile çektik   
                dahilEndeks2=parser.find("div",{"id":"ctl00_ctl58_g_655a851d_3b9f_45b0_a2d4_b287d18715c9"}).find("table").find("thead").find("tr").find_all("th")              #başlıkları alacak misal xu100 xu050
               
                for i in range(0,3):
                    print(f"{dahilEndeks2[i].string}:{dahilEndeks[i].string}")              #thead içinde de 3 tane th class var çünkü 3 başlık var, for döngüsünde sırasıyla bu başlıklar yazılacak 
                break                                                                       #tbody içinde de 3 tane td class var for döngüsü sırasıyla yazdırır

            except AttributeError:           
                print("Hatali bir şirket adi girdiniz.")
                break

        self.menuDon() 

    def cikis(self):
        self.dongu=False
        exit() 

    def menuDon(self):
        while True:
            x=input("Ana menüye dönmek için 7'ye, çikmak için lütfen 6'ya basiniz")
            if x=="7":
                print("Ana menüye dönülüyor")
                time.sleep(3)
                self.program()
                break
            elif x=="6":
                self.cikis() 
                break
            else:
                print("Lütfen geçerli bir seçim yapiniz.") 

Sistem=Hisse()
while Sistem.dongu:
    Sistem.program() 