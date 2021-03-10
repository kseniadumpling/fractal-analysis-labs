import cv2


def grayscale_img(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    cv2.imshow(path, img)
    cv2.waitKey(0)
    cv2.imwrite(path, img)


path = "../palette.jpg"
grayscale_img(path)
