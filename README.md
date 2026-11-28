# ARGUS — İHA uçuş yazılımı

TEKNOFEST Liseler Arası İHA Yarışması 2027 (Serbest Görev) için döner kanatlı bir İHA'nın yazılımını geliştiriyoruz. ARGUS, projenin çalışma adı. Uçuş kontrolcüsü ArduPilot (Copter); betikler Python ve [pymavlink](https://github.com/ArduPilot/pymavlink) ile yazılıyor ve şimdilik bilgisayarda simüle edilen bir İHA (SITL) üzerinde deneniyor.

> **Güvenlik:** Komut gönderen betikler (şu an `gorev.py` ve `komut_gonder.py`) gerçek bir İHA'da, pervaneler takılıyken ve pilot hazır değilken **asla** çalıştırılmaz.

## Hızlı başlangıç

Kurulum (WSL, Ubuntu, ArduPilot, Mission Planner) adım adım [REHBER_SITL.md](REHBER_SITL.md) dosyasında.

Kurulumdan sonra:

1. Bir Ubuntu terminalinde simülatörü başlat. Betikler 14551 ve 14552 portlarını dinlediği için iki `--out` gerekli:

   ```bash
   cd ~/ardupilot
   sim_vehicle.py -v ArduCopter --console --map --out 127.0.0.1:14551 --out 127.0.0.1:14552
   ```

2. Console penceresinde yeşil `EKF3 IMU0 is using GPS` satırını bekle.
3. İkinci bir Ubuntu terminalinde betiği çalıştır:

   ```bash
   cd ~/IHA-proje
   python gorev.py
   ```

Aynı portu dinleyen iki betik aynı anda çalışamaz (aşağıdaki tabloda hangi betiğin hangi portu kullandığı yazıyor).

## Dosyalar

| Dosya | Port | Ne yapar |
|---|---|---|
| `ilk_baglanti.py` | 14551 | İHA'ya bağlanır ve ilk HEARTBEAT mesajını ekrana basar. Bağlantının çalıştığını denemenin en kısa yolu. |
| `irtifa_oku.py` | 14551 | GLOBAL_POSITION_INT mesajını sürekli okuyup enlem, boylam ve irtifayı (metre) yazdırır. Çıkmak için Ctrl+C. |
| `arm_durumu.py` | 14551 | HEARTBEAT'teki `base_mode` alanının 128 bitine bakarak İHA'nın `ARMED` mı `DISARMED` mı olduğunu sürekli yazdırır. Komut gönderen bir betiği denerken ikinci pencerede açık tutmak için. |
| `gorev.py` | 14552 | **Komut gönderir. Asıl görev betiği.** GUIDED moduna geçer, arm eder, `GOREREK_IRTIFA` (20 m) yüksekliğe kalkar, `HEDEF_ENLEM`/`HEDEF_BOYLAM` koordinatına uçar (SET_POSITION_TARGET_GLOBAL_INT), hedefe `VARIS_ESIGI` kadar yaklaşınca `BEKLEME_SURESI` bekler ve orada LAND ile iner. Her komutun cevabını `ack_bekle()`, her mod değişikliğini HEARTBEAT'teki `custom_mode` ile `mod_bekle()` doğrular; bir şey ters giderse ya da 5 saniye içinde cevap gelmezse nedenini yazıp durur. Görev yarıda kalırsa (hata, Ctrl+C) `finally` bloğu İHA'yı RTL ile eve döndürür. Ayarlar dosyanın başındaki sabitlerde. |
| `konum_hesap.py` | — | İki enlem/boylam noktası arasındaki mesafeyi metre olarak hesaplayan `mesafe()` fonksiyonu ve testi. Kısa mesafeler için düz yer yaklaşımı (1° enlem ≈ 111 320 m, boylam enlemin kosinüsüyle küçülür). İHA'ya bağlanmaz. |
| `komut_gonder.py` | 14552 | **Komut gönderir.** GUIDED moduna geçer, arm eder, 20 m'ye kalkar, servo 9'u açıp 5 saniye sonra kapatır ve LAND moduyla iner. Arm ve kalkış komutlarının cevabını (COMMAND_ACK) kontrol eder, reddedilirse durur; kalkış cevabı 5 saniye içinde gelmezse de durur. Servonun konumunu SERVO_OUTPUT_RAW ile doğrular. Servo kısmı alıştırma amaçlıdır. |
| `log_analiz.py` | — | Bir uçuş kaydını (`.BIN`) okur; irtifa, batarya gerilimi ve dikey titreşim grafiklerini `irtifa.png`, `gerilim.png` ve `vibration.png` olarak kaydeder, kısa bir özet yazdırır. İHA'ya bağlanmaz. Başka bir uçuşu incelemek için dosyanın başındaki `kayit_yolu` değiştirilir; grafikler her çalıştırmada yeniden yazılır. |
| `yuk_birakma_gorevi.waypoints` | — | Mission Planner görev dosyası (PLAN → Load): kalkış, iki nokta, servo 9 ile yük bırakma, eve dönüş. Alıştırma amaçlıdır. |
| `IHA-proje.py` | — | Aşama 1'deki Python temelleri alıştırmaları. İHA'ya bağlanmaz. |
| `REHBER_SITL.md` | — | SITL ve Mission Planner kurulum rehberi (taslak; son hali 20 Aralık). |

