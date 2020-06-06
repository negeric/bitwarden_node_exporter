dev:
	BW_DB_PATH=$(CURDIR)/db.sqlite3 BW_ATTACH_PATH=$(CURDIR) python3 app/main.py

image:
	docker image build -t negeric/bitwarden_node_exporter:latest .
	docker image tag negeric/bitwarden_node_exporter:latest negeric/bitwarden_node_exporter:0.1.1
	docker push negeric/bitwarden_node_exporter:latest
	docker push negeric/bitwarden_node_exporter:0.1.1
