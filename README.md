# ARGUS — İHA uçuş yazılımı

TEKNOFEST Liseler Arası İHA Yarışması 2027 (Serbest Görev) için döner kanatlı bir İHA'nın yazılımını geliştiriyoruz. ARGUS, projenin çalışma adı. Uçuş kontrolcüsü ArduPilot (Copter); betikler Python ve [pymavlink](https://github.com/ArduPilot/pymavlink) ile yazılıyor ve şimdilik bilgisayarda simüle edilen bir İHA (SITL) üzerinde deneniyor.

> **Güvenlik:** Komut gönderen betikler (şu an `komut_gonder.py`) gerçek bir İHA'da, pervaneler takılıyken ve pilot hazır değilken **asla** çalıştırılmaz.

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
   python komut_gonder.py
   ```

Aynı portu dinleyen iki betik aynı anda çalışamaz (aşağıdaki tabloda hangi betiğin hangi portu kullandığı yazıyor).

## Dosyalar

| Dosya | Port | Ne yapar |
|---|---|---|
| `ilk_baglanti.py` | 14551 | İHA'ya bağlanır ve ilk HEARTBEAT mesajını ekrana basar. Bağlantının çalıştığını denemenin en kısa yolu. |
| `irtifa_oku.py` | 14551 | GLOBAL_POSITION_INT mesajını sürekli okuyup enlem, boylam ve irtifayı (metre) yazdırır. Çıkmak için Ctrl+C. |
| `arm_durumu.py` | 14551 | HEARTBEAT'teki `base_mode` alanının 128 bitine bakarak İHA'nın `ARMED` mı `DISARMED` mı olduğunu sürekli yazdırır. Komut gönderen bir betiği denerken ikinci pencerede açık tutmak için. |
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
