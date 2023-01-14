import datetime
import enum
import json
import pika
import random
import time
import threading
import sys
import os

class CarbonEmissionComputeServiceInterface:
    def __init__(self):
        self._queue_name = "carbon_emission_compute_queue"
        url = os.environ.get('CLOUDAMQP_URL', "amqp://guest:guest@localhost:5672/%2f")
        params = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue_name)
    
    def _publishReport(self, carbon_emission):
        self._channel.basic_publish(
            exchange='', 
            routing_key=self._queue_name, 
            body=json.dumps(carbon_emission))
    
    def _getNextReport(self):
        pass
    
    def run(self):
        while True:
            emission_report = self._getNextReport()
            self._publishReport(emission_report)
        

class VmCarbonEmissionComputerService(CarbonEmissionComputeServiceInterface):
    def __init__(self, vm_monitoring_data_source):
        self._monitoring_data_source = vm_monitoring_data_source
        self._conversion_factor = 0.5
        super().__init__()

    def _getNextReport(self):
        vm_data = self._monitoring_data_source.getMonitoringData()
        power_usage = ((vm_data["cpu_utilization"] * 100) +
                       (vm_data["memory_utilization"] * 50) + 
                       (vm_data["disk_utilization"] * 20))

        hardware_emissions = power_usage * self._conversion_factor / 3600
        carbon_emission = (hardware_emissions *
                          (vm_data["cpu_utilization"] / 100) * 
                          (vm_data["memory_utilization"] / 100) * 
                          (vm_data["disk_utilization"] / 100))
        
        return {
            "resource_type": "vm",
            "carbon_emission_per_second": carbon_emission,
            "vm_id": vm_data["vm_id"],
            "region": vm_data["region"],
            "timestamp": vm_data["timestamp"]
        }

class VmMonitoringDataGenerator:
    def __init(self):
        pass

    def getMonitoringData(self):
        time.sleep(1)
        return {
            "vm_id": "vm-" + str(int(random.uniform(0, 100))),
            "cpu_utilization": random.uniform(0, 100),
            "memory_utilization": random.uniform(0, 100),
            "disk_utilization": random.uniform(0, 100),
            "duration_hours": random.uniform(0, 10000),
            "region": "us-east-1",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    compute_service = VmCarbonEmissionComputerService(VmMonitoringDataGenerator())
    compute_service.run()
        
