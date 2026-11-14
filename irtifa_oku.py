from pymavlink import mavutil
print("baglaniyor ...")
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
kalp_atisi = baglanti.wait_heartbeat()
while True:
    konum = baglanti.recv_match(type="GLOBAL_POSITION_INT", blocking=True)

    enlem = konum.lat
    boylam = konum.lon 
    irtifa = konum.relative_alt
    print(f"Enlem = {enlem/ 10000000}")
    print(f"Boylam = {boylam / 10000000}")
    print(f"Irtifa = {irtifa/ 1000}")