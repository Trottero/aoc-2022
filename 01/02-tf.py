import numpy as np
import tensorflow as tf
import time

print(tf.config.list_physical_devices('GPU'))

agg = []
lines = []
with open ('./01/input.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            lines.append(agg)
            agg = []
            continue
        agg.append(int(line))

max_length = max([len(line) for line in lines])
lines = [line + [0] * (max_length - len(line)) for line in lines]

tensor = tf.constant(lines, dtype=tf.int32)
print(tensor.device)

print(tensor.shape)

start = time.perf_counter()
sum_per_elf = tf.reduce_sum(tensor, axis=1)
final_sum = tf.reduce_sum(tf.sort(sum_per_elf, direction='DESCENDING')[:3])
print(final_sum)
print(time.perf_counter() - start)