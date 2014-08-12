def compile(color):
	options = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
	index = options.index(color)
	if index == -1:
		raise 'non-supported color'
	else:
		return index + 30

def color_with_code(text, code):
	return "\033[" + str(code) + "m" + text + "\033[0m"

def color(text, color):
	code = compile(color)
	return color_with_code(text, code)


class Printer:
	master = None

	def __init__(self):
		self.indentation = 0
		if not Printer.master:
			Printer.master = self

	def output(self, text):
		print self.indentation * '\t' + text

	def indent(self):
		self.indentation += 1

	def dedent(self):
		if self.indentation == 0:
			raise 'negative indentation'
		self.indentation -= 1

	def write(self, text):
		self.output(self.indentation * '\t' + text)

	def success(self, text):
		self.output(color(text, 'green'))

	def inform(self, text):
		self.output(text)

	def warn(self, text):
		self.output(color(text, 'yellow'))

	def throw(self, text):
		self.output(color(text, 'red'))


def master():
	if not Printer.master:
		Printer.master = Printer()
	return Printer.master

def master_printer():
	return master()