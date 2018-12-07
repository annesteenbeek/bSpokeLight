import matplotlib.pyplot as plt
import numpy as np

# f = open("star.bin", 'r')
# f = open("rainbow.bin", 'r')
# image=bytearray(f.read())
# f.close()


def plot_bytearray_spoke(image):
    FRAMES = 256
    LED_GROUPS=8
    LEDS_PER_GROUP=8
    COLORS=3
    CENTER = 32
    center = 9.

    led_states = np.empty([FRAMES, LED_GROUPS*LEDS_PER_GROUP,COLORS])
    frame = 0 # start frame
    for frame in range(0,FRAMES):
        g = frame*8*3
        for color in range(3):
        # iterate over rgb colors
            g = frame*8*3+color*8 # R/G/B
            for block, j in enumerate(range(g, g+8)): 
                # Iterate over the 8 blocks of leds
                # 0 1 2 3 are the left side from the middle
                # 4 5 6 7 are the right side from the middle
                led_block = bin(image[j])[2:].zfill(8)
                for bit, state in enumerate(led_block):
                    if block < 4:
                        strip_index = CENTER-(LEDS_PER_GROUP*block+bit)-1
                    else:
                        strip_index = CENTER+(LEDS_PER_GROUP*(block-4)+bit)
                    led_states[frame,strip_index,color]=1.-float(state)

    row = np.arange(center/2,center/2+32)
    row = np.concatenate((-row[::-1],row))
    f = np.arange(0,1,1./FRAMES).reshape((-1,1))
    xpos = (row*np.cos(2*np.pi*f)).flatten()
    ypos = (row*np.sin(2*np.pi*f)).flatten()
    color_list = led_states.reshape((-1,3))

    fig = plt.figure()
    plt.scatter(xpos,ypos, color=color_list)
    plt.axis('equal')
    plt.show()


# plot_bytearray_spoke(image)