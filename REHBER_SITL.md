# ArduPilot SITL Kurulum Rehberi (Windows)

SITL (Software-in-the-Loop), bilgisayarda çalışan, simüle edilmiş bir İHA'dır. Bu sistem sayesinde İHA'yı gerçek hayatta uçurmadan önce simülasyonda istediğimiz kadar test edebiliriz.

> **TASLAK** — Bu rehberdeki komutlar aşağıdaki sistemde denenip çalıştı. Rehberin son hali 20 Aralık'ta hazır olacak.

## Bu rehber nasıl kullanılır?

- Adımları **sırayla** yap. Bir adımı atlama.
- Her komutu yazdıktan sonra **Enter**'a bas. Enter'a basmazsan bilgisayar beklemeye devam eder.
- Her adımın altında **"Doğru gittiyse"** kısmı var. Ekranında o yazıyı görmeden bir sonraki adıma geçme.
- Komutlardaki `kullanici` kelimesini, 2. bölümde seçtiğin kullanıcı adıyla değiştir.
- Ubuntu terminaline bir şey **yapıştırmak** için **sağ tık** ya da **Ctrl+Shift+V** kullan. Ctrl+V çalışmaz.
- Bir hata çıkarsa önce en alttaki **Sık karşılaşılan hatalar** bölümüne bak.

**Denenen sistem:**

| Ne | Sürüm |
|---|---|
| Windows | Windows 11 Home |
| WSL | 3.0.5.0 (WSL 2) |
| Ubuntu | 26.04.1 LTS |
| ArduPilot | `master` dalı, commit `20ed31186c` (13 Kasım 2026), ArduCopter V4.8.0-dev |
| Python (ArduPilot ortamı) | 3.14.4 |
| MAVProxy | 1.8.75 |
| pymavlink | 2.4.50 |
| Mission Planner | 1.3.83 |

## Gerekenler

- **Windows 11** (ya da güncel bir Windows 10) yüklü bir bilgisayar.
- **Yönetici yetkisi:** WSL kurulumu için PowerShell'i "Yönetici olarak çalıştır" ile açabilmen gerekiyor. Okul ya da iş bilgisayarında bu yetki genelde olmaz.
- **En az 15 GB boş disk alanı.** ArduPilot klasörü yaklaşık 2,3 GB, ArduPilot'un Python ortamı yaklaşık 1,8 GB yer kaplıyor. Buna Ubuntu ve Mission Planner da ekleniyor.
- **İyi bir internet bağlantısı.** Birkaç GB indirilecek.
- **2–3 saat zaman.** En uzun süren adım ArduPilot'un gerekli programlarını kurmak (30–60 dakika ya da daha fazla).
- **Kurulum boyunca bilgisayarın başında ol.** Kurulum ortasında şifre sorabilir. Cevap vermezsen birkaç dakika sonra durur (bkz. Sık karşılaşılan hatalar).
- **Dizüstü bilgisayarsan şarja tak** ve uyku moduna geçmesini engelle. Uyku modunda kurulum durur.

## WSL kurulumu

WSL (Windows Subsystem for Linux), Windows'un içinde Linux çalıştırmanı sağlar. ArduPilot SITL, Linux'ta (Ubuntu) çalışacak.

### Adım 1: WSL'yi kur

1. Başlat menüsüne **PowerShell** yaz.
2. Çıkan sonuca **sağ tıkla** → **Yönetici olarak çalıştır**.
3. Şu komutu yaz:

```powershell
wsl --install
```

4. Kurulum bitince **bilgisayarı yeniden başlat**.

### Adım 2: Ubuntu'yu kur

Yeniden başlattıktan sonra PowerShell'i yine **Yönetici olarak** aç ve şunu yaz:

```powershell
wsl --install -d Ubuntu
```

`-d Ubuntu`, "Ubuntu dağıtımını kur" demek.

**Doğru gittiyse** ekranda sırayla şunları görürsün:

```
Downloading: Ubuntu
Installing: Ubuntu
Distribution successfully installed.
Launching Ubuntu...
```

### Adım 3: Ubuntu kullanıcını oluştur

Ubuntu ilk açılışta seninle bu pencerede konuşur:

