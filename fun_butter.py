import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5): 
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Lecture des données C3D
c3d_filenames = [
    r"C:\Users\idris\Desktop\QUALISYS\TEST\ANKLE_TEST.c3d"
]
c3d_data = ktk.read_c3d(c3d_filenames[0])

# Obtention des points maximaux
num_points = obtenir_max_points(c3d_filenames)

# Extraction des données de marqueurs
markers = c3d_data["Points"]

# Obtention de la fréquence d'échantillonnage
fs = 1 / (markers.time[1] - markers.time[0])

## Sélection des données à filtrer
data_to_filter = markers.data["ACG"]

# Paramètres du filtre Butterworth
lowcut = 0.1  # Fréquence de coupure basse
highcut = 75  # Fréquence de coupure haute
order = 5 # Ordre du filtre

# Obtention de la fréquence d'échantillonnage
fs = 1 / (markers.time[1] - markers.time[0])

# Normalisation des fréquences de coupure
lowcut_normalized = lowcut / (fs / 2)
highcut_normalized = highcut / (fs / 2)

# Application du filtre Butterworth
filtered_data = butter_bandpass_filter(data_to_filter, lowcut_normalized, highcut_normalized, fs, order=order)

# Affichage des données originales et filtrées avec des couleurs différentes pour chaque dimension
plt.plot(markers.time, data_to_filter[:, 0], linestyle='--', label='X non filtré', color='blue')
plt.plot(markers.time, filtered_data[:, 0], linestyle='-', linewidth=2, label='X filtré', color='blue')

plt.plot(markers.time, data_to_filter[:, 1], linestyle='--', label='Y non filtré', color='orange')
plt.plot(markers.time, filtered_data[:, 1], linestyle='-', linewidth=2, label='Y filtré', color='orange')

plt.plot(markers.time, data_to_filter[:, 2], linestyle='--', label='Z non filtré', color='purple')
plt.plot(markers.time, filtered_data[:, 2], linestyle='-', linewidth=2, label='Z filtré', color='purple')

plt.xlabel('Temps')
plt.ylabel('Amplitude')
plt.legend()
plt.show()



