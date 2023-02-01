import sys
import numpy as np
from skimage import draw
arr = np.zeros((5, 5))

r0, c0 = 0, 0
r1, c1 = 1, 4
rr, cc = draw.line(r0, c0, r1, c1)

arr[rr, cc] = 1
print(arr)
