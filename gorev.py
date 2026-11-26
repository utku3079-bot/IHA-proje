from pymavlink import mavutil
import sys
TIMEOUT_SURESI = 5
GOREREK_IRTIFA = 20
INIS_ESIGI = GOREREK_IRTIFA - 0.5
BAGLANTI_ADRESI = "udpin:127.0.0.1:14552"

def ack_bekle(komut):
    # Gonderilen komutun cevabini (COMMAND_ACK) bekler.
    # Kabul edilirse True dondurur; cevap gelmezse ya da reddedilirse programi durdurur.
    while True:
        cevap = baglanti.recv_match(type="COMMAND_ACK", blocking=True, timeout= TIMEOUT_SURESI)
        if cevap is None:
            sys.exit(f"Hata: {komut} komutunun cevabi {TIMEOUT_SURESI} saniye icinde gelmedi")
        if cevap.command == komut:
            if cevap.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                print(f"{komut} komutu kabul edildi")
                return True
            else:
                sys.exit(f"Hata: {komut} komutu reddedildi (result={cevap.result})")


print(f"Baglanti adresi: {BAGLANTI_ADRESI}")
baglanti = mavutil.mavlink_connection(BAGLANTI_ADRESI)
kalp_atisi = baglanti.wait_heartbeat(timeout= TIMEOUT_SURESI)
if kalp_atisi is None:
    sys.exit("Kalp atisi alinmadi")
print("kalp atisi alindi")

baglanti.set_mode("GUIDED")
print("mode GUIDED olarak degistirildi")

# Arm
baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
ack_bekle(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM)

# Kalkis 
baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, GOREREK_IRTIFA)
ack_bekle(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF)

# INIS_ESIGI'ni gecince
while True:
    konum = baglanti.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout= TIMEOUT_SURESI)
    if konum is None:
        sys.exit("Konum bilgisi alinamadi")
    irtifa = (konum.relative_alt)/1000
    print(irtifa)
    if irtifa > INIS_ESIGI:
        baglanti.set_mode("LAND")
        print("mode: LAND")
        break