1. `Create a default Unix user account:` → bir kullanıcı adı yaz: **küçük harf, boşluksuz, Türkçe karakter olmadan** (örneğin `ahmet`). **Enter**'a bas.
2. `New password:` → bir şifre yaz. **Yazarken ekranda hiçbir şey görünmez, yıldız bile çıkmaz. Bu normal.** Enter'a bas.
3. `Retype new password:` → aynı şifreyi tekrar yaz, Enter'a bas.
4. Ubuntu, anonim kullanım verisi göndermek isteyip istemediğini sorar (`[Y/n/e]`). `y` ya da `n` yaz ve **Enter**'a bas. İkisi de olur.

**Bu şifreyi unutma.** Program kurarken sık sık soracak.

**Doğru gittiyse** şuna benzer yeşil-mavi bir satır görürsün:

```
kullanici@bilgisayar-adi:~$
```

Buna **komut istemi** denir. Linux, komut yazmanı bekliyor demektir.

### Adım 4: Kontrol et

Windows'ta (yönetici olmayan) bir PowerShell aç ve şunu yaz:

```powershell
wsl -l -v
```

**Doğru gittiyse:**

```
  NAME      STATE      VERSION
* Ubuntu    Running    2
```

`VERSION` sütununda **2** yazmalı.

### Adım 5: Ubuntu'yu güncelle

Bundan sonra Ubuntu'yu her zaman **Başlat menüsüne "Ubuntu" yazarak** aç. Böyle açınca doğru klasörde (ev klasörün, `~`) başlar.

Ubuntu terminalinde şunu yaz:

```bash
sudo apt update && sudo apt upgrade -y
```

- `sudo`: komutu yönetici yetkisiyle çalıştırır. Ubuntu şifreni sorar.
- `apt update`: program listesini yeniler. `apt upgrade -y`: kurulu programları günceller.

**Doğru gittiyse:** birkaç dakika satırlar akar, sonunda komut istemi (`kullanici@...:~$`) geri gelir ve kırmızı `E:` ile başlayan hata satırı olmaz.

## ArduPilot'u indirme ve kurma

Bu bölümdeki bütün komutlar **Ubuntu terminalinde** yazılır.

### Adım 1: Ev klasörüne git

```bash
cd ~
pwd
```

**Doğru gittiyse:** `/home/kullanici`

### Adım 2: ArduPilot'u indir

```bash
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
```

- `git clone`: GitHub'daki ArduPilot kodunu bilgisayarına kopyalar.
- `--recurse-submodules`: ArduPilot'un içinde kullandığı başka kod paketlerini de indirir. **Bunu yazmazsan kod eksik iner.**

5–15 dakika sürebilir.

**Doğru gittiyse:** `Cloning into 'ardupilot'...` ile başlar, yüzdeli satırlar akar, sonunda komut istemi geri gelir.

### Adım 3: Denenmiş sürüme geç

ArduPilot'un kodu her gün değişiyor. Bu rehberde denenen sürümün aynısını kullanmak için:

```bash
cd ~/ardupilot
git checkout 20ed31186c
git submodule update --init --recursive
```

- `git checkout 20ed31186c`: kodu, bu rehberin denendiği güne (13 Kasım 2026) geri alır.
- `git submodule update ...`: iç kod paketlerini de o sürüme eşitler.

**Doğru gittiyse:** `HEAD is now at 20ed31186c Blimp: avoid including AP_InertialSensor.h in headers` yazar. (`detached HEAD` uyarısı da çıkabilir, bu normal.)

### Adım 4: Gerekli programları kur

`~/ardupilot` klasöründeyken:

```bash
Tools/environment_install/install-prereqs-ubuntu.sh -y
```

- Bu, ArduPilot'un hazır kurulum betiği. Derleyici, Python kütüphaneleri, harita aracı gibi onlarca programı kurar.
- `-y`: kurulumdaki bütün "devam edeyim mi?" sorularına otomatik "evet" der.
- Başta Ubuntu şifreni sorar.

**Bu adım 30–60 dakika ya da daha uzun sürebilir.** Özellikle `Building wheel for wxpython (pyproject.toml) ... |` satırında uzun süre (30–60 dakika) hiçbir şey yazılmadan bekler. **Donmadı, çalışıyor.** Pencereyi kapatma, Ctrl+C'ye basma, bilgisayarın başından ayrılma (şifre tekrar sorulabilir).

