from pymavlink import mavutil
import time
baglanti = mavutil.mavlink_connection("udpin:127.0.0.1:14552")
kalp_atisi = baglanti.wait_heartbeat()
print("kalp atisi alindi")
baglanti.set_mode("GUIDED")
print("mode GUIDED olarak degistirildi")
baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
while True:
    command_mesaji = baglanti.recv_match(type = "COMMAND_ACK", blocking=True)
    print("command mesaji alindi")
    command_verisi = command_mesaji.command
    result_verisi = command_mesaji.result
    if command_verisi == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM :
       if  result_verisi == mavutil.mavlink.MAV_RESULT_ACCEPTED:
         print("YES")
         baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 20)
       else :
          print("NO")
       break
while True :
    konum = baglanti.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
    irtifa = (konum.relative_alt)/1000
    print(irtifa)
    if irtifa > 19.5 :
        baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 9, 1900, 0, 0, 0, 0, 0)
        while True:
         servo_durumu = baglanti.recv_match(type = "SERVO_OUTPUT_RAW", blocking= True)
         servo_mesaji = servo_durumu.servo9_raw
         print(servo_mesaji)
         if servo_mesaji == 1900:
             print("Yuk birakildi")
             break
        time.sleep(5)
        baglanti.mav.command_long_send(baglanti.target_system, baglanti.target_component, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 9, 1100, 0, 0, 0, 0, 0)
        while True:
         servo_durumu = baglanti.recv_match(type = "SERVO_OUTPUT_RAW", blocking= True)
         servo_mesaji = servo_durumu.servo9_raw
         if servo_mesaji == 1100:
             print("Servo kapatildi")
             break
        baglanti.set_mode("LAND")
        print("mode: LAND")
        break
