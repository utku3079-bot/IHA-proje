from pymavlink import mavutil
import sys
import time
import math
HEDEF_ENLEM = -35.3628127 
HEDEF_BOYLAM = 149.1652379 
TYPE_MASK = 3576
TIMEOUT_SURESI = 5
GOREREK_IRTIFA = 20
VARIS_ESIGI = 0.5
BEKLEME_SURESI = 3
INIS_ESIGI = GOREREK_IRTIFA - 0.5
GUIDED_MOD = 4 
LAND_MOD = 9
BAGLANTI_ADRESI = "udpin:127.0.0.1:14552"
METRE_PER_DERECE = 111320
def mesafe(enlem_1, boylam_1, HEDEF_ENLEM, HEDEF_BOYLAM):
    dikeyde_alinan_yol = (HEDEF_ENLEM - enlem_1) * METRE_PER_DERECE
    yatayda_alinan_yol = (HEDEF_BOYLAM - boylam_1) * math.cos(math.radians(enlem_1)) * METRE_PER_DERECE
    alinan_yol = math.sqrt(yatayda_alinan_yol * yatayda_alinan_yol + dikeyde_alinan_yol * dikeyde_alinan_yol )
    return(alinan_yol)
def mod_bekle(mod_numarasi):
     baslangic = time.time()
     while time.time() - baslangic < TIMEOUT_SURESI: 
            kalp_atisi = baglanti.recv_match(type="HEARTBEAT", blocking=True, timeout= TIMEOUT_SURESI)
            if kalp_atisi is None:
                sys.exit(f"{mod_numarasi} mesaji gelmedi")
            if kalp_atisi.custom_mode == mod_numarasi:
                 return True
     sys.exit("beklenen kod gelmedi")
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
try:
    gorev_tamamlandi = False
    baglanti.set_mode("GUIDED")
    print(mod_bekle(4))
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
            baglanti.mav.set_position_target_global_int_send(0, baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, TYPE_MASK, int(HEDEF_ENLEM *10000000) , int(HEDEF_BOYLAM * 10000000) , GOREREK_IRTIFA, 0, 0, 0,  0, 0, 0,  0, 0)
            break
    while True:
        konum = baglanti.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout= TIMEOUT_SURESI)
        if konum is None:
            sys.exit("Konum bilgisi alinamadi")
        enlem_1 = konum.lat / 10000000
        boylam_1 = konum.lon / 10000000
        print(mesafe(enlem_1, boylam_1, HEDEF_ENLEM, HEDEF_BOYLAM ))
        if mesafe(enlem_1, boylam_1, HEDEF_ENLEM, HEDEF_BOYLAM ) < VARIS_ESIGI:
            print("hedefe varildi")
            time.sleep(BEKLEME_SURESI)
            baglanti.set_mode("LAND")
            mod_bekle(LAND_MOD)
            gorev_tamamlandi = True
            break
finally: 
    if gorev_tamamlandi is False:
        baglanti.set_mode("RTL")
        print("mode: RTL")