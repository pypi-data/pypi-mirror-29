from IPython.core.magic import Magics, magics_class, cell_magic
import sys

@magics_class
class WriteFileRun(Magics):
	
	@cell_magic
	def writefile_run(self, line, cell):
		"""Write the contents of a cell to a file, and run the cell.
		
		Usage:
		%%writefile_run <filename> <options>

		Options:
		-a  Append the contents of the cell to an existing file
		-dr Don't run the cell
		"""

		args = line.strip().split(" ")
		args = [a for a in args if len(a)>0]
		if len(args)==0:
			sys.stderr.write("UsageError: the filename is a required argument")
			return

		
		filename = args[0]

		append = '-a' in args
		run = '-dr' not in args

		
		mode = 'a' if append else 'w'

		with open(filename, mode) as f:
			f.write(cell)
		
		if run:
			self.shell.run_cell(cell)


try:
	ip = get_ipython()
	ip.register_magics(WriteFileRun)
except NameError:
	print('Not in IPython, this magic will have no effect')
