"""roketin_adi = "Rumeli Roketi"
roketin_kutlesi = 2.5
roketin_kanatcik_sayisi = 5
roketin_firlatilma_durumu = True
print(type(roketin_adi))
print(type(roketin_firlatilma_durumu))
print(type(roketin_kanatcik_sayisi))
print(type(roketin_kutlesi))
roketin_irtifasi = 250
print(roketin_irtifasi + 50)
print(roketin_irtifasi)
print(roketin_kutlesi)
print(roketin_kanatcik_sayisi)
print(roketin_adi)
print(roketin_firlatilma_durumu)"""



"""
roketin_agirligi = m*g
print(roketin_agirligi)

v0 = 50 
t = 2
h = v0 * t - (1/2) * g * t * t
print(h)


ucus_suresi = 120
ucus_suresi_dakika = ucus_suresi//60 
ucus_suresi_saniye = ucus_suresi%60
print("Ucus suresi", ucus_suresi_dakika,  "dakika ve" , ucus_suresi_saniye, "saniyedir" )
"""

"""deneme1 = (input("deneme icin sayi girin: "))
print(deneme1 * 2)
"""



"""roketin_kutlesi = float(input("roketin kutlesini yazin: "))
g = 9.81
roketin_agirligi = roketin_kutlesi*g
roketin_adi = input("roketin adini yaziniz: ")
print(f"{ roketin_adi}nin agirligi { roketin_agirligi}N'dir " )

irtifa_icin_g = float(input("istenilen g degerini yaziniz: "))
irtifa_icin_v0 = float(input("istenilen v0 degerini yaziniz: "))
irtifa_icin_t = float(input("istenilen t degerini yaziniz: "))
h = irtifa_icin_v0 * irtifa_icin_t - 1 / 2 * irtifa_icin_g * irtifa_icin_t * irtifa_icin_t
print(f"roketin irtifasi {h}'dir")"""

"""ruzgarin_hizi = float(input("ruzgarin hizini m/s olarak yaziniz: "))
if ruzgarin_hizi > 9:
    print("Firlatma iptal")
else:
    print("Firlatmaya hazir")

roketin_dikey_hizi = float(input("roketin dikey hizini m/s olarak yaziniz: "))
if roketin_dikey_hizi > 0:
    print("Yukseliyor")
elif roketin_dikey_hizi == 0:
    print("Tepe noktasinda")
else :
    print("Dusuyor")

irtifa_icin_g = float(input("istenilen g degerini yaziniz: "))
irtifa_icin_v0 = float(input("istenilen v0 degerini yaziniz: "))
irtifa_icin_t = float(input("istenilen t degerini yaziniz: "))
h = irtifa_icin_v0 * irtifa_icin_t - 1 / 2 * irtifa_icin_g * irtifa_icin_t * irtifa_icin_t
if h < 0:
    print("Roket yere dusmus, formul gecersiz")
elif h > 0 :
    print(f"roketin irtifasi {h}'dir")
else :
    print("Roket yerde duruyor")
print(h)"""

#deneme 1
"""sayi_1 = 10
for i in range(10):
    print(sayi_1 - i)
    if i == 9 :
        print("Kalkis!")
#deneme 2
sayi = 10
for a in range(0, -10, -1):
    print(sayi + a)
    if a == -9:
        print("kalkis")
"""

"""v0 = 50
g = 10
for t in range(0, 11, 1):
    h = v0 * t - 1/2 * g * t * t
    print(h)
    v = v0 - g * t
    print(t,h,v)"""


"""v0 = 50
g = 10
t = 0
v = v0 - g * t
h = v0 * t - 1/2 * g * t * t
while v > 0:
    t = t + 0.1
    h = v0 * t - 1/2 * g * t * t
    v = v0 - g * t
print(h)
print(t)"""


"""for i in range(10, 0, -1):
    print(i)
print("kalkis!")
g = 10
for i in range(0, 11, 1):
    t = i/2
    h = 125 - 1/2 * g * t * t 
    v = -g * t
    print(t, h, v)
"""



