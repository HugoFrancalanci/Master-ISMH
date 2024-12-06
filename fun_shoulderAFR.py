#A VOIR AVEC MONSIEUR HYBOIS (FLEXION OK / ADDUCTION ET/OU ROTATION NON)

import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
import numpy as np
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Desktop\CMP II (10)\Mémoire\Protocole\Motion capture\Code traitement données\Python\Code 3D\Final\Code\STAGE_M1\Test_donnees\SHOULDER_TEST.c3d"
] 
 
num_points = obtenir_max_points(c3d_filenames)

def get_shoulderAFR(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["C7"]+ markers.data["MAN"]) 
        y =  0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["C7"]+ markers.data["MAN"]) - 0.5 * (markers.data["EPSD"] + markers.data["EASD"])  
        yz = markers.data["GLD"] - markers.data["GMD"]
        elbow_origin = (markers.data["CLD"] + markers.data["CMD"])*0.5
        elbow_y = 0.5 * (markers.data["CLD"] + markers.data["CMD"]) - markers.data["PSUD"]
        elbow_yz = markers.data["CLD"] - markers.data["CMD"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["C7"]+ markers.data["MAN"]) 
        y =  0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["C7"]+ markers.data["MAN"]) - 0.5 * (markers.data["EPSG"] + markers.data["EASG"])  
        yz = markers.data["GLG"] - markers.data["GMG"]
        elbow_origin = (markers.data["CLG"] + markers.data["CMG"])*0.5
        elbow_y = 0.5 * (markers.data["CLG"] + markers.data["CMG"]) - markers.data["PSUG"]
        elbow_yz = markers.data["CLG"] - markers.data["CMG"]
        
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["hip"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["elbow"] = ktk.geometry.create_frames(origin=elbow_origin, y=elbow_y, yz=elbow_yz)

    hips_to_elbow = ktk.geometry.get_local_coordinates(frames.data["elbow"], frames.data["hip"])
    euler_angles = ktk.geometry.get_angles(hips_to_elbow, "zxy", degrees=True)

    # Interpolation des données manquantes
    for i in range(euler_angles.shape[1]):
        angle_data = euler_angles[:, i]
        indices = np.arange(len(angle_data))
        non_nan_indices = indices[~np.isnan(angle_data)]
        estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
        euler_angles[:, i] = estimated_data
    
    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 0], color='red', label=f"Shoulder {side.capitalize()} Abduction")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"Shoulder {side.capitalize()} Flexion")
    plt.plot(markers.time, euler_angles[:, 2], color='blue', label=f"Shoulder {side.capitalize()} Rotation")
    
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} Shoulder Euler Angles")
    plt.grid(True)
    plt.show()

    return euler_angles

get_shoulderAFR('L', c3d_filenames, num_points)
get_shoulderAFR('R', c3d_filenames, num_points)