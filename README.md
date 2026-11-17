Bu projede TEKNOFEST icin IHA alaninda lise kategorisinde doner kanatli bir insansiz hava aracinin ilgili kodlarini yazacagim.
1. Asamada değişkenler ve veri tipleri, aritmetik, input/print, if-else, for ve while döngüleri, listeler, fonksiyonlar, sözlükler, dosya okuma/yazma konularini ogrendim.
Ilk denemelerimde kimi zaman cesitli kodlari calistiramadim veya hata verdi, ancak kisa bir sure icerisinde butun 1. Asama egitimimi tamamladim.
Öğrendiklerim:

WSL ile Windows'un içinde Linux çalıştırmak.
sudo, apt, git clone --recurse-submodules komutları.
Python sanal ortamı (venv-ardupilot).
SITL'yi sim_vehicle.py ile başlatmak.
Çalışmayanlar:

WSL kuruldu ama içine Ubuntu kurulmamıştı.
Ubuntu, Windows'un sistem klasöründe (system32) açıldı.
wxPython 30–60 dakika derlendi, donmuş sandın.
Kurulum ortasında sudo şifre zaman aşımına uğradı.
2. Mission Planner ve AUTO görevi
Öğrendiklerim:

UDP 14550 ile bağlanmak.
Haritada görev çizmek: TAKEOFF, WAYPOINT, DO_SET_SERVO, DELAY, RTL.
Servo 9: 1100 kapalı, 1900 açık.
Çalışmayanlar:

Connect Failed: Windows güvenlik duvarı bağlantıyı engelledi.
Home location invalid hatası.
Auto mode not armable: Önce GUIDED'da arm edip sonra AUTO'ya geçmek gerekiyor.
Throttle not neutral: rc 3 1000 gerekti.
İHA AUTO'da kalkmadı: AUTO_OPTIONS = 2 gerekti.
Do Action ile yanlışlıkla LOITER seçildi ve İHA yere çarptı
3. İlk pymavlink betikleri
Öğrendiklerim:

mavlink_connection, wait_heartbeat, recv_match.
GLOBAL_POSITION_INT ile enlem, boylam ve irtifa okumak. Birimler: 1e7 ve milimetre.
Çalışmayan:

Betik wait_heartbeat'te takıldı, çünkü simülatör 14551 portuna veri göndermiyordu. --out 127.0.0.1:14551 gerekti.
4. Arm durumu: arm_durumu.py
Öğrendiklerim:

base_mode ve bit maskesi.
& işlemi, bin().
128 = armed, 8 = GUIDED. Kendi ölçümün: 81 → 217.
Çalışmayanlar:

MAV_MODE_FLAG_SAFETY_ARMED için NameError.
Commit'ten önce test etmeden göndermek.
5. Komut gönderme 
Öğrendiklerim:

set_mode.
COMMAND_LONG ve 11 parametresi, parametre sırasının önemi.
Çalışmayanlar:

wait_heartbeat olmadan komut gönderildi ve hiçbir yere ulaşmadı.
İki betik aynı portu dinledi, ikinci port (14552) gerekti.
6. COMMAND_ACK
Öğrendiklerim:

Her komutun bir cevabı vardır.
command ve result alanları.
blocking=True ve type=.
Print ile hata ayıklamak.
Çalışmayanlar:

blocking olmadan okuyunca None geldi.
İlk gelen ACK set_mode'a aitti (176), arm'ın cevabı (400) değildi.
and kullanılan koşul yüzünden ret durumunda döngü sonsuza kadar döndü.
Kütüphane sabitinin üzerine yazıldı (= 400).
7. Kalkış ve iniş
Öğrendiklerim:

MAV_CMD_NAV_TAKEOFF (p7 = irtifa).
LAND modu.
Çalışmayanlar:

İrtifa bir kez okundu ve hiç güncellenmedi ("fotoğraf").
Birim karışıklığı (mm ile m).
== kullanılınca eşik hiç yakalanmadı.
Fazladan ve yanlış girintili break.
8. Yük bırakma
Öğrendiklerim:

DO_SET_SERVO.
SERVO_OUTPUT_RAW ile servonun döndüğünü doğrulamak.
time.sleep.
break sadece en yakın döngüden çıkar.
Çalışmayanlar:

İki ayrı if yüzünden yük tekrar tekrar bırakıldı.
blocking=1900 yazıldı.
İlk gelen SERVO_OUTPUT_RAW mesajı eskiydi.
İHA önceki uçuştan armed kaldı ve kalkış reddedildi. Nedeni mav.tlog kaydından bulundu.
9. Hata durumları ve branch
Öğrendiklerim:

Kalkış ACK'ini kontrol etmek.
timeout ve is None.
sys.exit.
git switch -c, merge, fast-forward.
Çalışmayanlar:

"Cevap bana ait değil" durumu "reddedildi" sanıldı.
Örnek kod olduğu gibi kopyalandı (sonuc = None).
break'ten sonra yazılan sys.exit hiç çalışmadı.