"""irtifa_olcumu = [0.0, 12.5, 30.2, 48.0, 50.1, 49.8]

print(irtifa_olcumu[0])
print(irtifa_olcumu[-1])
olcum_sayisi = len(irtifa_olcumu)
print(olcum_sayisi)
print(irtifa_olcumu[2])

irtifalarin_toplami = 0.0
for i in irtifa_olcumu:
    irtifalarin_toplami = irtifalarin_toplami + i
print(f"ortalama irtifa {irtifalarin_toplami/olcum_sayisi}'dir")

max_irtifa = irtifa_olcumu[0]
for i in irtifa_olcumu:
    if max_irtifa < i:
      max_irtifa = i
print(f"En yuksek irtifa {max_irtifa}'dir")

bos_bir_liste = []
g = 10
for i in range(0, 11, 1):
    t = i/2
    h = 125 - 1/2 * g * t * t 
    v = -g * t
    bos_bir_liste.append(h)
print(bos_bir_liste)
print(len(bos_bir_liste))
print(bos_bir_liste[-1])

deneme = [-5.0, -3.0, -8.0]
Hiz = deneme[0]
for b in deneme:
    if Hiz < b:
      Hiz = b
print(f"En yuksek hiz {Hiz}'dir")"""
"""
irtifalarin_toplami = 0.0
for i in irtifa_olcumu:
     irtifalarin_toplami = irtifalarin_toplami + i

irtifa_olcumu = [0.0, 12.5, 30.2, 48.0, 50.1, 49.8]

max_irtifa = irtifa_olcumu[0]"""

"""ornek_liste = [10, 20, 30]
def ortalama(liste):
     toplam = 0
     for i in liste:
      toplam = toplam + i
     return toplam/len(liste)
print(ortalama(ornek_liste))

irtifa_olcumu = [0.0, 12.5, 30.2, 48.0, 50.1, 49.8]
def en_buyuk(liste):
   en_buyuk_irtifa = liste[0]
   for a in liste:
      if en_buyuk_irtifa < a :
         en_buyuk_irtifa = a
   return en_buyuk_irtifa
print(en_buyuk(irtifa_olcumu))"""

"""g = 9.81
kutle = 1.2
agirlik = g * kutle
def gerekli_itki(kutle,g):
   return kutle * g 
print(gerekli_itki(kutle, g))
def durum(itki,kutle,g):
   if itki > gerekli_itki(kutle, g):
      return "yukseliyor"
   elif itki == gerekli_itki(kutle, g) :
      return "Askida"
   else:
      return "Alcaliyor"
print(durum(5, 1, 10))
"""
"""hiz = [-5.0, -3.0, -8.0]
print(en_buyuk(hiz))
print(ortalama(irtifa_olcumu))"""

"""

iha = {"adi" : "Rumeli", "kutlesi" : 1.2, "motor sayisi" : 4, "batarya kapasitesi" : 5000}
print(iha["adi"]) 
kameranin_kutlesi = 0.3
print(iha["kutlesi"])
iha["kutlesi"] = iha["kutlesi"] + kameranin_kutlesi
print(iha["kutlesi"])
iha["kamera"] = True
print(iha["kamera"])
for anahtar, deger in iha.items():
    print(anahtar, deger)

def gerekli_itki(kutle, g):
    return kutle * g
print(gerekli_itki(iha["kutlesi"], 10))

iha["renk"] = "sari"

print(iha["renk"])
aranan_anahtar = input("kontrol etmek istediginiz degiskeni yazin: ")
if aranan_anahtar in iha:
    print(f"istediginiz degisken sozlukte vardir")
else :
    print("Bilgi yok")

def ucus_suresi(iha, akim):
  kapasite_ah = iha["batarya kapasitesi"]/1000
  kullanim_orani = 0.8
  kullanilabilir_batarya = kapasite_ah * kullanim_orani
  return (kullanilabilir_batarya / akim) * 60
print(ucus_suresi(iha, 10))
"""

"""with open("ucus_kaydi.txt", "w") as dosya:
    dosya.write(5)

with open("ucus_kaydi.txt", "r") as dosya:
    for satir in dosya:
        print(satir.strip())
"""
"""g = 10
bos_bir_liste = []
with open("ucus_kaydi.txt", "w") as dosya:
 for i in range(0, 11, 1):
    t = i/2
    h = 125 - 1/2 * g * t * t 
    v = -g * t
    bos_bir_liste.append(h)
    dosya.write(f"{t}, {h}, {v}\n") """

bos_bir_liste_2 = []
with open("ucus_kaydi.txt", "r") as dosya:
   for satir in dosya:
    parcalar = satir.split(",")
    okunan_irtifa = float(parcalar[1])
    bos_bir_liste_2.append(okunan_irtifa)
print(bos_bir_liste_2)

en_yuksek_irtifa = bos_bir_liste_2[-1]
for i in bos_bir_liste_2:
   if en_yuksek_irtifa < i :
      en_yuksek_irtifa = i
print(en_yuksek_irtifa)
toplam_irtifa = 0
for a in bos_bir_liste_2:
   toplam_irtifa = a + toplam_irtifa
ortalama_irtifa = toplam_irtifa / len(bos_bir_liste_2)
print(ortalama_irtifa)
