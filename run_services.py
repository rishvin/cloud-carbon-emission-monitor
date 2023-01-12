import subprocess
import psutil
import time

from termcolor import colored

if __name__ == '__main__':
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
			"args": ["flask", "run", "--port=50000"],
			"message": "Access the web app at http://localhost:50000"
		},
	]

	print(colored("\n+++++++++++++++++++ Running Services +++++++++++++++++++\n", "yellow"))
	runningServices = []
	for service_info in services_info:
		service = subprocess.Popen(service_info["args"])
		print(colored("Service: {} started with pid: {} ".format(service_info["name"], service.pid), "green"))
		if "message" in service_info:
			print(colored(service_info["message"], "blue"))
		runningServices.append((service_info["name"], service))
		time.sleep(2)

	killedServices = []
	while len(killedServices) < len(runningServices):
		for service_name, service in runningServices:
			if len(killedServices) > 0:
				if service_name not in killedServices:
					service.kill()
					killedServices.append(service_name)
				continue

			psutil_process = psutil.Process(service.pid)
			if not psutil_process.is_running():
				print(colored("FATAL: Service: '{}' stopped running. Killing other services".format(service_name), "red"))
				killedServices.append(service_name)
				continue

			time.sleep(1)