**Doğru gittiyse:** en son satır şudur:

```
---------- Tools/environment_install/install-prereqs-ubuntu.sh end ----------
```

### Adım 5: Terminali yenile

```bash
source ~/.profile
```

Kurulum betiği, ayar dosyana ArduPilot'un yerini ekledi. Bu komut o ayarları şu an açık olan terminale yükler. (Terminali kapatıp açmak da aynı işi yapar.)

**Doğru gittiyse:** komut isteminin başına `(venv-ardupilot)` gelir:

```
(venv-ardupilot) kullanici@bilgisayar-adi:~/ardupilot$
```

Bu, ArduPilot'un Python ortamının açık olduğunu gösterir. Bundan sonra Ubuntu'yu her açışında bu yazıyı görmelisin.

### Adım 6: Kontrol et

```bash
which sim_vehicle.py
```

**Doğru gittiyse:** `/home/kullanici/ardupilot/Tools/autotest/sim_vehicle.py`

## SITL'yi başlatma

### İlk çalıştırma

```bash
cd ~/ardupilot
sim_vehicle.py -v ArduCopter --console --map -w
```

- `-v ArduCopter`: çok rotorlu İHA (drone) simüle et.
- `--console`: İHA'nın durum panelini aç.
- `--map`: haritayı aç.
- `-w`: ayarları sıfırla. **Yalnızca ilk çalıştırmada** yazılır.

İlk çalıştırmada ArduCopter derlenir. Ekranda `[123/1429] Compiling ...` gibi satırlar akar (denenen bilgisayarda 2,5 dakika sürdü).

**Doğru gittiyse:**

1. Terminalde `'build' finished successfully` yazar.
2. Üç pencere açılır: **ArduCopter** (beyaz, simülatörün kendisi — kapatma), **Console** ve **Map**. Harita Avustralya'nın Canberra şehrini gösterir; bu normal.
3. Terminalde `STABILIZE>` yazısı belirir. Bu, **MAVProxy** adlı yer kontrol programının komut istemidir. Burada yazdığın komutlar İHA'ya gider.
4. Yaklaşık bir dakika sonra Console penceresinde yeşil `AP: EKF3 IMU0 is using GPS` satırı çıkar. İHA uçmaya hazırdır.

Terminalde `Failed to download /SRTM3/...` hatası çıkabilir. **Önemsiz**, görmezden gel (bkz. Sık karşılaşılan hatalar).

### Sonraki çalıştırmalar

Ubuntu'yu aç ve:

```bash
cd ~/ardupilot
sim_vehicle.py -v ArduCopter --console --map
```

Bu sefer `-w` yok. Derleme de tekrarlanmaz; birkaç saniyede açılır.

### İlk test uçuşu (MAVProxy ile)

Console'da `EKF3 IMU0 is using GPS` satırını gördükten sonra, `STABILIZE>` istemine şu komutları sırayla yaz:

```
mode guided
arm throttle
takeoff 10
```

- `mode guided`: İHA'yı komutla yönetilen moda alır. İstem `GUIDED>` olur.
- `arm throttle`: motorları çalıştırır.
- `takeoff 10`: 10 metreye kalkar.

**`arm throttle` ile `takeoff 10` arasında 10 saniyeden fazla bekleme.** Beklersen İHA güvenlik için motorları kendiliğinden kapatır; o zaman `arm throttle`'dan tekrar başla.

**Doğru gittiyse:** Console'da `ARMED` yazar, `Alt` değeri 10'a doğru yükselir.

İndirmek için:

```
mode land
```

**Doğru gittiyse:** Console'da `AP: SIM Hit ground at 0.5 m/s` ve birkaç saniye sonra `AP: Disarming motors` yazar.

### Kapatma

1. Simülatörün terminalinde **Ctrl+C**'ye bas. Pencereler kapanır.
2. `exit` yaz, terminal kapanır.
3. (İsteğe bağlı) Windows PowerShell'de `wsl --shutdown` yazarsan Linux tamamen durur ve bellek boşalır. Dosyaların silinmez.

## Mission Planner'ı SITL'ye bağlama

Mission Planner, Windows'ta çalışan bir **yer kontrol istasyonu** programı. Haritada İHA'yı gösterir, tıklayarak görev çizmeni sağlar.

