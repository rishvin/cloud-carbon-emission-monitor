import Pyro4
import sys

from termcolor import colored
from collections import OrderedDict

service_memory = {}

class CarbonEmissionStorageService:
    def __init__(self, provider_memory=None):
        self._vm_to_carbon_emission = provider_memory if provider_memory else service_memory

    def storeReport(self, vm_id, report):
        vm_report = self._vm_to_carbon_emission.get(vm_id, OrderedDict())
        vm_report[report["timestamp"]] = report
        self._vm_to_carbon_emission[vm_id] = vm_report

    def listVMs(self):
        return list(self._vm_to_carbon_emission.keys())

    def getReport(self, vm_id):
        if vm_id not in self._vm_to_carbon_emission:
            return []

        return list(self._vm_to_carbon_emission[vm_id].values())

if __name__ == "__main__":
    daemon = Pyro4.Daemon(port=57654)
    uri = daemon.register(Pyro4.expose(CarbonEmissionStorageService), "CarbonEmissionStorageService")
    print(colored("Running ephimeral storage service at url: {}".format(daemon), "yellow"))
    daemon.requestLoop()
