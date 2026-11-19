import numpy as np
import matplotlib.pyplot as plt
from pymavlink import mavutil
kayit = mavutil.mavlink_connection("/home/adali/ardupilot/logs/00000018.BIN")
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
kayit_2 = mavutil.mavlink_connection("/home/adali/ardupilot/logs/00000018.BIN")
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