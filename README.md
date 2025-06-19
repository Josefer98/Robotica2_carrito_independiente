# Robotica2_carrito_independiente
## Nombres: Cristian Alejandro Durán Ignacio - Alfaro Ayzama José Fernando - Ever Rolando Rejas Espinoza

# 🚀 Proyecto final carrito independiente con baterias externas

💡 Este proyecto muestra cómo controlar un conjunto de cuatro ruedas mecanum omnidireccionales usando dos módulos Motoron I2C desde una Raspberry Pi 4

## 📌 Introducción

Utilizamos dos controladores Motoron (direcciones I2C `0x10` y `0x11`) para manejar cuatro motores con ruedas mecanum, logrando movimientos en cuatro direcciones: adelante, atrás, lateral derecha y lateral izquierda.  

## 🧰 Tecnologías y Librerías

- **Python 3**  
- **motoron** (driver I2C para módulos Motoron)  
- **time** (para temporización)
- 
## 🚀 Para armado, instalación y ejecución de código
### Clonar el repositorio
Copiar código
```bash
git clone https://github.com/Cristian-duran/RobotCt_Omni_Wheel
```
Dependencias y librerías necesarias
🔧 Instalar todo en uno:
```bash
pip install -r requirements.txt
```

motoron
```bash
pip install motoron

```

## ⚙️ Esquema de funcionamiento
Conecta ambos módulos Motoron a la Raspberry Pi vía I2C.

Ajusta las direcciones I2C si fuese necesario:

```bash
MC1_ADDR = 0x10  # módulo controla motores 1 y 2 (izquierdas)
MC2_ADDR = 0x11  # módulo controla motores 3 y 4 (derechas)
```

Ajusta la velocidad base en la misma cabecera:
```bash
SPEED = 800  # rango de -máximo a +máximo
```

Ejecuta el script de demostración:
```bash
SPEED = 800  # rango de -máximo a +máximo
```
```bash
python i2c_simple_multi_example.py
```

Se vera en consola la secuencia de movimientos:

Adelante (2 s)

Atrás (2 s)

Derecha (2 s)

Izquierda (2 s)

## 📌 Nota importante
Asegúrarnos de que el bus I2C esté habilitado en tu Raspberry Pi (raspi-config).
