import pika
import json
import Pyro4

from src.services.carbon_emission_storage_service.ephimeral_storage_service import CarbonEmissionStorageService

class CabonEmissionAnalyzerService:
    def __init__(self):
        self._queue_name = "carbon_emission_compute_queue"
        self._connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue_name)
        self._storage_service = Pyro4.Proxy(uri = "PYRO:CarbonEmissionStorageService@localhost:57654")

    def _analyzeAndPersistReport(self, channel, method, properties, report):
        if not report:
            return
        
        emission_report = json.loads(report)
        if emission_report["carbon_emission_per_second"] > 0.5:
            emission_report["carbon_emission_rate"] = "high"
        elif emission_report["carbon_emission_per_second"] > 0.1:
            emission_report["carbon_emission_rate"] = "medium"
        else:
            emission_report["carbon_emission_rate"] = "low"

        self._storage_service.storeReport(emission_report["vm_id"], emission_report)
        print("Analyzed report for vm_id =", emission_report)

    def run(self):
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self._analyzeAndPersistReport,
            auto_ack=True)
        self._channel.start_consuming()

if __name__ == "__main__":
    print("Running carbon emission analyzer service")
    service = CabonEmissionAnalyzerService()
    service.run()
