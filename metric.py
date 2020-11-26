import numpy as np
import glob
import metric
import importlib
import os
import inspect

class Metric():
	def __init__(self, name, computation):
		self.name = name
		self.compute = computation
	
def load_metrics():
	metrics_list = []
	path = os.getcwd()
	path = path + '\metrics'
	plugins = os.listdir(path)

	for plugin in plugins:
		if '_metric.py' not in plugin:
			plugins.remove(plugin)
			continue
		module_str = 'metrics.' + plugin
		module_str = module_str[:-3] 
		module = importlib.import_module(module_str)

		functions = inspect.getmembers(module, inspect.isfunction)
		name, function = functions[0]

		metrics_list.append(metric.Metric(name, function))
	return metrics_list