## Aşama 1: Python temelleri

Değişkenler ve veri tipleri, aritmetik, input/print, if-else, for ve while döngüleri, listeler, fonksiyonlar, sözlükler, dosya okuma/yazma. İlk denemelerimde bazı kodları çalıştıramadım ya da hata aldım, ama kısa sürede Aşama 1'i tamamladım.

## Aşama 2: Git, SITL ve pymavlink

Git ve GitHub, WSL, ArduPilot SITL kurulumu, Mission Planner ile AUTO görevi ve İHA'yı Python'dan yöneten pymavlink betikleri.

### Ne öğrendim

- **Kurulum:** WSL ile Windows'ta Linux çalıştırmak; `sudo`, `apt`, `git clone --recurse-submodules`; Python sanal ortamı (`venv-ardupilot`); SITL'yi `sim_vehicle.py` ile başlatmak.
- **Mission Planner:** UDP 14550 ile bağlanmak; haritada görev çizmek (TAKEOFF, WAYPOINT, DO_SET_SERVO, DELAY, RTL).
- **Veri okumak:** `mavlink_connection`, `wait_heartbeat`, `recv_match`; GLOBAL_POSITION_INT'te enlem/boylamın 10⁷ ile, irtifanın milimetre cinsinden geldiği.
- **Bit maskesi:** `base_mode` tek bir sayı ama her biti ayrı bir bilgi; `&` ile tek bit okunur. Kendi ölçümüm: STABILIZE ve disarm 81, GUIDED ve arm 217 (fark 128 + 8).
- **Komut göndermek:** `set_mode`; COMMAND_LONG ve 11 parametresi (sıra önemli).
- **Cevabı kontrol etmek:** Her komutun bir COMMAND_ACK cevabı var. Önce `command` alanıyla cevabın hangi komuta ait olduğuna, sonra `result` ile kabul mü ret mi olduğuna bakmak gerekiyor. "Bu cevap benim komutuma ait değil" ile "komutum reddedildi" aynı şey değil.
- **Döngüler ve akış:** Bir değişken kendiliğinden güncellenmez, yeni değer için yeniden okumak gerekir. İlk gelen mesaj aradığım olmayabilir, aradığımı bulana kadar döngüde okurum. `break` yalnızca en yakın döngüden çıkar, `sys.exit` programı bitirir.
- **Karşılaştırma:** Ölçülen değerlerde (irtifa) `==` yerine eşik, komut değerlerinde (PWM 1900) `==`.
- **Bekleme:** Sabit bir bekleme süresi yerine `timeout` (üst sınır) ve `is None` kontrolü.
- **Hata ayıklama:** Adımların arasına `print` koymak; simülatörün `mav.tlog` kaydından gönderilen komutları ve cevapları okumak.
- **Git:** commit, push, `git switch -c` ile dal açmak, `merge` ve fast-forward.

### Ne çalışmadı

