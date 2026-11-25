import numpy as np
import matplotlib.pyplot as plt
from pymavlink import mavutil
kayit_yolu = "/home/adali/ardupilot/logs/00000018.BIN"
print(f"okunan kayit: {kayit_yolu}")
kayit = mavutil.mavlink_connection(kayit_yolu)
zaman_listesi = []
irtifa_listesi = []
while True :
    veri = kayit.recv_match(type="BARO")
    if veri is None :
        print("veri yok")
        break
    I_alani = veri.I
    alt_alani = veri.Alt
    timeus_alani = veri.TimeUS
    if I_alani == 0:
        zaman_listesi.append(timeus_alani)
        irtifa_listesi.append(alt_alani)
print(len(irtifa_listesi))

t_listesi_mic = np.array(zaman_listesi)
h_listesi = np.array(irtifa_listesi)
t_listesi_sec = (t_listesi_mic / 1000000 )- (zaman_listesi[0] / 1000000)
plt.plot(t_listesi_sec, h_listesi)
plt.xlabel("zaman (s)")
plt.ylabel("irtifa (m)")
plt.savefig("irtifa.png")

volt_listesi = []
bat_zaman_listesi = []
kayit_2 = mavutil.mavlink_connection(kayit_yolu)
while True:
    bat_verisi = kayit_2.recv_match(type="BAT")
    if bat_verisi is None:
        break
    bat_voltu = bat_verisi.Volt
    volt_listesi.append(bat_voltu)
    bat_zamani = bat_verisi.TimeUS
    bat_zaman_listesi.append(bat_zamani)
volt_1_listesi = np.array(volt_listesi)
bat_1_listesi = np.array(bat_zaman_listesi)
zaman_listesi_sec = (bat_1_listesi / 1000000) - (zaman_listesi[0] / 1000000)
plt.figure()
plt.plot(zaman_listesi_sec, volt_1_listesi)
plt.xlabel("zaman (s)")
plt.ylabel("Volt")
plt.savefig("gerilim.png")

zaman_vibrasyon_listesi = []
titresim_listesi = []
kayit_3 = mavutil.mavlink_connection(kayit_yolu)
while True:
    vibration_verisi = kayit_3.recv_match(type="VIBE")
    if vibration_verisi is None:
        break
    vibrasyon_zaman_verisi = vibration_verisi.TimeUS
    z_titresim_verisi = vibration_verisi.VibeZ
    sensor_numarasi = vibration_verisi.IMU
    if sensor_numarasi == 0:
        zaman_vibrasyon_listesi.append(vibrasyon_zaman_verisi)
        titresim_listesi.append(z_titresim_verisi)
print(len(titresim_listesi))

titresim_1_listesi = np.array(titresim_listesi)
zaman_vibrasyon_1_listesi = np.array(zaman_vibrasyon_listesi)
zaman_Second_vibrasyon_listesi = (zaman_vibrasyon_1_listesi / 1000000) - (zaman_vibrasyon_listesi[0] / 1000000)
plt.figure()
plt.plot(zaman_Second_vibrasyon_listesi, titresim_1_listesi)
plt.xlabel("zaman (s)")
plt.ylabel("Vibration (m/s²)")
plt.savefig("vibration.png")

Pilot_icin_notlar_zaman = np.array(zaman_listesi_sec)
Pilot_icin_notlar_irtifa = np.array(h_listesi)
Pilot_icin_notlar_volt = np.array(volt_1_listesi)
Pilot_icin_notlar_titresim = np.array(titresim_1_listesi)

print(f"Zaman : {Pilot_icin_notlar_zaman.max():.2f} saniye")
print(f"EN YUKSEK IRTIFA : {Pilot_icin_notlar_irtifa.max():.2f} metre")
print(f"EN DUSUK GERILIM : {Pilot_icin_notlar_volt.min():.2f} volt")
print(f"EN YUKSEK TITRESIM : {Pilot_icin_notlar_titresim.max():.2f} m/s² ")
