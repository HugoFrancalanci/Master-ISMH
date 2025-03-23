import matplotlib.pyplot as plt
import numpy as np
import kineticstoolkit.lab as ktk

markers = ktk.read_c3d(
    r"C:\Users\idris\Desktop\Meshes\c3d_Data_Tennis\LIGNES\S01_L1_F1.c3d")["Points"]

markers = markers.get_subset(
    ["MTBD", "CLD", "CMD", "MTABD","PSRD","PSUD","MC2D","MC5D"]
)

"""
# Plot the markers trajectories

plt.subplot(2, 2, 1)
markers.plot("MTBD")
plt.subplot(2, 2, 2)
markers.plot("CLD")
plt.subplot(2, 2, 3)
markers.plot("CMD")
plt.subplot(2, 2, 4)
markers.plot("MTABD")
plt.subplot(2, 2, 5)
markers.plot("PSRD")
plt.subplot(2, 2, 6)
markers.plot("PSUD")
plt.subplot(2, 2, 7)
markers.plot("MC2D")
plt.subplot(2, 2, 8)
markers.plot("MC5D")
plt.tight_layout()
"""
cluster = ktk.kinematics.create_cluster(
    markers,
    ["MTABD","PSRD","PSUD","MC2D","MC5D"],
)

# Print the contents of the cluster
print(cluster["MTABD"])
print(cluster["PSRD"])
print(cluster["PSUD"])
print(cluster["MC2D"])
print(cluster["MC5D"])


reconstructed_markers = ktk.kinematics.track_cluster(markers, cluster)

# Plot the markers trajectories
plt.subplot(2, 2, 1)
reconstructed_markers.plot("MTABD")
plt.subplot(2, 2, 2)
reconstructed_markers.plot("PSRD")
plt.subplot(2, 2, 3)
reconstructed_markers.plot("PSUD")
plt.subplot(2, 2, 4)
reconstructed_markers.plot("MC2D")
plt.subplot(2, 2, 5)
reconstructed_markers.plot("MC5D")
plt.tight_layout()