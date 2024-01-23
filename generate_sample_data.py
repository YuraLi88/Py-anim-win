import numpy as np
import pandas as pd
import os
# Parameters for the sin wave
num_frames = 200
num_points = 100
x = np.linspace(0, 2 * np.pi, num_points)  # One period of the sine wave
path = 'data'
os.makedirs(path, exist_ok=True)
# Generating the data
for frame in range(num_frames):
    print(frame)
    y = np.sin(x - frame * np.pi / num_frames)*np.exp(-0.2*frame * np.pi / num_frames)  # Shifting the sin wave for each frame
    np.savetxt(f'{path}/frame{frame:03}.dat', np.c_[x,y])
    # data = pd.DataFrame({'x': x, 'y': y})
    # data.to_csv(f'frame{frame:03}.dat', sep='\t', index=False)  # Saving each frame as a .dat file

