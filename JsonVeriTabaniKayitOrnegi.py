import json
import re # Kullanıcı kayıtlarını kontrol edeceğiz.
import time
import random # Üyelik sonucunda random bir aktivasyon kodu göndermek için.

class Site:
    def __init__(self):
        self.dongu = True # programı biz çıkış vermediğimiz müddetçe açık bırakmak.
        self.veriler = self.verial() # verial isimli bir fonksiyon yapacağım, veritabanındaki verileri okumak ve veriler isimli objeye tanımlamak.

    def program(self):
        # Ben çıkış vermediğim sürece, ekrana menü vericek.
        secim = self.menu()
        
        if secim == "1":
            self.giris()
        if secim == "2":
            self.kayitol()
        if secim == "3":
            self.cikis()
            
    def menu(self): #Kontrol fonksiyonu yapmam lazım. Kullanıcı 1-2-3 dışında bir şey seçmemeli.
        
        def kontrol(secim):
            if re.search("[^1-3]", secim):
                raise Exception("Lütfen 1 ve 3 arasında geçerli bir seçim yapınız.")
            if len(secim) != 1:
                raise Exception("Lütfen 1 ve 3 arasında geçerli bir seçim yapınız.")
        
        while True: # While True döngüsüne sokmam lazımki, kullanıcı 1-3 dışında seçerse tekrar tekrar çalışsın.
            try:
                secim = input("Merhaba, Kösoğlu Sitesine hoşgeldiniz. \n\nLütfen yapmak istediğiniz işlemi seçiniz...\n\n[1]-Giriş\n[2]-Kayıt ol\n[3]-Çıkış\n\n")
                kontrol(secim)
            except Exception as Hata:
                print(Hata) # Kontrol fonksiyonunda hangi hata alınırsa onu yazdır.
                time.sleep(2)
            else:
                break # Kişi doğru secim yaptığında break ile döngüyü sonlandırıyorum.
        return secim
    
    def giris(self):
        
        print("Giriş menüsüne yönlendiriliyorsunuz...")
        time.sleep(2)
        Kullanici_Adi = input("Kullanıcı Adınızı Giriniz: ")
        Kullanici_Sifre = input("Kullanıcı Şifrenizi Giriniz: ")
        
        sonuc = self.giriskontrol(Kullanici_Adi, Kullanici_Sifre)
        
        if sonuc == True: # Kullanıcı adı ve şifresi giriskontrol'den doğru olarak girerse anlamına gelir. 
            self.girisbasarili()
        else:
            self.girisbasarisiz()
    
    def giriskontrol(self, Kullanici_Adi, Kullanici_Sifre):
        
        self.veriler = self.verial() # self.verial'ın jsondan aldığı verileri self.veriler e eşitliyoruz.
        
        try:
            for kullanici in self.veriler["Kullanıcılar"]: # Json datası sözlük datası gibi olduğundan dolayı. Sözlük yapısı içerisinde liste içinde tutuluyor. Bu yüzden for döndürdük.
                if kullanici["Kullanıcıadı"] == Kullanici_Adi and kullanici["Sifre"] == Kullanici_Sifre:
                    return True
        except KeyError:
            return False
        return False
        
    def girisbasarili(self):
        
        print("Kontrol Ediliyor...")
        time.sleep(2)
        print("Giriş Başarılı. Kösoğlu Sitesine hoşgeldiniz.")
        self.sonuc = False
        self.dongu = False
    
    def girisbasarisiz(self):
        
        print("Kullanıcı Adı veya Şifreniz Hatalıdır!!!")
        time.sleep(1)
        self.menudon()
    
    def kayitol(self):
        
        def kontrolka(Kullanici_Adi):
            if len(Kullanici_Adi) < 8:
                raise Exception("Kullanıcı adınız en az 8 karakterden oluşmalıdır.")
        
        while True:
            try:
                Kullanici_Adi = input("Kullanıcı Adınız: ")
                kontrolka(Kullanici_Adi)
            except Exception as HataAd:
                print(HataAd)
                time.sleep(2)
            else:
                break
    
        def kontrolsifre(Kullanici_Sifre):
            if len(Kullanici_Sifre) < 8:
                raise Exception("Şifreniz en az 8 karakterden oluşmalıdır.")
            elif not re.search("[0-9]", Kullanici_Sifre): # Sifre içerisinde 0-9 arasında rakam yok ise.
                raise Exception("Şifrenizde en az 1 tane rakam olmalıdır.")
            elif not re.search("[A-Z]", Kullanici_Sifre):
                raise Exception("Şifrenizde en az 1 tane büyük harf olmalıdır.")
            elif not re.search("[a-z]", Kullanici_Sifre):
                raise Exception("Şifrenizde en az 1 tane küçük harf olmalıdır.")
            
        while True:
            try:
                Kullanici_Sifre = input("Şifreniz: ")
                kontrolsifre(Kullanici_Sifre)
            except Exception as HataSifre:
                print(HataSifre)
                time.sleep(2)
            else:
                break
            
        def kontrolmail(Mail):
            if not re.search("@", Mail):
                raise Exception("Lütfen geçerli bir mail adresi giriniz: ")
            elif not re.search(".com", Mail):
                raise Exception("Lütfen geçerli bir mail adresi giriniz: ")
        
        while True:
            try:
                Mail = input("Mail adresinizi giriniz: ")
                kontrolmail(Mail)
            except Exception as HataMail:
                print(HataMail)
                time.sleep(2)
            else:
                break
        
        sonuc = self.kayitvarmi(Kullanici_Adi, Mail)
        if sonuc == True:
            print("Bu kullanıcı adı ve mail adresi, sistemde kayıtlıdır.")
        else:
            aktivasyonkodu = self.aktivasyongonder()
            durum = self.aktivasyonkontrol(aktivasyonkodu) # eşleşme durumunda durum = false,true dönecek.
        
        while True:
            if durum == True:
                self.verikaydet(Kullanici_Adi, Kullanici_Sifre, Mail)
                break
            else:
                print("Aktivasyon kodunuz hatalıdır.")
                time.sleep(1)
                self.menudon()
            
        
    def kayitvarmi(self, Kullanici_Adi, Mail):
        
        self.veriler = self.verial()
        try:
            for kullanici in self.veriler["Kullanıcılar"]:
                if kullanici["Kullanıcıadı"] == Kullanici_Adi and kullanici["Mail"] == Mail:
                    return True
        except KeyError:
            return False
        return False
    
    def aktivasyongonder(self):
        
        with open("C:/Users/Mehmet Akif/Desktop/Aktivasyon.txt","w", encoding="utf-8") as Dosya:
            aktivasyon = str(random.randint(10000, 99999))
            Dosya.write("Aktivasyon Kodunuz:" + aktivasyon)
        return aktivasyon
    
    def aktivasyonkontrol(self, aktivasyon):
        
        aktivasyonkodual = input("Lütfen mailinize gelen aktivasyon kodunu giriniz: ")
        if aktivasyon == aktivasyonkodual:
            return True
        else:
            return False
    
    # json veritabanından veri alacak.
    def verial(self): # bir json dosya yapısında olacak.
        # ilk olarak bilgisayarımızda json dosyasını arayacak. Bulamazsa error verecek. Bu errordan kaçınmak için try bloğunda yazıyorum.
        try: # bir hata döndürürse
           with open("C:/Users/Mehmet Akif/Desktop/Kullanıcılar.json","r", encoding="utf-8") as Dosya: # Masaüstünde böyle bir dosya varsa okuyacak.
               veriler = json.load(Dosya) # Okuma yapısı.
        except FileNotFoundError: # Dosyayı bulamazsa bu hatayı verecek. Ve bu hatayı verdiğinde 0 dan dosya oluşturmasını isteyeceğim.
            with open("C:/Users/Mehmet Akif/Desktop/Kullanıcılar.json","w", encoding="utf-8") as Dosya:
                Dosya.write("{}")
            with open("C:/Users/Mehmet Akif/Desktop/Kullanıcılar.json","r", encoding="utf-8") as Dosya: # Masaüstünde böyle bir dosya varsa okuyacak.
               veriler = json.load(Dosya)
        return veriler # verileri verial fonksiyonuna döndürecek-gönderecek.
                
    # yeni kullanıcı verilerini, json dosyasına kaydedicez.
    def verikaydet(self, Kullanici_Adi, Kullanici_Sifre, Mail): # Kullanıcı adı, şifre, maili, json dosyasına yazma işlemini gerçekleştirecek.
        
        self.veriler = self.verial()
        try:
            self.veriler["Kullanıcılar"].append({"Kullanıcıadı": Kullanici_Adi, "Sifre" : Kullanici_Sifre, "Mail" : Mail}) # girilen veriler sözlük yapısı gibi.
        except KeyError: # Hata yapısı varsa, ne yapacak. Kullanıcıadını bulamazsa
            self.veriler["Kullanıcılar"] = list()
            self.veriler["Kullanıcılar"].append({"Kullanıcıadı": Kullanici_Adi, "Sifre" : Kullanici_Sifre, "Mail" : Mail})
        
        with open("C:/Users/Mehmet Akif/Desktop/Kullanıcılar.json","w", encoding="utf-8") as Dosya:
            json.dump(self.veriler, Dosya, ensure_ascii=False, indent=4) # Türkçe karakter sorununu halletmek için utf-8 gibi. Indent, alt alta yazabilmek için. 4 karakter boşlukla aşağıda gerçekleştirecek.
            print("Kayıt Başarılı Şekilde Oluşturulmuştur...")
            self.menudon()
            
    def cikis(self):
        
        print("Siteden çıkılıyor.")
        time.sleep(2)
        self.dongu = False
        exit()
    
    def menudon(self):
        
        while True:
            x = input("Ana menüye dönmek için 5'e, çıkmak için 4'e basınız...: ")
            if x == "5":
                print("Ana menüye dönülüyor...")
                time.sleep(2)
                self.program()
                break
            elif x == "4":
                self.cikis()
                break
            else:
                print("Lütfen geçerli bir seçim yapınız...")
    
Sistem = Site()
while Sistem.dongu:
    Sistem.program()