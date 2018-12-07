import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from plot_spoke import plot_bytearray_spoke

FRAMES = 256
LED_GROUPS=8
LEDS_PER_GROUP=8
LEDS_PER_SIDE=8*8
LEDS_PER_ARM=4*8
center = 9.
length = 32.

spoke_size = int(2*length+center)
size = (spoke_size, spoke_size)

image = Image.open('imgs/rainbow.png')
square_image = image.resize(size)

image_np = np.array(square_image)

# create two arrays of indexes for each possible led position
line = np.arange(center/2,center/2+length)
line = np.concatenate((-line[::-1],line)) # create single line for arm
f = np.arange(0,1,1./FRAMES).reshape((-1,1))
xpos = np.rint(line*np.cos(2*np.pi*f)).flatten().astype(int)
ypos = np.rint(line*np.sin(2*np.pi*f)).flatten().astype(int)

offset = np.abs(np.min(xpos))
xpos = offset+xpos
ypos = offset+ypos
color_list = (image_np[xpos,ypos,:]<133).astype(int) # inverse, since on = 0

# # plot 
# xpos = line*np.cos(2*np.pi*f)
# ypos = line*np.sin(2*np.pi*f)

# fig = plt.figure()
# plt.scatter(xpos,ypos, color=color_list)
# plt.axis('equal')
# plt.show()

# Flip first halve of every line since leds are counted from the center
for i in range(FRAMES):
    j = i*LEDS_PER_SIDE
    color_list[j:j+LEDS_PER_ARM] = color_list[j:j+LEDS_PER_ARM][::-1]

# 1 color per subframe
c_color_list = []
for i in range(FRAMES):
    _begin = i*LEDS_PER_SIDE
    _end = (i+1)*LEDS_PER_SIDE
    _np_frame = color_list[_begin:_end].ravel(order='F')
    _frame_list = _np_frame.reshape((3*LED_GROUPS,8)).tolist()
    for row in _frame_list:
        bytestr = ''.join(str(e) for e in row)
        c_color_list.append(int(bytestr,2))
c_color_list = bytearray(c_color_list)

plot_bytearray_spoke(c_color_list)
