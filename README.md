# BAE · Baby Ambient Eco-sensor

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Eco-Friendly-2ecc71?style=for-the-badge&logo=leaf&logoColor=white"/>
</p>

> **BAE** es un nano dispositivo ecológico integrado al pañal del bebé que detecta en tiempo real si el pañal está **seco y estable** o **mojado**, mediante sensores de humedad y temperatura.

---

## 🌿 ¿Qué es BAE?

BAE (Baby Ambient Eco-sensor) es un dispositivo de **1.2 gramos** y **18×12 mm** fabricado con materiales 100% ecológicos:

| Componente | Material |
|---|---|
| PCB | Sustrato biodegradable |
| Sensor de humedad | Fibra orgánica conductora |
| Carcasa | Bambú prensado |
| Tinta de circuitos | Tinta vegetal conductora |
| Batería | Celda flexible de 72h de duración |

---

## 🚀 Despliegue rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/BAE.git
cd BAE
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar localmente

```bash
streamlit run app.py
```

### 4. Desplegar en Streamlit Cloud

1. Sube el repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repo `BAE` y el archivo `app.py`
5. Haz clic en **Deploy** ✅

---

## 📊 Funcionalidades

- 👶 **Avatar animado** del bebé — feliz (pañal seco) o llorando (pañal mojado)
- 💧 **Monitor de humedad** con barra visual en tiempo real
- 🌡️ **Sensor de temperatura** con alertas de frío/calor
- 📋 **Historial de lecturas** con timestamps
- ⚙️ **Umbrales configurables** desde el sidebar
- 🎮 **Modo demostración** con simulación sinusoidal automática
- 🌿 **Info del dispositivo** ecológico

---

## 🔬 Especificaciones técnicas

```
Dimensiones:     18 × 12 × 1.5 mm
Peso:            1.2 g
Conectividad:    BLE 5.0
Batería:         72 horas continuas
Sensor humedad:  Resistivo orgánico, precisión ±2%
Sensor temp:     Termistor NTC, precisión ±0.3°C
Muestreo:        Cada 3 segundos
```

---

## 🛠️ Estructura del proyecto

```
BAE/
├── app.py              # App principal Streamlit
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

---

## 📝 Cómo conectar hardware real

Cuando conectes el nano dispositivo BAE físico, reemplaza la sección de simulación en `app.py`:

```python
# Reemplazar la sección "demo_mode" con:
import serial
port = serial.Serial('/dev/ttyUSB0', 9600)
line = port.readline().decode().strip()
humidity, temperature = map(float, line.split(','))
```

El firmware del dispositivo debe enviar por serial: `HUMEDAD,TEMPERATURA\n`  
Ejemplo: `67.3,28.5`

---

<p align="center">
  Hecho con 🌿 y ❤️ · BAE v1.0.0
</p>
