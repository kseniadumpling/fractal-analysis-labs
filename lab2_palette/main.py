import cv2


def show_blue(img):
    img_blue = img.copy()

    img_blue[:, :, 1] = 0
    img_blue[:, :, 2] = 0

    cv2.imshow("blue", img_blue)
    cv2.waitKey(0)


def show_green(img):
    img_green = img.copy()

    img_green[:, :, 0] = 0
    img_green[:, :, 2] = 0

    cv2.imshow("green", img_green)
    cv2.waitKey(0)


def show_red(img):
    img_red = img.copy()

    img_red[:, :, 0] = 0
    img_red[:, :, 1] = 0

    cv2.imshow("red", img_red)
    cv2.waitKey(0)


path = "../palette.jpg"

image = cv2.imread(path)

show_blue(image)
show_green(image)
show_red(image)
