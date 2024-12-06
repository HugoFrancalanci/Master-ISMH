import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
import numpy as np
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    #chemin
] 
 
num_points = obtenir_max_points(c3d_filenames)


def get_wristF_handP(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = (markers.data["CLD"] + markers.data["CMD"])*0.5
        y = 0.5 * (markers.data["CLD"] + markers.data["CMD"]) - markers.data["PSUD"]
        yz = markers.data["PSRD"] - markers.data["PSUD"]
        hand_origin = 0.5 * (markers.data["MC2D"] + markers.data["MC5D"])
        hand_y = 0.5 * (markers.data["PSRD"] + markers.data["PSUD"]) -  0.5 * (markers.data["MC2D"] + markers.data["MC5D"])
        hand_yz = markers.data["MC2D"] - markers.data["MC5D"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = (markers.data["CLG"] + markers.data["CMG"])*0.5
        y = 0.5 * (markers.data["CLG"] + markers.data["CMG"]) - markers.data["PSUG"]
        yz = markers.data["PSUG"] - markers.data["PSRG"]
        hand_origin = 0.5 * (markers.data["MC2G"] + markers.data["MC5G"])
        hand_y = 0.5 * (markers.data["PSRG"] + markers.data["PSUG"]) - 0.5 * (markers.data["MC2G"] + markers.data["MC5G"])
        hand_yz = markers.data["MC2G"] - markers.data["MC5G"]
        
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")


    frames = ktk.TimeSeries(time=markers.time)
    frames.data["forearm"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["hand"] = ktk.geometry.create_frames(origin=hand_origin, y=hand_y, yz=hand_yz)

    forearm_to_hand = ktk.geometry.get_local_coordinates(frames.data["forearm"], frames.data["hand"])
    euler_angles = ktk.geometry.get_angles(forearm_to_hand, "ZXY", degrees=True)

    # Sample data for testing
    angle_data = np.array([10, np.nan, 20, np.nan, 30])
    indices = np.arange(len(angle_data))
    non_nan_indices = indices[~np.isnan(angle_data)]

    # Print values before interpolation
    print("Indices:", indices)
    print("Non-NaN Indices:", non_nan_indices)
    print("Angle Data:", angle_data)

    # Interpolate missing data
    estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])

    # Print interpolated data
    print("Estimated Data:", estimated_data)

    
    # Plot the Euler angles with different colors
    plt.figure()
    plt.plot(markers.time, euler_angles[:, 0], color='blue', label=f"wrist {side.capitalize()} Flexion")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"hand {side.capitalize()} Pronation")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} wrist Euler Angles")
    plt.grid(True)
    plt.show()
    
    
    # Return the Euler angles
    return euler_angles

get_wristF_handP('R', c3d_filenames, num_points)
get_wristF_handP('L', c3d_filenames, num_points)
