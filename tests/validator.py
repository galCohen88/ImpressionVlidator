import cv2
import numpy as np

img_rgb = cv2.imread('webpage.png')
pattern = cv2.imread('pattern.png')
h, w = pattern.shape[:-1]

res = cv2.matchTemplate(img_rgb, pattern, cv2.TM_CCOEFF_NORMED)
threshold = .8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (10, 247, 49), 2)

cv2.imwrite('result.png', img_rgb)