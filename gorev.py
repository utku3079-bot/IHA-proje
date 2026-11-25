from pymavlink import mavutil

import sys
baglanti_adresi = "udpin:127.0.0.1:14552"
print(f"okunan kayit: {baglanti_adresi}")
baglanti = mavutil.mavlink_connection(baglanti_adresi)
kalp_atisi = baglanti.wait_heartbeat(timeout = 5)
if kalp_atisi is None :
    sys.exit("Kalp atisi alinmadi")
print("kalp atisi alindi")
baglanti.set_mode("GUIDED")
print("mode GUIDED olarak degistirildi")
baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
while True:
    command_mesaji = baglanti.recv_match(type = "COMMAND_ACK", blocking=True, timeout = 5)
    if command_mesaji is None :
        sys.exit("Command mesaji alinmadi")
    print("command mesaji alindi")
    command_verisi = command_mesaji.command
    result_verisi = command_mesaji.result
    if command_verisi == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM :
       if  result_verisi == mavutil.mavlink.MAV_RESULT_ACCEPTED:
         print("YES")
         baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 20)
       else :
          print("NO")
          sys.exit("Hata: command verisi veya result verisi dogru degil")
       break
while True: 
    veri = baglanti.recv_match(type="COMMAND_ACK", blocking=True, timeout = 5)
    if veri is None:
        print("hiçbir şey gelmedi")
        sys.exit("Hata: command mesaji beklendi ama gelmedi")
    kalkis_verisi = veri.command
    result_cevabi = veri.result
    if kalkis_verisi == mavutil.mavlink.MAV_CMD_NAV_TAKEOFF:
        if result_cevabi == mavutil.mavlink.MAV_RESULT_ACCEPTED:
          print("kalkis emri verildi")
          break
        else :
          print("Kalkis reddedildi")
          sys.exit("Hata: command veya result verisi dogru degil")
while True :
    konum = baglanti.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout = 5)
    if konum is None :
        sys.exit("Konum bilgisi alinamadi")
    irtifa = (konum.relative_alt)/1000
    print(irtifa)
    if irtifa > 19.5 :
        baglanti.set_mode("LAND")
        print("mode: LAND")
        break
