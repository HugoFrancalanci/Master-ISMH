import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
import numpy as np
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    #chemin
] 
 
num_points = obtenir_max_points(c3d_filenames)

def get_kneeF_shinR(side, c3d_filenames, num_points): 
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSD"] + markers.data["EASD"])
        y = 0.5 * (markers.data["EPSD"] + markers.data["EASD"]) - 0.5 * (markers.data["GLD"] + markers.data["GMD"])  
        yz = markers.data["GLD"] - markers.data["GMD"]
        shin_origin = 0.5*(markers.data["MLD"] + markers.data["MMD"]) 
        shin_y = 0.5*(markers.data["GLD"] + markers.data["GMD"])  - 0.5 * (markers.data["MLD"] + markers.data["MMD"])
        shin_yz = markers.data["MLD"] - markers.data["MMD"] 
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSG"] + markers.data["EASG"])
        y = 0.5 * (markers.data["EPSG"] + markers.data["EASG"]) - 0.5 * (markers.data["GLG"] + markers.data["GMG"]) 
        yz = markers.data["GLG"] - markers.data["GMG"]
        shin_origin = 0.5*(markers.data["MLG"] + markers.data["MMG"])   
        shin_y = 0.5*(markers.data["GLG"] + markers.data["GMG"])  - 0.5 * (markers.data["MLG"] + markers.data["MMG"]) 
        shin_yz = markers.data["MLG"] - markers.data["MMG"]  
  
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["Thigh"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)  
    frames.data["Shin"] = ktk.geometry.create_frames(origin=shin_origin, y=shin_y, yz=shin_yz) 

    hip_to_shin = ktk.geometry.get_local_coordinates(frames.data["Shin"], frames.data["Thigh"])
    euler_angles = ktk.geometry.get_angles(hip_to_shin, "ZXY", degrees=True)


    # Interpolate missing data
    for i in range(euler_angles.shape[1]):
        angle_data = euler_angles[:, i]
        indices = np.arange(len(angle_data))
        non_nan_indices = indices[~np.isnan(angle_data)]
        estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
        euler_angles[:, i] = estimated_data
    
    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 0], color='blue', label=f"Knee {side.capitalize()} Flexion/Extension")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"Knee {side.capitalize()} Internal/External Rotation")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} Knee Euler Angles")
    plt.grid(True)
    plt.show()
    
    # Return the Euler angles
    return euler_angles

get_kneeF_shinR('R', c3d_filenames, num_points)
get_kneeF_shinR('L', c3d_filenames, num_points)
