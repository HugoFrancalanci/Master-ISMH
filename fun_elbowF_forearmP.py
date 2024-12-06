#VALIDE

import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
import numpy as np
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Desktop\CMP II (10)\Mémoire\Protocole\Motion capture\Code traitement données\Python\Code 3D\Final\habiletes_tests\THM_S1_M1.c3d"
] 
 
num_points = obtenir_max_points(c3d_filenames)

def get_elbowF_forearmP(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["ACD"]
        y = markers.data["ACD"] - 0.5 * (markers.data["CLD"] + markers.data["CMD"])
        yz = markers.data["CLD"] - markers.data["CMD"]
        forearm_origin = (markers.data["PSUD"] + markers.data["PSRD"])*0.5
        forearm_y = 0.5 * (markers.data["CLD"] + markers.data["CMD"]) - markers.data["PSUD"]
        forearm_yz = markers.data["PSRD"] - markers.data["PSUD"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["ACG"]
        y = markers.data["ACG"] - 0.5 * (markers.data["CLG"] + markers.data["CMG"])
        yz = markers.data["CLG"] - markers.data["CMG"]
        forearm_origin = (markers.data["PSUG"] + markers.data["PSRG"])*0.5
        forearm_y = 0.5 * (markers.data["CLG"] + markers.data["CMG"]) - markers.data["PSUG"]
        forearm_yz = markers.data["PSRG"] - markers.data["PSUG"]
        
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")


    frames = ktk.TimeSeries(time=markers.time)
    frames.data["arm"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["forearm"] = ktk.geometry.create_frames(origin=forearm_origin, y=forearm_y, yz=forearm_yz)

    arm_to_forearm = ktk.geometry.get_local_coordinates(frames.data["forearm"], frames.data["arm"])
    euler_angles = ktk.geometry.get_angles(arm_to_forearm, "ZXY", degrees=True)

    # Interpolate missing data
    for i in range(euler_angles.shape[1]):
        angle_data = euler_angles[:, i]
        indices = np.arange(len(angle_data))
        non_nan_indices = indices[~np.isnan(angle_data)]
        estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
        euler_angles[:, i] = estimated_data
    
    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 0], color='blue', label=f"elbow {side.capitalize()} Flexion")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"forearm {side.capitalize()} Pronation")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} elbow Euler Angles")
    plt.grid(True)
    plt.show()
    
    
    # Return the Euler angles
    return euler_angles

get_elbowF_forearmP('L', c3d_filenames, num_points)
get_elbowF_forearmP('R', c3d_filenames, num_points)










