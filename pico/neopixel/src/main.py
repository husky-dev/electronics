import machine, neopixel
from time import sleep_ms

np = neopixel.NeoPixel(machine.Pin(15), 60)

def clear():
  for i in range(0,59):
    np[i] = (0, 0, 0)
  np.write()

def loop():
  for i in range(0, 60):
    for j in range(0, 60):
      if i == j:
        np[j] = (255, 0 ,0)
      else:
        np[j] = (0,0,0)
    np.write()
    sleep_ms(50)

while True:
  loop()
