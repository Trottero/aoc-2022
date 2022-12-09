import numpy as np


tail = (0, 0)
head = (1, 0)

print(np.rad2deg(np.arctan2(head[0] - tail[0], head[1] - tail[1])))

head2 = (1, 1)
print(f'Expected 45 got: {np.rad2deg(np.arctan2(head2[0] - tail[0], head2[1] - tail[1]))}')

head3 = (0, 1)
print(f'Expected 0 got: {np.rad2deg(np.arctan2(head3[0] - tail[0], head3[1] - tail[1]))}')

head4 = (-1, -1)
print(f'Expected -135 got: {np.rad2deg(np.arctan2(head4[0] - tail[0], head4[1] - tail[1]))}')


head = (2, 4)
tail = (4, 3)

print(f'Expected -45 got: {np.rad2deg(np.arctan2(head[0] - tail[0], head[1] - tail[1]))}')
