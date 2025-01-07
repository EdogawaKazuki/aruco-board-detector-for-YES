import cv2
import cv2.aruco as aruco
import math

def generate_aruco_marker(marker_id, marker_size_mm, screen_resolution, screen_diagonal_inches, aruco_dict_type):
    
    screen_size_mm = screen_diagonal_inches * 25.4

    # Calculate the aspect ratio of the monitor
    aspect_ratio = screen_resolution[0] / screen_resolution[1]

    # Calculate the physical width and height in millimeters
    monitor_physical_width = (screen_size_mm ** 2 / (1 + aspect_ratio ** 2)) ** 0.5 * aspect_ratio
    monitor_physical_height = monitor_physical_width / aspect_ratio

    # Calculate the pixel size per millimeter for both dimensions
    pixel_width_per_mm = screen_resolution[0] / monitor_physical_width
    pixel_height_per_mm = screen_resolution[1] / monitor_physical_height

    # Calculate marker size in pixels
    marker_size_pixels = int(marker_size_mm * pixel_width_per_mm)

    # Define the dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)

    # Generate the marker
    marker_image = aruco.generateImageMarker(aruco_dict, marker_id, marker_size_pixels)

    # Create a window to display the marker
    cv2.namedWindow('ArUco Marker', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ArUco Marker', marker_size_pixels, marker_size_pixels)

    # Display the marker
    cv2.imshow('ArUco Marker', marker_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_aruco_board(board_width, board_height, marker_size_mm, marker_separation_mm, screen_resolution, screen_diagonal_inches, aruco_dict_type):
    screen_size_mm = screen_diagonal_inches * 25.4

    # Calculate the aspect ratio of the monitor
    aspect_ratio = screen_resolution[0] / screen_resolution[1]

    # Calculate the physical width and height in millimeters
    monitor_physical_width = (screen_size_mm ** 2 / (1 + aspect_ratio ** 2)) ** 0.5 * aspect_ratio

    # Calculate the pixel size per millimeter for both dimensions
    pixel_width_per_mm = screen_resolution[0] / monitor_physical_width

    # Calculate marker size and separation in pixels
    marker_size_pixels = int(marker_size_mm * pixel_width_per_mm)
    marker_separation_pixels = int(marker_separation_mm * pixel_width_per_mm)

    # Define the dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)

    # Create the board
    board = cv2.aruco.GridBoard((board_width, board_height), 
                               marker_size_mm,
                               marker_separation_mm,
                               aruco_dict)

    # Calculate the board image size
    board_width_pixels = board_width * marker_size_pixels + (board_width - 1) * marker_separation_pixels
    board_height_pixels = board_height * marker_size_pixels + (board_height - 1) * marker_separation_pixels
    
    # Draw the board (reducing margin and border size)
    margin_size = 5
    boarder_bits = 1
    board_image = cv2.aruco.drawPlanarBoard(board, 
                                          (board_width_pixels, board_height_pixels),
                                          margin_size,
                                          boarder_bits)

    # Create a window to display the board
    cv2.namedWindow('ArUco Board', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ArUco Board', board_image.shape[1], board_image.shape[0])

    # Display the board
    cv2.imshow('ArUco Board', board_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
screen_resolution = (1920, 1080)  # Screen resolution in pixels (width, height)
screen_diagonal_inches = 24  # Diagonal screen size in inches
marker_size_mm = 30  # Desired marker size in millimeters
marker_separation_mm = 10  # Separation between markers in millimeters
aruco_dict_type = aruco.DICT_4X4_50  # ArUco dictionary type

# generate_aruco_marker(marker_id=42, marker_size_mm=marker_size_mm, 
#                       screen_resolution=screen_resolution, screen_diagonal_inches=screen_diagonal_inches,
#                       aruco_dict_type=aruco_dict_type)

generate_aruco_board(board_width=5, board_height=7, marker_size_mm=marker_size_mm, 
                     marker_separation_mm=marker_separation_mm, screen_resolution=screen_resolution, 
                     screen_diagonal_inches=screen_diagonal_inches, aruco_dict_type=aruco_dict_type)
