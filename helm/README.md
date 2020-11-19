# Install update-all-the-things on k8s

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dep update

kubectl create namespace upd

helm install mariadb bitnami/mariadb --namespace upd -f values.db.yaml
helm upgrade --install upd . -f values.yaml --namespace upd
```