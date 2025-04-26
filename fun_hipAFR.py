import numpy as np
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    #chemin
] 
 
num_points = obtenir_max_points(c3d_filenames)

def get_hipAFR(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["C7"]+ markers.data["MAN"]) 
        y =  0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["C7"]+ markers.data["MAN"]) - 0.5 * (markers.data["EPSD"] + markers.data["EASD"])  
        yz = markers.data["GLD"] - markers.data["GMD"]
        knee_origin = 0.25 * (markers.data["GLD"] + markers.data["GMD"] + markers.data["EPSD"] + markers.data["EASD"])
        knee_y = markers.data["EASD"] - 0.5 * (markers.data["GLD"] + markers.data["GMD"])
        knee_yz = markers.data["GLD"] - markers.data["GMD"]
        
        
    elif side == 'L':
            markers = ktk.read_c3d(c3d_filenames[0])["Points"]
            origin = 0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["C7"]+ markers.data["MAN"]) 
            y =  0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["C7"]+ markers.data["MAN"]) - 0.5 * (markers.data["EPSG"] + markers.data["EASG"])  
            yz = markers.data["GLG"] - markers.data["GMG"]
            knee_origin = 0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["GLG"] + markers.data["GMG"])
            knee_y = markers.data["EASG"] - 0.5 * (markers.data["GLG"] + markers.data["GMG"])
            knee_yz = markers.data["GLG"] - markers.data["GMG"]
            
    else:
            raise ValueError("Invalid side specified. Use 'R' or 'L'.")
            
            
    frames = ktk.TimeSeries(time=markers.time)
    frames.data["shoulder"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["knee"] = ktk.geometry.create_frames(origin=knee_origin, y=knee_y, yz=knee_yz)

    shoulder_to_knee = ktk.geometry.get_local_coordinates(frames.data["shoulder"], frames.data["knee"])
    euler_angles = ktk.geometry.get_angles(shoulder_to_knee, "ZXY", degrees=True)

    # Interpolation des données manquantes
    for i in range(euler_angles.shape[1]):
        angle_data = euler_angles[:, i]
        indices = np.arange(len(angle_data))
        non_nan_indices = indices[~np.isnan(angle_data)]
        estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
        euler_angles[:, i] = estimated_data

    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 1], color='red', label=f"Hip {side.capitalize()} Abduction")
    plt.plot(markers.time, euler_angles[:, 0], color='green', label=f"Hip {side.capitalize()} Flexion")
    """plt.plot(markers.time, euler_angles[:, 2], color='blue', label=f"Hip {side.capitalize()} Rotation")"""
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} Hip Euler Angles")
    plt.grid(True)
    plt.show()

    return euler_angles

get_hipAFR('L', c3d_filenames, num_points)
get_hipAFR('R', c3d_filenames, num_points)
