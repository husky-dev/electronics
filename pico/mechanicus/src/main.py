from ps2 import PS2Controller
# from motor import Motor
# from time import sleep, sleep_ms

# motor_left_front = Motor(ia_pin=16, ib_pin=17)
# motor_left_back = Motor(ia_pin=18, ib_pin=19)

# motor_right_front = Motor(ia_pin=13, ib_pin=12)
# motor_right_back = Motor(ia_pin=15, ib_pin=14)

# Green - data (di_pin_no)
# Orange - CMD (do_pin_no)
# Yellow - attn (cs_pin_no)
# Blue - CLK (clk_pin_no)
ps = PS2Controller(di_pin_no=2, do_pin_no=3, cs_pin_no=4, clk_pin_no=5)
ps.init()
while True:
  ps.read_once()
  if len(ps.pressed_keys) > 0:
    print(ps.pressed_keys)

# def map_values(x,a,b,c,d):
#    y=(x-a)/(b-a)*(d-c)+c
#    return y

# def forward():
#   speed = 100
#   motor_left_front.forward(speed)
#   motor_left_back.forward(speed)
#   motor_right_front.forward(speed)
#   motor_right_back.forward(speed)

# def back():
#   speed = 100
#   motor_left_front.back(speed)
#   motor_left_back.back(speed)
#   motor_right_front.back(speed)
#   motor_right_back.back(speed)

# def stop():
#   motor_left_front.stop()
#   motor_left_back.stop()
#   motor_right_front.stop()
#   motor_right_back.stop()

# def sideway_right():
#   motor_left_front.forward(100)
#   motor_left_back.back(100)
#   motor_right_front.back(100)
#   motor_right_back.forward(100)

# def sideway_left():
#   motor_left_front.back(100)
#   motor_left_back.forward(100)
#   motor_right_front.forward(100)
#   motor_right_back.back(100)

# def diagonal():
#   motor_left_front.forward(100)
#   motor_right_back.forward(100)

# def turn_of_rear_axis():
#   motor_left_front.forward(100)
#   motor_right_front.back(100)

# def motors_test():
#   sleep(2)
#   motor_left_front.forward()
#   sleep(1)
#   motor_left_front.stop()
#   sleep(1)
#   motor_left_back.forward()
#   sleep(1)
#   motor_left_back.stop()
#   sleep(1)
#   motor_right_front.forward()
#   sleep(1)
#   motor_right_front.stop()
#   sleep(1)
#   motor_right_back.forward()
#   sleep(1)
#   motor_right_back.stop()

# def start():
#   # ctrl.init()
#   # while True:
#   #   ctrl.read_once()
#   #   ly = ctrl.ly
#   #   print("ly = %d" % ly)
#   #   if ly == 0:
#   #     stop()
#   #   if ly < 0:
#   #     speed = map_values(ly, 0, -128, 0, 100)
#   #     print("forward = %d" % speed)
#   #     forward()
#   #   if ly > 0:
#   #     speed = map_values(ly, 0, 128, 0, 100)
#   #     print("back = %d" % speed)
#   #     back()
#   sleep(3)

#   forward()
#   sleep(1)
#   stop()
#   sleep(1)

#   back()
#   sleep(1)
#   stop()
#   sleep(1)

#   sideway_right()
#   sleep(1)
#   stop()
#   sleep(1)

#   sideway_left()  
#   sleep(1)
#   stop()
#   sleep(1)

#   diagonal()  
#   sleep(1)
#   stop()
#   sleep(1)

#   turn_of_rear_axis()  
#   sleep(1)
#   stop()
#   sleep(1)

# start()
