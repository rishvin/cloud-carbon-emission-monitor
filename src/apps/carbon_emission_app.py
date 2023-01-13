import json
import Pyro4

from flask import Flask, request
from os import environ
from termcolor import colored

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    <h1> Cloud Carbon Emission App </h1>
    <div>
        <form action="/list_vms" method="GET">
            <input type="submit" value="List VMs">
        </form>
    </div>
    <div>
        <p> Enter the VM to get its carbon emission data </p>
        <form action="/vm_carbon_emission" method="POST">
            <input name="vm_carbon_emission">
            <input type="submit" value="Get Carbon Emission">
        </form>
    </div>
     '''

@app.route("/list_vms", methods=["GET"])
def list_vms():
    storage_service = Pyro4.Proxy(uri = "PYRO:CarbonEmissionStorageService@localhost:57654")
    try:
        return json.dumps(storage_service.listVMs(), indent=4)
    except Exception as ex:
        print(colored("Error while listing VMs, reason: {}".format(ex), "red"))
        return "VMs list cannot be retrieved at the moment, please try again later."

@app.route("/vm_carbon_emission", methods=["POST"])
def vm_carbon_emission():
    vm_id = request.form.get("vm_carbon_emission", "")
    if not vm_id:
        return "You did not enter any VM ID"

    storage_service = Pyro4.Proxy(uri = "PYRO:CarbonEmissionStorageService@localhost:57654")
    try:
        return json.dumps(storage_service.getReport(vm_id), indent=4)
    except Exception as ex:
        print(colored("Error while retrieving report for vm-id: {}, reason: {}".format(vm_id, ex), "red"))
        return "Carbon emission report for vm-id: {} cannot be retrieved at the moment, please try again later.".format(vm_id)

if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0', port=environ.get("PORT", 5000))