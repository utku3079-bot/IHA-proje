# ARGUS Panel ↔ İHA mesaj formatı

**Sürüm:** 0.1 (taslak), 28 Kasım 2026
**Durum:** Görev paneli v1 (Kademe 1) için. Değişiklikler bu dosyada, sürüm numarası artırılarak yapılır.

Bu belge, stok sahası yönetim paneli ile İHA'daki görev programının birbirine hangi mesajları, hangi biçimde gönderdiğini tanımlar. Panel ve görev programı farklı kişiler tarafından yazılsa bile bu belgeye uyduğu sürece birlikte çalışmalıdır.

## 1. Genel yapı

```
Panel (dizüstü bilgisayar)  ──UDP / JSON──►  Görev programı  ──MAVLink──►  ArduPilot
                            ◄─────────────   (şimdi dizüstü,  ◄──────────
                                              ileride Raspberry Pi)
```

- Panel **MAVLink konuşmaz**. İHA'yı doğrudan yönetmez; yalnızca görev verir ve durum alır.
- İHA'yı yöneten tek program görev programıdır (bugünkü `gorev.py`'nin gelişmiş hali). Güvenlik kararları (RTL, iniş) orada verilir.
- Böylece panel çökse ya da bağlantı kopsa bile İHA'nın davranışı görev programının ve ArduPilot'un kontrolünde kalır.

## 2. Taşıma

| | Değer |
|---|---|
| Protokol | UDP |
| Görev programının dinlediği port | **15001** |
| Panelin dinlediği port | **15000** |
| Adres (v1) | `127.0.0.1` (ikisi aynı bilgisayarda) |
| Kodlama | UTF-8 JSON, **bir UDP paketi = bir mesaj** |
| En büyük mesaj | 1 KB |

Portlar, SITL'in kullandığı 14550–14552 ile çakışmaması için seçildi.

UDP paketleri kaybolabilir. Bu yüzden:
- Panel bir **görev** gönderdikten sonra **2 saniye** içinde aynı `gorev_id`'li bir **durum** mesajı (aşama `gorev_alindi`) gelmezse görevi tekrar gönderir; en fazla 3 kez.
- Görev programı aynı `gorev_id`'yi ikinci kez alırsa görevi yeniden başlatmaz, yalnızca son durumunu tekrar gönderir.
- Durum mesajları düzenli aralıkla gönderildiği için birinin kaybolması sorun değildir.

## 3. Ortak alanlar

Her mesajda bulunur:

| Alan | Tür | Açıklama |
|---|---|---|
| `surum` | sayı | Bu belgenin ana sürümü. Şimdilik `0`. Farklı sürümdeki mesaj reddedilir. |
| `tip` | yazı | `gorev`, `durum`, `sonuc` ya da `hata` |
| `gorev_id` | yazı | Paneldeki görevin kimliği, örn. `"G-0001"`. Panel üretir; bir oturumda tekrar etmez. |
| `zaman` | sayı | Gönderilme anı, Unix zamanı (saniye, `time.time()`) |

**Birimler:** Koordinatlar **derece** (×10⁷ değil), irtifa ve mesafe **metre**, gerilim **volt**, süre **saniye**. İrtifa kalkış noktasına göredir.

## 4. Mesaj türleri

### 4.1 `gorev`: Panel → İHA

"Şu kutu şu konumda mı, git bak."

