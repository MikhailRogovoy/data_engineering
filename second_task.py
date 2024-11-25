import numpy as np
import os.path

matrix = np.load('second_task.npy', 'r')

x, y, z = [], [], []

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if (matrix[i][j] > 520):
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("second_task_result", x=x, y=y, z=z)
np.savez_compressed("second_task_result_compressed", x=x, y=y, z=z)

savez_size = os.path.getsize('second_task_result.npz')
savez_compressed_size = os.path.getsize('second_task_result_compressed.npz')

print(f"savez: {savez_size}")
print(f"savez_compressed: {savez_compressed_size}")
print(f"diff = {savez_size - savez_compressed_size}")