import multiprocessing
import subprocess
import os
import sys
import psutil
import time

if __name__ == '__main__':
   services_info = [
	("storage_service", "src.services.carbon_emission_storage_service.ephimeral_storage_service"),
	("compute_service", "src.services.carbon_emission_compute_service.mock_compute_service"),
	("analyzer_service", "src.services.carbon_emission_analyzer_service.analyzer_service"),
   ]

runningServices = []
for service_name, service_module in services_info:
	service = subprocess.Popen(["python", "-m", service_module])
	print(service)
	print("Service: {} started with pid: {} ".format(service_name, service.pid))
	runningServices.append((service_name, service))
	time.sleep(1)

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
			print("FATAL: Service: '{}' stopped running. Killing other services".format(service_name))
			killedServices.append(service_name)
			continue

		time.sleep(1)

