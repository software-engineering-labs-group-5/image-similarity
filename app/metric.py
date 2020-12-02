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
	
