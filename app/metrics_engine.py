import metric

class MetricsEngine():
	
	def __init__(self):
		self.metrics_list = []
		pass

	def load_metrics(self, path):
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

			self.metrics_list.append(metric.Metric(name, function))
