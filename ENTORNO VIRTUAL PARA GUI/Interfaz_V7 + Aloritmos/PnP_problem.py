import numpy as np
import cv2 as cv
from enum import Enum
import time

class DrawOption(Enum):
    AXES = 1
    CUBE = 2

def drawAxes(img, corners, imgpts):
    def tupleOfInts(arr):
        return tuple(int(x) for x in arr)

    corner = tupleOfInts(corners[0].ravel())
    img = cv.line(img, corner, tupleOfInts(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv.line(img, corner, tupleOfInts(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv.line(img, corner, tupleOfInts(imgpts[2].ravel()), (0, 0, 255), 5)
    return img

def drawCube(img, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # Add green plane
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    # Add box borders
    for i in range(4):
        j = i + 4
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
        img = cv.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)
    return img


def rotate_cube(cube_corners, rvec, origin_vertex):
    # Translate cube corners to set origin_vertex as the origin
    translated_cube_corners = cube_corners - cube_corners[origin_vertex]

    # Convert rotation vector to rotation matrix
    R, _ = cv.Rodrigues(rvec)

    # Apply rotation to translated cube points
    rotated_translated_cube_corners = np.dot(R, translated_cube_corners.T).T

    # Translate back to the original position
    rotated_cube_corners = rotated_translated_cube_corners + cube_corners[origin_vertex]

    return rotated_cube_corners

def calculate_cube_side_lengths(cube_corners):
    # Calcular las distancias entre los puntos
    distances = []
    for i in range(4):
        distances.append(np.linalg.norm(cube_corners[i] - cube_corners[(i + 1) % 4]))  # Lados del plano XY
        distances.append(np.linalg.norm(cube_corners[i + 4] - cube_corners[(i + 1) % 4 + 4]))  # Lados del plano XY
        distances.append(np.linalg.norm(cube_corners[i] - cube_corners[i + 4]))  # Conecta los dos planos

    return distances

def poseEstimation(option: DrawOption, video_capture):
    camMatrix = np.array([[675.19156976, 0, 327.98559774],
                           [0, 676.03397821, 243.42532395],
                           [0, 0, 1]])
    distCoeff = np.array([[0.10306693, -1.12841865, 0.0027022, 0.00406938, 2.14339482]])

    # Initialize
    nRows = 7
    nCols = 7
    termCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    worldPtsCur = np.zeros((nRows * nCols, 3), np.float32)
    worldPtsCur[:, :2] = np.mgrid[0:nRows, 0:nCols].T.reshape(-1, 2)

    # World points of objects to be drawn
    axis = np.float32([[6, 0, 0], [0, 6, 0], [0, 0, -6]])
    cubeCorners = np.float32([[0,0,0],[0,6,0],[6,6,0],[6,0,0],
                       [0,0,-6],[0,6,-6],[6,6,-6],[6,0,-6]])
    # Define la distancia entre los cuadrados del tablero de ajedrez en centímetros
    square_distance_cm = 1.7

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        imgGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cornersFound, cornersOrg = cv.findChessboardCorners(imgGray, (nRows, nCols), None)

        if cornersFound:
            cornersRefined = cv.cornerSubPix(imgGray, cornersOrg, (11, 11), (-1, -1), termCriteria)
            _, rvecs, tvecs = cv.solvePnP(worldPtsCur, cornersRefined, camMatrix, distCoeff)

            if option == DrawOption.AXES:
                imgpts, _ = cv.projectPoints(axis, rvecs, tvecs, camMatrix, distCoeff)
                frame = drawAxes(frame, cornersRefined, imgpts)

            if option == DrawOption.CUBE:
                imgpts, _ = cv.projectPoints(cubeCorners, rvecs, tvecs, camMatrix, distCoeff)
                frame = drawCube(frame, imgpts)

                # Convert rvec to numpy array for rotation
                rvec_np = np.array(rvecs)
                # Rotate the cube
                rotated_cube_corners = rotate_cube(cubeCorners, rvec_np,4)

                # Calculate side lengths of the rotated cube
                side_lengths = calculate_cube_side_lengths(rotated_cube_corners)
                total_side_length = sum(side_lengths)

                # Estima la distancia en centímetros
                distance_cm = np.linalg.norm(tvecs) *square_distance_cm
                # Dibuja la distancia estimada en la imagen
                cv.putText(frame, f'Distance: {distance_cm:.2f} cm', (20, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

        time.sleep(0.2)

        cv.imshow('Chessboard', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    video_capture = cv.VideoCapture(0)
    poseEstimation(DrawOption.CUBE, video_capture)
    video_capture.release()
    cv.destroyAllWindows()
