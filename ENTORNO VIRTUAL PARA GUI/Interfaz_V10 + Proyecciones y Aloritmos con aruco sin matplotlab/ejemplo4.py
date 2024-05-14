import numpy as np
import cv2

# Datos de los cuadrados
data_1 = {'rvecs': np.array([[[ 1.99887477, -2.21877817,  0.08552004]]]), 'tvecs': np.array([[[-0.12211195, -0.09585458,  0.48435917]]]), 'corners_reales': [(106, 137), (104, 72), (172, 60), (179, 132)]}
data_2 = {'rvecs': np.array([[[-2.05046621, -2.18125333,  0.21551142]]]), 'tvecs': np.array([[[-0.1023936 , -0.07732863,  0.42136772]]]), 'corners_reales': [(105, 362), (105, 284), (187, 279), (189, 357)]}
data_3 = {'rvecs': np.array([[[-1.53943376,  1.65806193,  0.03953506]]]), 'tvecs': np.array([[[-0.16235047, -0.10557457,  0.46894231]]]), 'corners_reales': [(251, 121), (245, 51), (319, 42), (323, 109)]}
data_4 = {'rvecs': np.array([[[ 2.12067084, -2.32900786,  0.03300034]]]), 'tvecs': np.array([[[-0.14026687, -0.08959012,  0.44441734]]]), 'corners_reales': [(270, 350), (265, 273), (341, 265), (349, 343)]}

# Promedio de los parámetros de rotación y traslación
rvecs_avg = np.mean([data_1['rvecs'], data_2['rvecs'], data_3['rvecs'], data_4['rvecs']], axis=0)
tvecs_avg = np.mean([data_1['tvecs'], data_2['tvecs'], data_3['tvecs'], data_4['tvecs']], axis=0)

# Convertir los vectores de rotación a matrices de rotación
rotation_matrices = [cv2.Rodrigues(rvecs)[0] for rvecs in rvecs_avg]

# Sumar las matrices de rotación
rotation_matrix_avg = np.mean(rotation_matrices, axis=0)

# Combinar la matriz de rotación promediada con la matriz de traslación promediada
H_avg = np.hstack((rotation_matrix_avg, tvecs_avg.reshape(3,1)))

# Imprimir la matriz de transformación promediada
print("Matriz de transformación promediada:")
print(H_avg)
