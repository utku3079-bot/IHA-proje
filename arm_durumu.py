from pymavlink import mavutil
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
kalp_atisi = baglanti.wait_heartbeat()
while True:
    veri = baglanti.recv_match(type="HEARTBEAT", blocking=True)
    motor_durumu = veri.base_mode
    if (motor_durumu & MAV_MODE_FLAG_SAFETY_ARMED) == MAV_MODE_FLAG_SAFETY_ARMED:
        print("ARMED")
    else :
        print("DISARMED")
    print(motor_durumu)
    