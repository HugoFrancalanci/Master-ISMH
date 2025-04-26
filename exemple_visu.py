import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points


def get_elbowF_forearmP(side, c3d_filenames, num_points):
    # Get shoulder center based on side
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
        raise ValueError("Invalid side specified. Use 'right' or 'left'.")


    frames = ktk.TimeSeries(time=markers.time)
    frames.data["Arm"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["Forearm"] = ktk.geometry.create_frames(origin=forearm_origin, y=forearm_y, yz=forearm_yz)

    # Merge 'markers' and 'frames' TimeSeries objects
    merged_data = ktk.TimeSeries.merge(markers, frames)

    # Set the merged data to the contents using matplotlib
    ktk.Player(merged_data)

# Example usage:
# Specify your arguments accordingly
c3d_filenames = [
    r"D:\QUALISYS\c3d_Data_Tennis\LIGNES/S08_L1_F1.c3d"
] # Provide actual file paths
num_points = obtenir_max_points(c3d_filenames)

# Call the function
''''get_elbowF_forearmP('R', c3d_filenames, num_points)'''
get_elbowF_forearmP('L', c3d_filenames, num_points)


# Display the plot if you expect something to be plotted
plt.show()



##################
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points

def get_kneeF_shinR(side, c3d_filenames, num_points): 
    if side == 'R':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSD"] + markers.data["EASD"])
        y = 0.5 * (markers.data["EPSD"] + markers.data["EASD"]) - 0.5 * (markers.data["GLD"] + markers.data["GMD"])  # Marqueurs du fémur et des condyles du genou droit
        yz = markers.data["GLD"] - markers.data["GMD"]
        shin_origin = markers.data["TIBD"]  # Marqueur du tibia droit
        shin_y = markers.data["TIBD"] - 0.5 * (markers.data["MLD"] + markers.data["MMD"])
        shin_yz = markers.data["MLD"] - markers.data["MMD"]  # Marqueur de la malléole latérale droit

    elif side == 'L':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.5 * (markers.data["EPSG"] + markers.data["EASG"])
        y = 0.5 * (markers.data["EPSG"] + markers.data["EASG"]) - 0.5 * (markers.data["GLG"] + markers.data["GMG"])  # Marqueurs du fémur et des condyles du genou gauche
        yz = markers.data["GLG"] - markers.data["GMG"]
        shin_origin = markers.data["TIBG"]  # Marqueur du tibia gauche
        shin_y = markers.data["TIBG"] - 0.5 * (markers.data["MLG"] + markers.data["MMG"]) 
        shin_yz = markers.data["MLG"] - markers.data["MMG"]  # Marqueur des malléoles latérale/médiale de la cheville gauche

    else:
        raise ValueError("Invalid side specified. Use 'right' or 'left'.")

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["Thigh"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)  
    frames.data["Shin"] = ktk.geometry.create_frames(origin=shin_origin, y=shin_y, yz=shin_yz) 

    # Merge 'markers' and 'frames' TimeSeries objects
    merged_data = ktk.TimeSeries.merge(markers, frames)

    # Set the merged data to the contents using matplotlib
    ktk.Player(merged_data)

# Example usage:
# Specify your arguments accordingly
c3d_filenames = [
    r"C:\Users\idris\Desktop\Meshes\c3d_Data_Tennis\LIGNES\S01_L1_F1.c3d"
] # Provide actual file paths
num_points = obtenir_max_points(c3d_filenames)

# Call the function
get_kneeF_shinR('L', c3d_filenames, num_points)


# Display the plot if you expect something to be plotted
plt.show()



##################
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points


def get_shoulderAFR(side, c3d_filenames, num_points):
    markers = ktk.read_c3d(c3d_filenames[0])["Points"]
    
    if side == 'R':
        origin = 0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["ACD"] + markers.data["XPY"])
        y = 0.33 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["ACD"]) - 0.5 * (markers.data["EPSD"] + markers.data["EASD"])
        yz = markers.data["GLD"] - markers.data["GMD"]
        elbow_origin = 0.5 * (markers.data["CLD"] + markers.data["CMD"])
        elbow_y = markers.data["ACD"] - 0.5 * (markers.data["CLD"] + markers.data["CMD"]) 
        elbow_yz = markers.data["CLD"] - markers.data["CMD"]
        
    elif side == 'L':
        origin = 0.25 * (markers.data["EPSG"] + markers.data["EASG"] + markers.data["ACG"] + markers.data["XPY"])
        y = 0.33 * (markers.data["EPSG"] + markers.data["EASD"] + markers.data["ACG"]) - 0.5 * (markers.data["EPSG"] + markers.data["EASG"])
        yz = markers.data["GLG"] - markers.data["GMG"]
        elbow_origin = 0.5 * (markers.data["CLG"] + markers.data["CMG"])
        elbow_y = markers.data["ACG"] - 0.5 * (markers.data["CLG"] + markers.data["CMG"]) 
        elbow_yz = markers.data["CLG"] - markers.data["CMG"] 
    else:
        raise ValueError("Invalid side specified. Use 'R' or 'L'.")
        

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["hip"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)
    frames.data["elbow"] = ktk.geometry.create_frames(origin=elbow_origin, y=elbow_y, yz=elbow_yz)


    hips_to_elbow = ktk.geometry.get_local_coordinates(frames.data["elbow"], frames.data["hip"])
    euler_angles = ktk.geometry.get_angles(hips_to_elbow, "ZXY", degrees=True)

    # Merge 'markers' and 'frames' TimeSeries objects
    merged_data = ktk.TimeSeries.merge(markers, frames)

    # Set the merged data to the contents using matplotlib
    ktk.Player(merged_data)

