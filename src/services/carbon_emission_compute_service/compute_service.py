import datetime
import enum
import json
import pika
import random
import time
import threading

class CarbonEmissionComputeServiceInterface:
    def __init__(self):
        self._queue_name = "carbon_emission_compute_queue"
        self._connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
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
        