import kineticstoolkit.lab as ktk
import numpy as np

def interpolate_data(points, max_points):
    interpolated_points = {}
    for marker, data in points.data.items():
        # Interpoler les données pour avoir le même nombre de points
        interpolated_data = np.zeros((max_points, 3))
        for dim in range(3):
            interpolated_data[:, dim] = np.interp(np.linspace(0, 1, max_points), np.linspace(0, 1, len(data)), data[:, dim])
        interpolated_points[marker] = interpolated_data
    return interpolated_points

def obtenir_max_points(c3d_filenames):
    max_points = max(len(ktk.read_c3d(c3d_filename)["Points"].time) for c3d_filename in c3d_filenames)
    return max_points