### Adım 1: Mission Planner'ı kur

1. Tarayıcıda şu adrese git: https://firmware.ardupilot.org/Tools/MissionPlanner/
2. **`MissionPlanner-latest.msi`** dosyasını indir.
3. İndirilen dosyayı çalıştır, kurulumu varsayılan ayarlarla bitir (sürücü kurmak isterse **Yükle** de).
4. Kurulumdan sonra `.msi` dosyasını silebilirsin. **Proje klasörüne indirdiysen mutlaka sil**; 120 MB'lık bu dosya GitHub'a yüklenemez.

### Adım 2: Simülatörü başlat

Önceki bölümdeki gibi simülatörü başlat ve `EKF3 IMU0 is using GPS` satırını bekle.

### Adım 3: Mission Planner'ı aç

İlk açılışta çıkabilecek pencereler:

- **Altitude Angel Plugin** → **No**. (Hesap açmayı gerektiren bir harita hizmeti; simülasyonda gerekmez.)
- **Windows Güvenlik Duvarı** izin isterse → **İzin ver (Allow)**. **İptal etme.** İptal edersen Windows bağlantıyı engeller (bkz. Sık karşılaşılan hatalar).

### Adım 4: Bağlan

1. Sağ üstte, **CONNECT** düğmesinin solundaki iki kutuyu **UDP** ve **115200** yap.
2. **CONNECT**'e bas.
3. Port sorarsa **14550** yaz → **OK**.

Neden 14550? Simülatör başlarken terminalde `"--out" "X.X.X.1:14550"` gibi bir satır yazar. Simülatör İHA verilerini Windows'a bu porttan gönderir.

**Doğru gittiyse:**

- CONNECT düğmesi yeşil olur ve **DISCONNECT** yazar.
- Pencere başlığında `ArduCopter V4.8.0-dev` yazar.
- **Getting Params** penceresi açılır (İHA'nın 1400'den fazla ayarı iniyor). **Cancel'a basma**, bitmesini bekle.
- Harita Canberra'ya kayar, İHA simgesi görünür. Sol alttaki `Sats` değeri 10 civarında olur.

## İlk görev (kalkış, rota, iniş)

Bu bölümde haritaya tıklayarak bir görev çizecek ve İHA'nın onu **kendi başına (AUTO modunda)** uçmasını sağlayacaksın.

### Adım 1: Bir ayarı değiştir (yalnızca bir kez)

ArduCopter, AUTO modunda kalkış için normalde pilotun kumandadaki gaz kolunu kaldırmasını bekler. Simülasyonda kumanda olmadığı için bu bekleme kapatılır.

1. Mission Planner'da üst menüden **CONFIG** → soldan **Full Parameter List**.
2. Sağdaki arama kutusuna **`AUTO_OPTIONS`** yaz.
3. **Value** sütununa **`2`** yaz.
4. Sağdaki **Write Params**'a bas.

(`2` = "AUTO kalkışında gaz kolunu bekleme". Bu ayar İHA'nın belleğinde kalır; simülatörü `-w` ile başlatmadıkça tekrar yapman gerekmez.)

### Adım 2: Görevi çiz

1. Üst menüden **PLAN**.
2. Haritanın altındaki **Default Alt** kutusunu **`20`** yap (her nokta 20 metrede uçulur).
3. Haritada İHA'nın yakınına, birbirinden 50–100 metre uzağa **3 kez tıkla**. Alttaki tabloya 3 `WAYPOINT` satırı eklenir.
4. Tablonun **1. satırında** `WAYPOINT` yazan kutuya tıkla → **`TAKEOFF`** seç. Bu satırın **Alt** değeri `20` olmalı.
5. Haritada bir kez daha tıkla. Yeni satırın komutunu **`RETURN_TO_LAUNCH`** yap ("eve dön ve in"). **Bu satır görevin son satırı olmalı.**
6. Sağdaki **Home Location** bölümünde **Lat** ve **Long** kutuları boşsa, mavi **Home Location** yazısına tıkla. Kutular İHA'nın konumuyla dolar (yaklaşık `-35.36`, `149.16`). Rakım (**ASL**) sorarsa **`584`** yaz (Canberra'daki simülasyon kalkış noktasının rakımı).

