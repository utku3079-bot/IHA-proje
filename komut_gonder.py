from pymavlink import mavutil
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
       else :
          print("NO")
       break
print(result_verisi)
