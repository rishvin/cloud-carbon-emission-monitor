import subprocess
import psutil
import time
import atexit
import sys

from termcolor import colored

if __name__ == '__main__':
	runningServices = []

	def cleanup():
		for service_name, service in runningServices:
			try:
				service.kill()
				print(colored("Killed service: {}".format(service_name), "red"))
			except Exception as ex:
				pass
	
	atexit.register(cleanup)
	
	services_info = [
		{
			"name": "storage_service", 
			"args": ["python", "-m", "src.services.carbon_emission_storage_service.ephimeral_storage_service"]
		},
		{
			"name": "compute_service", 
			"args": ["python", "-m", "src.services.carbon_emission_compute_service.vm_compute_service"]
		},
		{
			"name": "analyzer_service", 
			"args": ["python", "-m", "src.services.carbon_emission_analyzer_service.analyzer_service"]
		},
		{
			"name": "carbon_emission_web_app", 
			"args": ["python", "-m", "src.apps.carbon_emission_app"],
			"message": "Follow the flask app link to access the app."
		},
	]

	print(colored("\n+++++++++++++++++++ Running Services +++++++++++++++++++\n", "yellow"))
	for service_info in services_info:
		service = subprocess.Popen(service_info["args"])
		print(colored("Service: {} started with pid: {} ".format(service_info["name"], service.pid), "green"))
		if "message" in service_info:
			print(colored(service_info["message"], "blue"))
		runningServices.append((service_info["name"], service))
		time.sleep(2)
	
	while True:
		for service_name, service in runningServices:
			time.sleep(1)
			
			psutil_process = psutil.Process(service.pid)
			if not psutil_process.is_running() or psutil_process.status() == psutil.STATUS_ZOMBIE:
				print(colored("FATAL: Service: '{}' stopped running. Killing other services".format(service_name), "red"))
				sys.exit(1)