from pymavlink import mavutil
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14552")
kalp_atisi = baglanti.wait_heartbeat()
baglanti.set_mode("GUIDED")

baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

