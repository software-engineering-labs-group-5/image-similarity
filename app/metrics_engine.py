import os
import importlib
import inspect

from metric import Metric

class MetricsEngine():
	
	def __init__(self):
		self.metrics_list = []
		pass

	def load_metrics(self, path):
		try:
			plugins_list = os.listdir(path)
		except:
			try:
				path = path[1:]
				plugins_list = os.listdir(path)
			except:
				try:
					path = path[2:]
					plugins_list = os.listdir(path)
				except:
					raise Exception("No plugins folder found!")
		
		plugins = []
		for plugin in plugins_list:
			if '_metric.py' in plugin:
				if not os.path.isdir(plugin):
					plugins.append(plugin)
		
		if not len(plugins) > 0:
			raise Exception("No plugin in plugins folder found!") 

		for plugin in plugins:
			module_str = f"{path.replace('/', '')}"
			module_str = f"{module_str.replace('.', '')}"
			spec = importlib.util.spec_from_file_location(module_str, f"{path}/{plugin}")
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)

			functions = inspect.getmembers(module, inspect.isfunction)

			for func in functions:
				name, function = func
				if '_metric' in name:
					break

			self.metrics_list.append(Metric(name, function))

	def calculate_metrics(reference_image, modified_image):
		results = {metric.name: metric.compute(img_1, img_2) for metric in engine.metrics_list}
		return results