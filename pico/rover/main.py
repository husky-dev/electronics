from machine import Pin, PWM, ADC
from time import sleep_ms

# ✅ Simple binary usage
# motor_A_IA.on() - Forward
# motor_A_IB.on() - Reverse
motor_A_IA = Pin(2, Pin.OUT, value = 0)
motor_A_IB = Pin(3, Pin.OUT, value = 0)
motor_B_IA = Pin(4, Pin.OUT, value = 0)
motor_B_IB = Pin(5, Pin.OUT, value = 0)

# PWM
motor_A_IA_pwm = PWM(Pin(2))
motor_A_IA_pwm.freq(20000) # 20kHz
motor_A_IA_pwm.duty_u16(32768) # 50%



# joistic_rx_pin = 28
# joistic_rx_adc = ADC(joistic_rx_pin)

# while True:
#   val = joistic_rx_adc.read_u16()
#   print(val)
#   motor_A_IA.off()
#   motor_A_IB.off()
#   motor_B_IA.off()
#   motor_B_IB.off()
#   if val < 30000:
#     motor_A_IA.on()
#     motor_B_IA.on()
#     print("go forward")
#   if val > 40000:
#     motor_A_IB.on()
#     motor_B_IB.on()
#     print("go back")
#   sleep_ms(100)
