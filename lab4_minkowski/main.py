import cv2
import numpy as np


# верхняя поверхность u_δ(i,j)
def calcuate_u(img, max_delta):
    width, height = img.shape
    u = np.zeros((max_delta + 1, width + 1, height + 1))

    for i in range(0, width):
        for j in range(0, height):
            u[0][i][j] = img[i][j]
            for d in range(1, max_delta + 1):
                u[d][i][j] = max(u[d-1][i][j] + 1,
                                 max(u[d-1][i+1][j+1], u[d-1][i-1][j+1],
                                     u[d-1][i+1][j-1], u[d-1][i-1][j-1]))
    return u


# нижняя повехность b_δ(i,j)
def calcuate_b(img, max_delta):
    width, height = img.shape
    b = np.zeros((max_delta + 1, width + 1, height + 1))

    for i in range(0, width):
        for j in range(0, height):
            b[0][i][j] = img[i][j]
            for d in range(1, max_delta + 1):
                b[d][i][j] = min(b[d-1][i][j] - 1,
                                 min(b[d-1][i+1][j+1], b[d-1][i-1][j+1],
                                     b[d-1][i+1][j-1], b[d-1][i-1][j-1]))
    return b


# объем δ-параллельного тела
def calcuate_vol(img, max_delta):
    width, height = img.shape
    u = calcuate_u(img, max_delta)
    b = calcuate_b(img, max_delta)
    vol = np.zeros(max_delta + 1)

    for d in range(1, max_delta + 1):
        sum = 0
        for i in range(0, width):
            for j in range(0, height):
                sum += u[d][i][j] - b[d][i][j]
        vol[d] = sum

    return vol


# площадь поверхности фрактала А_δ
def calculate_A(img, max_delta):
    A = np.zeros(max_delta + 1)
    vol = calcuate_vol(img, max_delta)

    for d in range(1, max_delta + 1):
        A[d] = (vol[d] - vol[d-1]) / 2

    return A


# фрактальная размерность
def calculate_D(img_path, max_delta, cell_size):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    width, height = img.shape

    cell_width = int(width / cell_size)
    cell_heigth = int(height / cell_size)
    A = np.zeros((cell_width, cell_heigth, max_delta + 1))

    for i in range(0, cell_width):
        for j in range(0, cell_heigth):
            cell_img = img[j*cell_size:cell_size *
                           (j+1), i*cell_size:cell_size*(i+1)]
            a = calculate_A(cell_img, max_delta)
            for d in range(1, max_delta + 1):
                A[i][j][d] = a[d]

    sum_A = []
    for d in range(1, max_delta + 1):
        sum = 0
        for i in range(0, cell_width):
            for j in range(0, cell_heigth):
                sum += A[i][j][d]
        sum_A.append(sum)

    return 2 - np.polyfit(np.log(sum_A), np.log(np.arange(1, max_delta+1)), 1)[0] * (-1)


paths = ["../koch.png", "../sierpinski.png", "../bricks1.png"]
for path in paths:
    res = calculate_D(path, 2, 100)
    print("{:20}: {}".format(path, res))
