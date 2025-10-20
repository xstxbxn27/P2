import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

wav = "prueba.wav"          # usa exactamente este nombre
x, fs = sf.read(wav)

# Asegura mono
if x.ndim == 2:
    x = x.mean(axis=1)

# Quita offset DC global (ayuda a estabilizar la ZCR)
x = x - np.mean(x)

# zcr_unidad.py
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

wav = "prueba.wav"        # usa este nombre exacto
x, fs = sf.read(wav)
if x.ndim == 2:
    x = x.mean(axis=1)

# quita offset DC global (ayuda a estabilizar)
x = x - np.mean(x)

win = int(0.010*fs)   # 10 ms
hop = win             # salto 10 ms

def zcr_unit(frame):
    # umbral adaptativo: dead-zone para evitar cruces espurios
    rms = np.sqrt(np.mean(frame**2)) + 1e-12
    tau = 0.01 * rms              # prueba 0.005–0.02 si quieres más/menos sensibilidad
    f0, f1 = frame[:-1], frame[1:]
    mask = (np.abs(f0) > tau) & (np.abs(f1) > tau)
    crosses = ((f0 * f1) < 0) & mask
    return crosses.sum() / (len(frame) - 1)   # ← UNIDADES (0..1)

t, zcr = [], []
for i in range(0, len(x)-win+1, hop):
    fr = x[i:i+win]
    zcr.append(zcr_unit(fr))
    t.append(i/fs)

# suavizado ligero (opcional) para parecerse más a paneles de herramienta
if len(zcr) >= 3:
    zcr = np.convolve(zcr, np.ones(3)/3, mode="same")

plt.figure(figsize=(10,4))
plt.plot(t, zcr, label="ZCR (unitària 0–1)")
plt.xlabel("Temps [s]"); plt.ylabel("ZCR [0–1]")
plt.title("Taxa de creuaments per zero (unitària)")
plt.grid(True); plt.legend(); plt.tight_layout()
plt.show()