Tablo şöyle olmalı:

```
1  TAKEOFF            Alt 20
2  WAYPOINT           Alt 20
3  WAYPOINT           Alt 20
4  RETURN_TO_LAUNCH
```

### Adım 3: Görevi İHA'ya yükle

1. Sağdaki **Write**'a bas. Hata çıkmamalı.
2. Kontrol için **Read**'e bas. "This will clear your existing points" sorusuna **OK** de. Tablo aynı satırlarla geri dolmalı. (Write yapmadan Read'e basarsan tablo boşalır.)

### Adım 4: Uçur

1. **Gaz kolunun aşağıda olduğundan emin ol.** Simülatörün terminalinde (MAVProxy istemi) şunu yaz:

```
rc 3 1000
```

(`rc 3` = kumandanın 3. kanalı, yani gaz; `1000` = en aşağı. Arm etmek için gaz en aşağıda olmalı.)

2. Mission Planner'da üst menüden **DATA** → sol alttaki **Actions** sekmesi.
3. Mod listesinden **`Guided`** seç → **Set Mode**. Sol üstteki göstergede `Guided` yazdığını **gör**.
4. **Arm/Disarm**'a bas. Göstergede `DISARMED` yazısı `ARMED` olur.
5. Mod listesinden **`Auto`** seç → **Set Mode**. **10 saniye içinde** yap.

**Do Action ve Restart Mission düğmelerine basma.** Bu görev için gerekmiyorlar; Do Action listesinde yanlış bir şey seçiliyse İHA'yı düşürebilir.

**Doğru gittiyse:** İHA 20 metreye kalkar, 2. ve 3. noktalara uçar, kalkış noktasına döner ve iner. Göstergede tekrar `DISARMED` yazar. **Messages** sekmesinde (en yeni mesaj en üstte) `Mission: 1 Takeoff`, `Mission: 2 WP`... satırlarını görürsün.

## Sık karşılaşılan hatalar

Bu hataların hepsi denenen kurulumda gerçekten yaşandı.

### Ubuntu açılmıyor, Başlat menüsünde arayınca Microsoft Store açılıyor

- **Neden:** WSL kurulu, ama içine Ubuntu kurulmamış (`wsl --status` "no installed distributions" der).
- **Çözüm:** Yönetici PowerShell'de `wsl --install -d Ubuntu`.

### Kullanıcı adını / cevabı yazdım ama hiçbir şey olmuyor

- **Neden:** Enter'a basılmadı.
- **Çözüm:** Terminalde her cevaptan sonra **Enter**'a bas.

### Ubuntu `/mnt/c/windows/system32` klasöründe açıldı

- **Neden:** Ubuntu, yönetici PowerShell'inden başlatıldı ve o pencerenin klasöründe açıldı. Bu, **Windows'un sistem klasörü**.
- **Çözüm:** `cd ~` yaz. Bu klasörde dosya oluşturma ya da silme komutu (özellikle `rm`) **çalıştırma**. Ubuntu'yu bundan sonra Başlat menüsünden aç.

### Kurulum `Building wheel for wxpython` satırında takıldı

