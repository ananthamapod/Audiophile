import requests
import secrets
import time

class Audiophile_Client(object):
	def __init__(self):
		self.session = requests.session()
	
	def connect(self):
		p = self.session.post("http://0.0.0.0:5000/login", {'id': secrets.robot_id})
		print p.text

	def new_project(self, name):
		p = self.session.post("http://0.0.0.0:5000/new", {'name': name})
		print p.text
		return p.text

	def send_data(self, tSeries, coords):
		p = self.session.post("http://0.0.0.0:5000/add", {'coords': coords, 'tSeries': tSeries})
		print p.text
		return p.text

if __name__ == "__main__":
	a = Audiophile_Client()
	a.connect()
	a.new_project('Audiophile')
	for i in range(4):
		time.sleep(1)
		a.send_data(i*10,i)

