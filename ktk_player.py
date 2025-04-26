
import kineticstoolkit.lab as ktk

# Download and read markers from a sample C3D file
filename = r"C:\Users\idris\Desktop\Meshes\TEST\ANKLE_TEST.c3d"
markers = ktk.read_c3d(filename)["Points"]



p=ktk.Player(markers,up="z", anterior="y")
