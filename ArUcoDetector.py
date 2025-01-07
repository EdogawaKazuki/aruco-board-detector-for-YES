import cv2
import numpy as np
import os

# Add these as global variables at the top of the file, after imports
home_position = None
home_rotation_matrix = None
camera_position = None
camera_rotation_matrix = None

def load_camera_data(file_path):
    # Load camera matrix and distortion coefficients from a file
    with np.load(file_path) as data:
        camera_matrix = data['camera_matrix']
        dist_coeffs = data['dist_coeffs']
    return camera_matrix, dist_coeffs

def detect_aruco_markers(image, camera_matrix, dist_coeffs):
    global home_position, home_rotation_matrix, camera_position, camera_rotation_matrix
    
    # Clear console before new output
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load the dictionary that was used to generate the markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()

    # Create ArUco board
    board = cv2.aruco.GridBoard(
        (5, 7),
        0.03,
        0.01,
        aruco_dict
    )

    # Detect the markers in the image
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    if ids is not None:
        # Estimate the board pose
        retval, rvec, tvec = cv2.aruco.estimatePoseBoard(
            corners, ids, board, camera_matrix, dist_coeffs, None, None
        )

        if retval:
            # Draw board axis
            cv2.drawFrameAxes(image, camera_matrix, dist_coeffs, rvec, tvec, 0.1)
            cv2.aruco.drawDetectedMarkers(image, corners, ids)
            
            # Convert board rotation vector to rotation matrix
            rmat, _ = cv2.Rodrigues(rvec)
            
            # Calculate camera position (inverse transform)
            camera_position = -np.matrix(rmat).T * np.matrix(tvec)
            
            # Camera rotation is inverse of board rotation
            camera_rotation_matrix = rmat.T
            camera_rotation_vec, _ = cv2.Rodrigues(camera_rotation_matrix)
            
            # Convert rotation matrix to Euler angles (in radians)
            # Order of rotations: yaw (Y), pitch (X), roll (Z)
            pitch = np.arctan2(-camera_rotation_matrix[2,0], 
                             np.sqrt(camera_rotation_matrix[2,1]**2 + camera_rotation_matrix[2,2]**2))
            yaw = np.arctan2(camera_rotation_matrix[2,1], camera_rotation_matrix[2,2])
            roll = np.arctan2(camera_rotation_matrix[1,0], camera_rotation_matrix[0,0])
            
            # Convert to degrees
            yaw_deg = np.degrees(yaw)
            pitch_deg = np.degrees(pitch)
            roll_deg = np.degrees(roll)
            
            # Store current position and rotation for relative calculations
            current_position = camera_position
            current_rotation_matrix = camera_rotation_matrix
            
            # Calculate relative position and rotation if home is set
            if home_position is not None:
                relative_position = current_position - home_position
                relative_rotation = current_rotation_matrix @ home_rotation_matrix.T
                
                # Convert relative rotation to euler angles
                pitch = np.arctan2(-relative_rotation[2,0], 
                                 np.sqrt(relative_rotation[2,1]**2 + relative_rotation[2,2]**2))
                yaw = np.arctan2(relative_rotation[2,1], relative_rotation[2,2])
                roll = np.arctan2(relative_rotation[1,0], relative_rotation[0,0])
                
                # Convert to degrees
                rel_yaw_deg = np.degrees(yaw)
                rel_pitch_deg = np.degrees(pitch)
                rel_roll_deg = np.degrees(roll)
                
                print(f"Current camera position: {camera_position.flatten()}")
                print(f"Current camera angles (degrees):")
                print(f"  Yaw (Y-axis): {yaw_deg:.2f}")
                print(f"  Pitch (X-axis): {pitch_deg:.2f}")
                print(f"  Roll (Z-axis): {roll_deg:.2f}")
                print("\nRelative to home:")
                print(f"Position: {relative_position.flatten()}")
                print(f"Angles (degrees):")
                print(f"  Yaw: {rel_yaw_deg:.2f}")
                print(f"  Pitch: {rel_pitch_deg:.2f}")
                print(f"  Roll: {rel_roll_deg:.2f}")
            else:
                print(f"Camera position: {camera_position.flatten()}")
                print(f"Camera angles (degrees):")
                print(f"  Yaw (Y-axis): {yaw_deg:.2f}")
                print(f"  Pitch (X-axis): {pitch_deg:.2f}")
                print(f"  Roll (Z-axis): {roll_deg:.2f}")
                print("\nPress 'h' to set home position")
    else:
        print("No ArUco markers detected")

    return image

# Load camera data from file
camera_matrix, dist_coeffs = load_camera_data('calibration_data.npz')

print("camera_matrix: ", camera_matrix)
print("dist_coeffs: ", dist_coeffs)
print("Camera Calibration Loaded")

# open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    output_image = detect_aruco_markers(frame, camera_matrix, dist_coeffs)
    cv2.imshow('Detected ArUco markers', output_image)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('h'):
        if 'camera_position' in locals() and 'camera_rotation_matrix' in locals():
            home_position = camera_position
            home_rotation_matrix = camera_rotation_matrix
            print("\nHome position set!")
    elif key == ord('q'):  # Add a quit option
        break

cap.release()
cv2.destroyAllWindows()
