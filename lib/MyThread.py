import threading
import sys,time
from Linker import interface
from db import Model
from Queue import Queue



class MyPercent(object):
	"""docstring for MyPrcent"""
	percentage = 0
	total = 0
	@staticmethod
	def step():
		MyPercent.percentage = MyPercent.percentage + 1
		MyPercent.out()

	@staticmethod
	def out():
		sys.stdout.write('out is {0}/{1}\r'.format(MyPercent.percentage,MyPercent.total))
		sys.stdout.flush()


class MyThread(threading.Thread):
	"""docstring for MyThread"""
	def __init__(self,tasks):
		threading.Thread.__init__(self)
	def run(self):
		web = interface()
		web.execute(tasks.get())
		MyPercent.step()
		time.sleep(0.5)

class ThreadPool(object):
	"""docstring for ThreadPool"""
	def __init__(self, arg ,tasks):
		self.arg = arg
		self.pool = []
		self.tasks = tasks
		self.init()

	def init(self):
		for num in range(self.arg):
			self.pool.append(MyThread(self.tasks))

	def start(self):
		for thread in self.pool:
			thread.start()
		for thread in self.pool:
			thread.join()

def M(table_name):
	global arrModel
	arrModel = {}
	try:
		return arrModel[table_name]
	except:
		arrModel[table_name] = Model(table_name)
		return arrModel[table_name]

		
if __name__ == '__main__':
	tasks = Queue()
	links = M('pages').field('link,page_id').select()
	for link in links:
		tasks.put({"link":link[0],"page_id":link[1]})
	MyPercent.total=tasks.qsize()
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	pool = ThreadPool(5,tasks)
	pool.start()
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