- **Kurulum:** WSL kuruldu ama içine Ubuntu kurulmamıştı. Ubuntu bir kere Windows'un `system32` klasöründe açıldı. wxPython 30–60 dakika derlendi, dondu sandım. Kurulumun ortasında `sudo` şifresi zaman aşımına uğradı.
- **Mission Planner:** Windows güvenlik duvarı bağlantıyı engelledi (`Connect Failed`). `Auto mode not armable` (önce GUIDED'da arm etmek gerekiyor), `Throttle not neutral` (`rc 3 1000`), AUTO'da kalkmama (`AUTO_OPTIONS = 2`). Do Action ile yanlışlıkla LOITER seçildi ve İHA yere çarptı.
- **Bağlantı:** Simülatör 14551'e veri göndermediği için betik `wait_heartbeat`'te takıldı. `wait_heartbeat` olmadan gönderilen komut hiçbir yere ulaşmadı. İki betik aynı portu dinleyince biri veri alamadı.
- **COMMAND_ACK:** `blocking=True` olmadan okuyunca `None` geldi. İlk gelen cevap `set_mode`'a aitti (176), arm'a (400) değil. `and` ile yazılmış koşul yüzünden ret durumunda döngü sonsuza kadar döndü.
- **Kalkış ve iniş:** İrtifayı bir kez okuyup hiç güncellemedim. Milimetreyle metreyi karıştırdım. `==` ile kurduğum eşik hiç yakalanmadı. Yanlış girintili bir `break` döngüyü tek turda bitirdi.
- **Servo:** İki ayrı `if` yüzünden servo tekrar tekrar açılıp kapandı. `blocking=1900` yazdım (`blocking` yalnızca True/False alır). İlk okunan SERVO_OUTPUT_RAW mesajı eskiydi.
- **Simülatör durumu:** Bir uçuş bitmeden betiği yeniden çalıştırınca İHA armed kaldı ve kalkış reddedildi; nedenini `mav.tlog` kaydından buldum.
- **Hata durumları:** `break`'ten sonra yazdığım `sys.exit` hiç çalışmadı.

## Aşama 2b ve görev betiği (Kasım 2026)

### Ne öğrendim

- **numpy ve matplotlib:** Listeyi `np.array` ile diziye çevirip döngüsüz hesap yapmak; `plot`, eksen isimleri, `savefig`; her grafikten önce `plt.figure()`.
- **Uçuş kaydı okumak:** `.BIN` dosyası da `mavlink_connection` ile açılır; BARO (irtifa), BAT (gerilim) ve VIBE (titreşim) mesajları. Dosya bitince `recv_match` `None` döndürür.
- **Her sensör kendi zamanıyla çizilir;** zaman mikrosaniyeden saniyeye çevrilir ve ilk değer çıkarılarak sıfırdan başlatılır.
- **Fonksiyonlar:** Tekrar eden kodu `ack_bekle(komut)` ve `mod_bekle(mod)` olarak bir kez yazıp çağırmak; parametrenin değeri çağrıldığı anda belli olur.
- **Sabitler:** Ayar sayılarını (irtifa, timeout, adres) dosyanın başında büyük harfli isimlerle tutmak; iniş eşiğini kalkış irtifasından hesaplatmak.
- **Timeout iki türlü:** `recv_match(timeout=...)` yalnızca *hiç mesaj gelmezse* işe yarar; beklenen şey hiç olmazken mesajlar gelmeye devam ediyorsa `time.time()` ile toplam süre sınırı gerekir.
- **`try/finally`:** Betik nasıl biterse bitsin (`sys.exit`, Ctrl+C) `finally` çalışır; görev yarıda kalırsa RTL. Bağlantı koparsa RTL komutu İHA'ya ulaşamaz, o durumu ArduPilot'un kendi failsafe'i karşılar.
- **Kanıt:** `mav.tlog` her simülatör açılışında sıfırlanır, `~/ardupilot/logs/*.BIN` kalıcıdır. RTL testi `00000022.BIN` kaydında görülebilir.

### Ne çalışmadı

- İlk grafiklerde zaman ekseni mikrosaniyede kaldı (`1e9`); hesabın sonucu bir değişkene atanmamıştı.
- Batarya döngüsünde `None` kontrolü alanı okuduktan sonra geldiği için dosya sonunda `AttributeError` alındı.
- Titreşim, bataryanın zaman dizisiyle çizilmeye çalışıldı: `x and y must have same first dimension`.
- Simülatördeki batarya hiç boşalmadı; `SIM_BATT_CAP_AH = 0` olduğu için kapasite sonsuz. Düşük batarya testinde değiştirilmesi gerekecek.
- Toplam süre sınırının başlangıç zamanı fonksiyonun dışında (program başında) alınınca, iniş anındaki mod kontrolü süre çoktan dolduğu için hemen başarısız oldu ve İHA LAND yerine RTL'ye geçti.

## Hedefe gitme (28 Kasım 2026)

`gorev.py` artık İHA'yı bir koordinata gönderip orada indiriyor. SITL'de kalkış noktasının 50 m kuzeyine gönderildi; İHA hedefi bir kez yaklaşık 0,7 m geçti (aşma, overshoot), sonra birkaç santimetrede durdu ve hedefin üstüne indi (kayıt: `00000024.BIN`).

### Ne öğrendim

- **Enlem/boylam → metre:** 1° enlem ≈ 111 320 m; boylamda bu değer enlemin kosinüsüyle çarpılır. Mesafe Pisagor ile bulunur. `math.cos` radyan ister.
- **Birimler:** Kodun içinde her şey derece; ×10⁷ çevrimi yalnızca İHA'ya gönderirken ve İHA'dan okurken yapılır.
- **SET_POSITION_TARGET_GLOBAL_INT:** 16 alan; `type_mask` bir bit maskesi (1 = bu alanı dikkate alma). Yalnızca konum için 3576. Bu mesaj bir komut olmadığı için COMMAND_ACK gelmez; varış konumdan anlaşılır.
- **Testin başlangıç durumu da testin parçası:** Simülatör kapatılmazsa İHA bir önceki uçuşun indiği yerden başlar.

### Ne çalışmadı

- Python'da `111.320` yüz on bir virgül üç iki demek; sonuç 1000 kat küçük çıktı. Sabit tanımlanmış ama kullanılmamıştı.
- Fonksiyonda `print` kullanınca dönen değer `None` oldu; `return` gerekiyordu.
- Kosinüs boylamdan alınmıştı; kuzey testi bunu yakalamadı, doğu testi yakalar.
- Fonksiyon çağrısının içine `HEDEF_ENLEM = ...` yazmak sözdizimi hatası verdi; zaman alanı unutulunca bütün alanlar bir sıra kaydı.
- `if mod_bekle is True` fonksiyonun kendisine baktığı için hiç doğru olmadı; görev tamamlandı sayılmadı ve iniş sonrası gereksiz RTL gönderildi.
- `VARIS_ESIGI = 0.05` SITL'de çalışıyor ama gerçek GPS'te birkaç metrelik oynama yüzünden hiç ulaşılamayabilir; gerçek uçuştan önce büyütülecek.
