import numpy as np
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Desktop\CMP II (10)\Mémoire\Protocole\Motion capture\Code traitement données\Fichiers_tests\TPOSE_TEST.c3d"
] 

num_points = obtenir_max_points(c3d_filenames)

def get_ankleF_shinR(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["GLD"] + markers.data["GMD"])
        y = markers.data["EASD"] - 0.5 * (markers.data["GLD"] + markers.data["GMD"])
        yz = markers.data["GLD"] - markers.data["GMD"]
        feet_origin = markers.data["MT5D"]
        feet_y = 0.5*(markers.data["GLD"] + markers.data["GMD"]) - 0.5 * (markers.data["MLD"] + markers.data["MMD"])
        feet_yz = markers.data["MLD"] - markers.data["MMD"]
        
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["GLG"] + markers.data["GMG"])
        y = markers.data["EASG"] - 0.5 * (markers.data["GLG"] + markers.data["GMG"])
        yz = markers.data["GLG"] - markers.data["GMG"]
        feet_origin = markers.data["MT5G"]
        feet_y = 0.5*(markers.data["GLG"] + markers.data["GMG"]) - 0.5 * (markers.data["MLG"] + markers.data["MMG"])
        feet_yz = markers.data["MLG"] - markers.data["MMG"]
        
    else:
            raise ValueError("Invalid side specified. Use 'R' or 'L'.")
            
            
    frames = ktk.TimeSeries(time=markers.time)
    frames.data["knee"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["feet"] = ktk.geometry.create_frames(origin=feet_origin, y=feet_y, yz=feet_yz)

    knee_to_feet = ktk.geometry.get_local_coordinates(frames.data["knee"], frames.data["feet"])
    euler_angles = ktk.geometry.get_angles(knee_to_feet, "ZXY", degrees=True)

    # Interpolation des données manquantes
    for i in range(euler_angles.shape[1]):
        angle_data = euler_angles[:, i]
        indices = np.arange(len(angle_data))
        non_nan_indices = indices[~np.isnan(angle_data)]
        estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
        euler_angles[:, i] = estimated_data

    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 0], color='blue', label=f"Ankle {side.capitalize()} Flexion/Extension")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"feet {side.capitalize()} Internal/External Rotation")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} Ankle Euler Angles")
    plt.grid(True)
    plt.show()

    return euler_angles

get_ankleF_shinR('L', c3d_filenames, num_points)
get_ankleF_shinR('R', c3d_filenames, num_points)