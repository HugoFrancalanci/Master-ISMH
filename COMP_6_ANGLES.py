import numpy as np
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points

c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Desktop\CMP II (10)\Mémoire\Protocole\Motion capture\Code traitement données\Python\Fichiers_tests\TPOSE_TEST.c3d"
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

num_points = obtenir_max_points(c3d_filenames)

def get_elbowF_forearmP(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["ACD"]
        y = markers.data["ACD"] - 0.5 * (markers.data["CLD"] + markers.data["CMD"])
        yz = markers.data["CLD"] - markers.data["CMD"]
        forearm_origin = markers.data["PSUD"]
        forearm_y = 0.5 * (markers.data["CLD"] + markers.data["CMD"]) - markers.data["PSUD"]
        forearm_yz = markers.data["PSRD"] - markers.data["PSUD"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["ACG"]
        y = markers.data["ACG"] - 0.5 * (markers.data["CLG"] + markers.data["CMG"])
        yz = markers.data["CLG"] - markers.data["CMG"]
        forearm_origin = markers.data["PSUG"]
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
    plt.plot(markers.time, euler_angles[:, 2], color='green', label=f"forearm {side.capitalize()} Pronation")
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

num_points = obtenir_max_points(c3d_filenames)

def get_hipAFR(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["ACD"]
        y = markers.data["ACD"] - 0.5 * (markers.data["CLD"] + markers.data["CMD"])
        yz = markers.data["CLD"] - markers.data["CMD"]
        knee_origin = 0.5 * (markers.data["GLD"] + markers.data["GMD"])
        knee_y = markers.data["EASD"] - 0.5 * (markers.data["GLD"] + markers.data["GMD"])
        knee_yz = markers.data["GLD"] - markers.data["GMD"]
        
        
    elif side == 'L':
            markers = ktk.read_c3d(c3d_filenames[0])["Points"]
            origin = markers.data["ACG"]
            y = markers.data["ACG"] - 0.5 * (markers.data["CLG"] + markers.data["CMG"])
            yz = markers.data["CLG"] - markers.data["CMG"]
            knee_origin = 0.5 * (markers.data["GLG"] + markers.data["GMG"])
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
    plt.plot(markers.time, euler_angles[:, 0], color='red', label=f"Hip {side.capitalize()} Abduction")
    plt.plot(markers.time, euler_angles[:, 1], color='green', label=f"Hip {side.capitalize()} Flexion")
    plt.plot(markers.time, euler_angles[:, 2], color='blue', label=f"Hip {side.capitalize()} Rotation")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.legend()
    plt.title(f"{side.capitalize()} Hip Euler Angles")
    plt.grid(True)
    plt.show()

    return euler_angles

get_hipAFR('L', c3d_filenames, num_points)
get_hipAFR('R', c3d_filenames, num_points)

num_points = obtenir_max_points(c3d_filenames)

def get_kneeF_shinR(side, c3d_filenames, num_points): 
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSD"] + markers.data["EASD"])
        y = 0.5 * (markers.data["EPSD"] + markers.data["EASD"]) - 0.5 * (markers.data["GLD"] + markers.data["GMD"])  # Marqueurs du fémur et des condyles du genou droit
        yz = markers.data["GLD"] - markers.data["GMD"]
        shin_origin = 0.5*(markers.data["GLD"] + markers.data["GMD"]) 
        shin_y = 0.5*(markers.data["GLD"] + markers.data["GMD"])  - 0.5 * (markers.data["MLD"] + markers.data["MMD"])
        shin_yz = markers.data["MLD"] - markers.data["MMD"]  # Marqueur de la malléole latérale droit

    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSG"] + markers.data["EASG"])
        y = 0.5 * (markers.data["EPSG"] + markers.data["EASG"]) - 0.5 * (markers.data["GLG"] + markers.data["GMG"])  # Marqueurs du fémur et des condyles du genou gauche
        yz = markers.data["GLG"] - markers.data["GMG"]
        shin_origin = 0.5*(markers.data["GLG"] + markers.data["GMG"])   # Marqueur du tibia gauche
        shin_y = 0.5*(markers.data["GLG"] + markers.data["GMG"])  - 0.5 * (markers.data["MLG"] + markers.data["MMG"]) 
        shin_yz = markers.data["MLG"] - markers.data["MMG"]  # Marqueur des malléoles latérale/médiale de la cheville gauche

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

num_points = obtenir_max_points(c3d_filenames)

def get_shoulderAFR(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSD"] + markers.data["EASD"])
        y = 0.5 * (markers.data["EPSD"] + markers.data["EASD"]) - 0.5 * (markers.data["GLD"] + markers.data["GMD"])  # Marqueurs du fémur et des condyles du genou droit
        yz = markers.data["GLD"] - markers.data["GMD"]
        shoulder_origin = markers.data["ACD"]
        shoulder_y = markers.data["ACD"] - 0.5 * (markers.data["CLD"] + markers.data["CMD"]) 
        shoulder_yz = markers.data["CLD"] - markers.data["CMD"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSG"] + markers.data["EASG"])
        y = 0.5 * (markers.data["EPSG"] + markers.data["EASG"]) - 0.5 * (markers.data["GLG"] + markers.data["GMG"])  # Marqueurs du fémur et des condyles du genou gauche
        yz = markers.data["GLG"] - markers.data["GMG"]
        shoulder_origin = markers.data["ACG"]
        shoulder_y = markers.data["ACG"] - 0.5 * (markers.data["CLG"] + markers.data["CMG"]) 
        shoulder_yz = markers.data["CLG"] - markers.data["CMG"]
        
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["hip"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["shoulder"] = ktk.geometry.create_frames(origin=shoulder_origin, y=shoulder_y, yz=shoulder_yz)

    hips_to_shoulders = ktk.geometry.get_local_coordinates(frames.data["shoulder"], frames.data["hip"])
    euler_angles = ktk.geometry.get_angles(hips_to_shoulders, "ZXY", degrees=True)

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

num_points = obtenir_max_points(c3d_filenames)


def get_wristF_handP(side, c3d_filenames, num_points):
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = (markers.data["PSUD"])
        y = 0.5 * (markers.data["CLD"] + markers.data["CMD"]) - markers.data["PSUD"]
        yz = markers.data["PSRD"] - markers.data["PSUD"]
        hand_origin = 0.5 * (markers.data["MC2D"] + markers.data["MC5D"])
        hand_y = 0.5 * (markers.data["PSRD"] + markers.data["PSUD"]) -  0.5 * (markers.data["MC2D"] + markers.data["MC5D"])
        hand_yz = markers.data["MC2D"] - markers.data["MC5D"]
        
    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = markers.data["PSUG"]
        y = 0.5 * (markers.data["CLG"] + markers.data["CMG"]) - markers.data["PSUG"]
        yz = markers.data["PSRG"] - markers.data["PSUD"]
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
    plt.plot(markers.time, euler_angles[:, 2], color='green', label=f"hand {side.capitalize()} Pronation")
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