import datetime
import enum
import json
import pika
import random
import time
import threading

from carbon_emission_compute_service import CarbonEmissionComputeServiceInterface

class VMMonitoringMockDataGenerator:
    def __init(self):
        pass

    def getMonitoringData(self):
        return {
            "vm_id": "vm-" + str(int(random.uniform(0, 100))),
            "cpu_utilization": random.uniform(0, 100),
            "memory_utilization": random.uniform(0, 100),
            "disk_utilization": random.uniform(0, 100),
            "duration_hours": random.uniform(0, 10000),
            "region": "us-east-1",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class MockCarbonEmissionComputerSerice(CarbonEmissionComputeServiceInterface):
    def __init__(self):
        self._monitoring_data_source = VMMonitoringMockDataGenerator()
        self._conversion_factor = 0.5
        super().__init__()

    def _getNextReport(self):
        time.sleep(1)
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

if __name__ == "__main__":
    mock = MockCarbonEmissionComputerSerice()
    mock.run()
        