# Example usage:
# Specify your arguments accordingly
c3d_filenames = [
    r"C:\Users\idris\Desktop\Meshes\c3d_Data_Tennis\LIGNES\S01_L1_F1.c3d"
] # Provide actual file paths
num_points = obtenir_max_points(c3d_filenames)

# Call the function
get_wristF_handP('R', c3d_filenames, num_points)

get_wristF_handP('L', c3d_filenames, num_points)

# Display the plot if you expect something to be plotted
plt.show()

############

import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
from fun_XprocessData import obtenir_max_points



def get_separation(side, c3d_filenames, num_points):
    # Get hip center based on side
    if side == 'ALL':
        markers = ktk.read_c3d(c3d_filenames[0])["Points"]
        origin = 0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["EPSG"] + markers.data["EASG"])
        y = 0.5 * (markers.data["EASD"] + markers.data["EASG"]) - 0.25 * (markers.data["EPSD"] + markers.data["EASD"] + markers.data["EPSG"] + markers.data["EASG"]) # Marqueurs du fémur et des condyles du genou droit
        yz = markers.data["EASD"] - markers.data["EASG"]
        trunk_origin = 0.5 * (markers.data["ACG"] + markers.data["ACD"])
        trunk_y = 0.5 * (markers.data["C7"] + markers.data["MAN"]) - 0.5 * (markers.data["ACG"] + markers.data["ACD"])
        trunk_yz = markers.data["ACD"] - markers.data["ACG"]  

    else:
        raise ValueError("Invalid side specified. Use 'ALL'.")

    frames = ktk.TimeSeries(time=markers.time)
    frames.data["hip"] = ktk.geometry.create_frames(origin=origin, y=y, yz=yz)  
    frames.data["trunk"] = ktk.geometry.create_frames(origin=trunk_origin, y=trunk_y, yz=trunk_yz) 


# Merge 'markers' and 'frames' TimeSeries objects
    merged_data = ktk.TimeSeries.merge(markers, frames)

    # Set the merged data to the contents using matplotlib
    ktk.Player(merged_data)

# Example usage:
# Specify your arguments accordingly
c3d_filenames = [
    r"C:\Users\idris\Desktop\Meshes\c3d_Data_Tennis\LIGNES\S01_L1_F1.c3d"
] # Provide actual file paths
num_points = obtenir_max_points(c3d_filenames)

# Call the function
get_wristF_handP('R', c3d_filenames, num_points)

get_wristF_handP('L', c3d_filenames, num_points)

# Display the plot if you expect something to be plotted
plt.show()
"""