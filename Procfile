web: export FLASK_APP=src/apps/carbon_emission_app.py; flask run; \
     docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management; \
     sleep 1; \
     python -m src.services.carbon_emission_storage_service.ephimeral_storage_service &; \
     sleep 1; \
     python -m src.services.carbon_emission_compute_service.vm_compute_service &; \
     sleep 1; \
     python -m src.services.carbon_emission_analyzer_service.analyzer_service &
