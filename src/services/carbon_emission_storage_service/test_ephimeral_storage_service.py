import pytest

from .ephimeral_storage_service import CarbonEmissionStorageService

@pytest.fixture
def carbon_service():
    return CarbonEmissionStorageService()

def test_store_report(carbon_service):
    vm_id = "vm1"
    report = {"timestamp": "2022-01-01 12:00:00", "emissions": 100}
    carbon_service.storeReport(vm_id, report)
    assert vm_id in carbon_service.listVMs()
    stored_report = carbon_service.getReport(vm_id)
    assert len(stored_report) == 1
    print(stored_report)
    assert stored_report[0] == report

def test_list_vms(carbon_service):
    carbon_service.storeReport("vm1", {"timestamp": "2022-01-01 12:00:00", "emissions": 100})
    carbon_service.storeReport("vm2", {"timestamp": "2022-01-01 12:00:00", "emissions": 200})
    carbon_service.storeReport("vm3", {"timestamp": "2022-01-01 12:00:00", "emissions": 300})
    assert set(carbon_service.listVMs()) == {"vm1", "vm2", "vm3"}

def test_get_report(carbon_service):
    vm_id = "vm1"
    carbon_service.storeReport(vm_id, {"timestamp": "2022-01-01 12:00:00", "emissions": 100})
    carbon_service.storeReport(vm_id, {"timestamp": "2022-01-01 12:00:01", "emissions": 200})
    stored_reports = carbon_service.getReport(vm_id)
    assert len(stored_reports) == 2
    assert stored_reports[0]["emissions"] == 100
    assert stored_reports[1]["emissions"] == 200
