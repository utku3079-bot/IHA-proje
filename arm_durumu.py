from pymavlink import mavutil
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
kalp_atisi = baglanti.wait_heartbeat()
MAV_MODE_FLAG_SAFETY_ARMED = 128
while True:
    veri = baglanti.recv_match(type="HEARTBEAT", blocking=True)
    motor_durumu = veri.base_mode
    if (motor_durumu & MAV_MODE_FLAG_SAFETY_ARMED) == MAV_MODE_FLAG_SAFETY_ARMED:
        print("ARMED")
    elif (motor_durumu & 81) == 81 :
        print("stabilized")
    else :
        print("DISARMED")
    print(motor_durumu)
    