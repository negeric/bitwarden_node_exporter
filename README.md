# Bitwarden_rs Node Exporter
This tool was designed to expose Bitwarden metrics to Prometheus.  Currently, this exposes the following metrics
* Number of Attachments
* Total size of attachments
* Number of Collections
* SQLite Database Size
* Total number of Passwords
* User count
* Count MFA users 
* Number of Organizations

## Requirements
This only works with [Bitwarden_rs](https://github.com/dani-garcia/bitwarden_rs) with a SQLite database.  
While the Docker image can be used with docker-compose, the included manifest was written for Kubernetes.  
[Deploy Bitwarden on Kubernetes](https://tothecloud.dev/kubernetes/deploy-bitwarden-on-kubernetes/).  
A working deployment of prometheus is also required.

## Deployment
This will deploy a pod running a simple Flask app that exposes `/metrics` and `/health`.  The deployment uses Prometheus annotations for automatic scraping
```
annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '80'
    prometheus.io/path: '/metrics'
```
Note, if you override the `BW_APP_PORT` env var, ensure that `prometheus.io/port` matches.

Since this pod requires access to the SQLite database file, it much attach the same PVC that Bitwarden uses.  To avoid a dependency on ReadWriteMany PVCs, this uses PodAffinity to schedule this pod on the node with Bitwarden.  If you deployed bitwarden with the `app` name of something other than `bitwarden`, then you must update the PodAffinity annotation in the deployment yaml
```
labels:
    app: bitwarden
```

## Deployment YAML
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bitwarden-node-exporter
  namespace: bitwarden
  labels:
    app: bitwarden-node-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bitwarden-node-exporter
  template:
    metadata:
      labels:
        app: bitwarden-node-exporter
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '80'
        prometheus.io/path: '/metrics'
    spec:
      affinity:
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - bitwarden
            topologyKey: "kubernetes.io/hostname"
      volumes:
      - name: bitwarden-pv
        persistentVolumeClaim:
          claimName: bitwarden-pv
      containers:
      - name: bitwarden-node-exporter
        image: negeric/bitwarden_node_exporter:latest
        volumeMounts:
        - mountPath: /data
          name: bitwarden-pv
        ports:
        - containerPort: 80
        imagePullPolicy: Always
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
          timeoutSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
          timeoutSeconds: 10
        restartPolicy: Always
        env:
        - name: BW_APP_PORT
          value: "80"
        - name: BW_LOGLEVEL
          value: "WARN"
        - name: BW_DB_PATH
          value: "/data/db.sqlite3"
        - name: BW_ATTACH_PATH
          value: "/data/attachments"
```