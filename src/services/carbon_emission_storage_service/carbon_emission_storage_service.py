import Pyro4

from collections import OrderedDict

class CarbonEmissionStorageService:
    def __init__(self):
        self._vm_to_carbon_emission = {}

    def storeReport(self, vm_id, report):
        vm_report = self._vm_to_carbon_emission.get(vm_id, OrderedDict())
        vm_report[report["timestamp"]] = report
        self._vm_to_carbon_emission[vm_id] = vm_report

    def getReport(self, vm_id):
        if vm_id not in self._vm_to_carbon_emission:
            return []

        return self._vm_to_carbon_emission[vm_id].values()

if __name__ == "__main__":
    daemon = Pyro4.Daemon(host="localhost", port=57654)
    uri = daemon.register(Pyro4.expose(CarbonEmissionStorageService), "CarbonEmissionStorageService")
    print("Ready. Object uri =", uri)

    # Start the event loop of the server to wait for calls
    daemon.requestLoop()