- **Neden:** wxPython kütüphanesi bilgisayarında sıfırdan derleniyor (Ubuntu 26.04 için hazır paketi yok). 30–60 dakika ya da daha uzun sürer.
- **Kontrol:** Satır sonundaki `|` işareti dönüyorsa (`| / - \`) çalışıyor. Görev Yöneticisi'nde (Ctrl+Shift+Esc) **VmmemWSL** işleminin işlemci kullanımı yüksekse çalışıyor.
- **Çözüm:** Bekle. 15–20 dakika boyunca işaret dönmüyor ve işlemci kullanımı %0'a yakınsa yardım iste.

### Kurulum `sudo: timed out` ile durdu

- **Neden:** `sudo` şifreyi yaklaşık 15 dakika hatırlar. Uzun bir adımdan sonra şifreyi tekrar sordu, cevap gelmeyince vazgeçti.
- **Çözüm:** Aynı kurulum komutunu tekrar çalıştır. Önceden kurulanları atlar:

```bash
cd ~/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
```

Bu sefer bilgisayarın başında kal.

### Terminalde `Failed to download /SRTM3/filelist_python ...` hatası

- **Neden:** MAVProxy, haritaya arazi yüksekliği verisi indiremedi.
- **Çözüm:** Gerek yok. Uçuşu etkilemez.

### Mission Planner: `Connect Failed`

- **Neden:** Windows Güvenlik Duvarı'nda Mission Planner için "Engelle" kuralları oluşmuş (ilk açılıştaki izin penceresi iptal edildiyse olur).
- **Kontrol:** Normal PowerShell'de:

```powershell
Get-NetFirewallRule -DisplayName "Mission Planner" | Select-Object DisplayName, Action
```

`Action` sütununda `Block` görüyorsan sorun budur.

- **Çözüm:**
  1. Mission Planner'ı kapat.
  2. WSL'nin ağ adresini öğren (normal PowerShell):

     ```powershell
     Get-NetIPAddress -InterfaceAlias "vEthernet (WSL*" -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength
     ```

     Denenen bilgisayarda sonuç `192.168.80.1` ve `20` idi; bu, `192.168.80.0/20` ağı demek. Seninki farklı olabilir.
  3. **Yönetici** PowerShell'de engelleme kurallarını sil ve yalnızca WSL'den gelen veriye izin veren bir kural ekle (ikinci komut tek satırdır; `192.168.80.0/20` yerine kendi ağını yaz):

     ```powershell
     Remove-NetFirewallRule -DisplayName "Mission Planner"
     New-NetFirewallRule -DisplayName "Mission Planner (WSL SITL)" -Direction Inbound -Program "C:\Program Files (x86)\Mission Planner\MissionPlanner.exe" -Protocol UDP -LocalPort 14550 -RemoteAddress 192.168.80.0/20 -Action Allow
     ```

  4. Mission Planner'ı aç ve tekrar bağlan.

### Mission Planner: `Your home location is invalid`

- **Neden:** Home Location bölümünde Lat ve Long boş.
- **Çözüm:** PLAN ekranında sağdaki mavi **Home Location** yazısına tıkla.

### `Arm: Auto mode not armable`

- **Neden:** ArduCopter güvenlik için AUTO modunda arm etmeye izin vermez.
- **Çözüm:** Önce **Guided** modunda arm et, sonra **Auto**'ya geç.

### `Arm: Throttle (RC3) is not neutral`

- **Neden:** Gaz kolu en aşağıda değil.
- **Çözüm:** MAVProxy istemine `rc 3 1000` yaz, sonra tekrar arm et.

### Arm oluyor, görev başlıyor (`Mission: 1 Takeoff`) ama İHA kalkmıyor; 10 saniye sonra `Disarming motors`

- **Neden:** AUTO kalkışı, gaz kolunun kaldırılmasını bekliyor.
- **Çözüm:** `AUTO_OPTIONS` ayarını `2` yap (İlk görev → Adım 1).

### İHA kalkıp birkaç saniye sonra hızla alçaldı ve yere çarptı (`SIM Hit ground at 1.9 m/s`)

- **Neden:** Actions sekmesindeki **Do Action** düğmesine basıldı ve listede **Loiter** seçiliydi. İHA LOITER moduna geçti. LOITER'da gaz kolu tırmanma hızını belirler; gaz en aşağıdaysa İHA en hızlı şekilde alçalır.
- **Çözüm:** Do Action'ı kullanma. Bir düğmeye basmadan önce seçili olanı **her zaman** kontrol et; her mod değişikliğinden sonra göstergedeki mod adına bak.

### `Arm failed ... Do you wish to Force Arm?`

- **Çözüm:** **Cancel**. **Force Arm'a asla basma.** Güvenlik kontrollerini atlar; gerçek bir İHA'da kazaya ve yaralanmaya yol açabilir. Bunun yerine **Messages** sekmesinde arm'ın neden reddedildiğini oku ve yukarıdaki hatalardan uygun olanı bul.

### Simülatörü yeniden başlattım, eski ayarlarım gitti

- Simülatör yeniden başlayınca **MAVProxy'de yazdığın komutlar** (örneğin `rc 3 1000`) sıfırlanır; gerekirse tekrar yaz.
- **Görev ve `AUTO_OPTIONS` gibi parametreler kaybolmaz.** İHA'nın belleğinde kalırlar (simülatörü `-w` ile başlatmadıkça).
