import json
import time
import pytest
import subprocess
import requests
import Pyro4

from collections import OrderedDict

@pytest.fixture(scope="session")
def services():
    services_infos = [
        {
            "args": ["python", "-m", "src.services.carbon_emission_storage_service.ephimeral_storage_service"]
        },
        {
            "args": ["python", "-m", "src.services.carbon_emission_compute_service.vm_compute_service"]
        },
        {
            "args": ["python", "-m", "src.services.carbon_emission_analyzer_service.analyzer_service"]
        },
    ]
    
    runningServices = []
    for service_info in services_infos:
        service = subprocess.Popen(service_info["args"])
        runningServices.append(service)
        time.sleep(0.5)

    yield runningServices

    for service in runningServices:
        service.kill()

def test_list_and_get_report(services):
    running_services = services
    time.sleep(1)

    storage_service = Pyro4.Proxy(uri = "PYRO:CarbonEmissionStorageService@localhost:57654")
    try:
        vms = storage_service.listVMs()
        assert len(vms) > 0
    except:
        assert False

    try:
        report = storage_service.getReport(vms[0])
        assert len(report) > 0
        assert "resource_type" in report[0]
        assert "carbon_emission_per_second" in report[0]
        assert "carbon_emission_rate" in report[0]
        assert "timestamp" in report[0]
        assert "vm_id" in report[0]
        assert "region" in report[0]
    except:
        assert False