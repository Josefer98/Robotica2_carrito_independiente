#!/usr/bin/env python3

import time
import motoron
from threading import Thread

# --- Configuraciï¿½n mï¿½dulos Motoron ---
MC1_ADDR = 0x10  # mï¿½dulo controla motores 1 y 2 (ruedas izquierda)
MC2_ADDR = 0x11  # mï¿½dulo controla motores 3 y 4 (ruedas derecha)
SAMPLE_INTERVAL_S = 1.0
SPEED = 500

# Inicializaciï¿½n de mï¿½dulos Motoron
def setup_mc(mc):
    mc.reinitialize()
    mc.disable_crc()
    mc.clear_reset_flag()

mc1 = motoron.MotoronI2C(address=MC1_ADDR)
mc2 = motoron.MotoronI2C(address=MC2_ADDR)
setup_mc(mc1)
setup_mc(mc2)

# Funciï¿½n para leer "Current speed" de un canal del Motoron
# Offset 6, longitud 2 bytes (signed int16)
def read_current_speed(mc, channel):
    raw = mc.get_variables(channel, 6, 2)
    return int.from_bytes(raw, byteorder='little', signed=True)

# Monitoreo de velocidades de los cuatro motores
def monitor_speeds():
    while True:
        # Leer canales 2 y 3 de cada mï¿½dulo
        v1 = read_current_speed(mc1, 2)
        v2 = read_current_speed(mc1, 3)
        v3 = read_current_speed(mc2, 2)
        v4 = read_current_speed(mc2, 3)
        print(f"Velocidades | M1: {v1} | M2: {v2} | M3: {v3} | M4: {v4}")
        time.sleep(SAMPLE_INTERVAL_S)

# Funciones de movimiento

def move_forward(speed=SPEED):
    # ambos mï¿½dulos hacia adelante
    mc1.set_speed(2, speed)
    mc1.set_speed(3, speed)
    mc2.set_speed(2, speed)
    mc2.set_speed(3, speed)


def move_backward(speed=SPEED):
    mc1.set_speed(2, -speed)
    mc1.set_speed(3, -speed)
    mc2.set_speed(2, -speed)
    mc2.set_speed(3, -speed)


def strafe_right(speed=SPEED):
    # izquierda atrï¿½s, derecha adelante
    mc1.set_speed(2, -speed)
    mc1.set_speed(3, -speed)
    mc2.set_speed(2, speed)
    mc2.set_speed(3, speed)


def strafe_left(speed=SPEED):
    mc1.set_speed(2, speed)
    mc1.set_speed(3, speed)
    mc2.set_speed(2, -speed)
    mc2.set_speed(3, -speed)


def stop_all():
    mc1.set_speed(2, 0)
    mc1.set_speed(3, 0)
    mc2.set_speed(2, 0)
    mc2.set_speed(3, 0)

# Lanzar hilo de monitoreo de velocidades
monitor_thread = Thread(target=monitor_speeds, daemon=True)
monitor_thread.start()

# Ciclo principal de demostraciï¿½n
try:
    while True:
        print("Adelante")
        move_forward()
        time.sleep(2)

        print("Atras")
        move_backward()
        time.sleep(2)

        print("Derecha")
        strafe_right()
        time.sleep(2)

        print("Izquierda")
        strafe_left()
        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    print("Deteniendo motores...")
    stop_all()
    print("Motores detenidos.")