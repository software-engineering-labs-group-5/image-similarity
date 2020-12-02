import numpy as np
import glob
import metric
import importlib
import os
import inspect

img_1 = np.zeros((3,3,1))
img_2 = np.ones((3,3,1))

metrics_list = []

metrics_list = metric.load_metrics()

print(metrics_list)

for metrick in metrics_list:
	print(metrick.compute(img_1, img_2))
