import Pyro4

from termcolor import colored
from collections import OrderedDict

vm_to_carbon_emission = {}

class CarbonEmissionStorageService:
    def __init__(self):
        vm_to_carbon_emission = {}

    def storeReport(self, vm_id, report):
        vm_report = vm_to_carbon_emission.get(vm_id, OrderedDict())
        vm_report[report["timestamp"]] = report
        vm_to_carbon_emission[vm_id] = vm_report

    def getReport(self, vm_id):
        if vm_id not in vm_to_carbon_emission:
            return []

        return vm_to_carbon_emission[vm_id].values()

if __name__ == "__main__":
    daemon = Pyro4.Daemon(port=57654)
    uri = daemon.register(Pyro4.expose(CarbonEmissionStorageService), "CarbonEmissionStorageService")
    print(colored("Running ephimeral storage service at url: {}".format(daemon), "yellow"))
    daemon.requestLoop()
