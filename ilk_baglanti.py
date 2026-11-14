from pymavlink import mavutil
print("baglaniyor ...")
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
kalp_atisi = baglanti.wait_heartbeat()
print(kalp_atisi)