| Alan | Tür | Zorunlu | Açıklama |
|---|---|---|---|
| `kutu` | yazı | evet | Kutu kodu, örn. `"P-102"` |
| `konum_adi` | yazı | evet | Saha konumu, örn. `"A-3"` |
| `enlem`, `boylam` | sayı | evet | Konumun koordinatı (derece) |
| `aruco_id` | sayı | evet | Kutunun üstünde olması beklenen işaretin kimliği (Kademe 2'de kullanılır) |
| `irtifa` | sayı | hayır | Uçuş irtifası, verilmezse 20 m |

```json
{"surum": 0, "tip": "gorev", "gorev_id": "G-0001", "zaman": 1764331200.0,
 "kutu": "P-102", "konum_adi": "A-3", "enlem": -35.3628127, "boylam": 149.1652379,
 "aruco_id": 102, "irtifa": 20}
```

### 4.2 `durum`: İHA → Panel

Görev boyunca **her saniye** ve her aşama değişiminde gönderilir.

| Alan | Tür | Açıklama |
|---|---|---|
| `asama` | yazı | Aşağıdaki listeden biri |
| `enlem`, `boylam`, `irtifa` | sayı | İHA'nın o anki konumu |
| `hedefe_mesafe` | sayı | Hedefe yatay mesafe (m) |
| `batarya_v` | sayı | Batarya gerilimi (V) |

`asama` değerleri, sırasıyla:

| Değer | Anlamı |
|---|---|
| `gorev_alindi` | Görev alındı ve kabul edildi (panelin beklediği onay) |
| `kalkis` | Arm edildi, kalkıyor |
| `yolda` | Hedefe gidiyor |
| `hedefte` | Hedefe vardı, bekliyor / fotoğraf çekiyor |
| `arama` | Kutu yerinde değil, çevrede arıyor (Kademe 2) |
| `inis` | İniyor |
| `tamamlandi` | Yere indi, motorlar disarm; görev bitti |

```json
{"surum": 0, "tip": "durum", "gorev_id": "G-0001", "zaman": 1764331215.4,
 "asama": "yolda", "enlem": -35.3630102, "boylam": 149.1652380, "irtifa": 19.8,
 "hedefe_mesafe": 22.5, "batarya_v": 12.31}
```

### 4.3 `sonuc`: İHA → Panel

Hedefte iş bitince **bir kez** gönderilir (panel `durum` ile almadıysa son durumla birlikte tekrar istenebilir, bkz. Açık sorular).

| Alan | Tür | Açıklama |
|---|---|---|
| `sonuc` | yazı | `bulundu`, `yanlis_yerde`, `bulunamadi` ya da `foto_cekildi` |
| `okunan_aruco_id` | sayı ya da `null` | Kamerada okunan işaret; okunamadıysa `null` |
| `enlem`, `boylam` | sayı | Fotoğrafın çekildiği konum |
| `foto` | yazı | Fotoğraf dosyasının adı, örn. `"G-0001_A-3.jpg"` |

- `bulundu`: Beklenen işaret beklenen konumda okundu.
- `yanlis_yerde`: Konumda **başka** bir işaret okundu.
- `bulunamadi`: Konumda (ve aramada) işaret okunamadı.
- `foto_cekildi`: **Kademe 1** sonucu. İHA henüz işaret okumuyor; yalnızca fotoğraf çekti, kararı panel/insan verir.

```json
{"surum": 0, "tip": "sonuc", "gorev_id": "G-0001", "zaman": 1764331240.2,
 "sonuc": "foto_cekildi", "okunan_aruco_id": null,
 "enlem": -35.3628125, "boylam": 149.1652378, "foto": "G-0001_A-3.jpg"}
```

### 4.4 `hata`: İHA → Panel

Görev kabul edilmediğinde ya da yarıda kaldığında gönderilir.

| Alan | Tür | Açıklama |
|---|---|---|
| `neden` | yazı | İnsanın okuyacağı açıklama, örn. `"Arm reddedildi (result=4)"` |
| `eylem` | yazı | İHA'nın yaptığı: `RTL`, `LAND` ya da `yok` (yerdeyken) |

```json
{"surum": 0, "tip": "hata", "gorev_id": "G-0001", "zaman": 1764331203.1,
 "neden": "Mesgul: G-0000 devam ediyor", "eylem": "yok"}
```

## 5. Kurallar

1. Aynı anda **tek görev** yürütülür. Görev sürerken yeni bir `gorev_id` gelirse görev programı `hata` döndürür (`"Mesgul"`, eylem `yok`) ve eski göreve devam eder.
2. Görev programı eksik ya da hatalı alanlı bir `gorev`i uçmadan reddeder (`hata`, eylem `yok`).
3. Görev programı her `hata` sonrası görevi bitmiş sayar; panel yeni görev verebilir.
4. Panel **durum** mesajı 5 saniye boyunca gelmezse bağlantıyı "kopuk" gösterir. İHA tarafında ne olacağına görev programı ve ArduPilot'un failsafe ayarları karar verir; panel bir şey yapmaz.

## 6. Açık sorular

Henüz karar verilmedi; v1 kodu yazılırken netleşecek:

- **Fotoğrafın aktarımı:** Şimdilik yalnızca dosya adı gidiyor. Dosya panele nasıl taşınacak (ortak klasör, ayrı aktarım, uçuş sonrası kopyalama)?
- **Yarışmadaki bağlantı:** Panel ile Raspberry Pi arasında hangi donanım (Wi-Fi, telemetri modemi)? Menzil ve hız mesaj boyutunu etkiler.
- **Güvenlik:** Aynı ağdaki herkes `gorev` gönderebilir. Basit bir anahtar/şifre alanı gerekli mi?
- **Arama:** `arama` aşamasının alanı, deseni ve süresi (Kademe 2).
- **Kayıp sonuç:** `sonuc` mesajı kaybolursa panel nasıl yeniden ister?
