#!/usr/bin/env python3

import time
import motoron
from threading import Thread

# Direcciones I2C de los controladores Motoron
MC1_ADDR = 0x10  # Controla FL (izq) y FR (der)
MC2_ADDR = 0x11  # Controla BL (izq) y BR (der)

SPEED = 300
SAMPLE_INTERVAL_S = 1.0

# Inicializaciï¿½n de controladores Motoron
def setup_mc(mc):
    mc.reinitialize()
    mc.disable_crc()
    mc.clear_reset_flag()

mc1 = motoron.MotoronI2C(address=MC1_ADDR)
mc2 = motoron.MotoronI2C(address=MC2_ADDR)
setup_mc(mc1)
setup_mc(mc2)

# Funciï¿½n para leer velocidad actual de un canal
def read_current_speed(mc, channel):
    raw = mc.get_variables(channel, 6, 2)
    return int.from_bytes(raw, byteorder='little', signed=True)

# Hilo de monitoreo de velocidad
def monitor_speeds():
    while True:
        v_fl = read_current_speed(mc1, 2)
        v_fr = read_current_speed(mc1, 3)
        v_bl = read_current_speed(mc2, 2)
        v_br = read_current_speed(mc2, 3)
        print(f"Velocidades | FL:{v_fl:5} FR:{v_fr:5} BL:{v_bl:5} BR:{v_br:5}")
        time.sleep(SAMPLE_INTERVAL_S)

Thread(target=monitor_speeds, daemon=True).start()

# Funciï¿½n genï¿½rica para mover cada motor por separado
def move_motors(v_fl, v_fr, v_bl, v_br):
    mc1.set_speed(2, v_fl)  # FL
    mc1.set_speed(3, v_fr)  # FR
    mc2.set_speed(2, v_bl)  # BL
    mc2.set_speed(3, v_br)  # BR

# Funciones de movimiento bï¿½sicas
def move_forward():    move_motors(-SPEED,  SPEED, -SPEED,  SPEED)
def move_backward():   move_motors(SPEED, -SPEED, SPEED, -SPEED)
def turn_left():       move_motors(SPEED, SPEED, SPEED, SPEED)  # Giro antihorario
def turn_right():      move_motors(-SPEED, -SPEED, -SPEED, -SPEED)  # Giro horario
def stop_all():        move_motors(0, 0, 0, 0)

# Bucle principal
print("Control manual: w = adelante, s = atras, a = giro izq, d = giro der, x = stop, q = salir")
try:
    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == 'w':
            move_forward()
            print("Avanzando...")
        elif cmd == 's':
            move_backward()
            print("Retrocediendo...")
        elif cmd == 'a':
            turn_left()
            print("Girando a la izquierda...")
        elif cmd == 'd':
            turn_right()
            print("Girando a la derecha...")
        elif cmd == 'x':
            stop_all()
            print("Frenado!")
        elif cmd == 'q':
            print("Saliendo...")
            break
        else:
            print("Comando no reconocido.")
except KeyboardInterrupt:
    pass
finally:
    stop_all()
    print("Motores detenidos.")
