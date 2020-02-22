if [ "$1" = "up" ] || [ -z "$1" ]; then
#kubectl apply -f logstash/log-cm.yaml
#kubectl apply -f logstash/log-ss.yaml
#kubectl apply -f logstash/log-svc-nodePort.yaml

kubectl apply -f logstash/log-cm.yaml
kubectl apply -f logstash/log-dep.yaml
kubectl apply -f logstash/log-dep-svc-nodePort.yaml
elif [ "$1" = "down" ]; then
kubectl delete -f logstash/log-dep-svc-nodePort.yaml
kubectl delete -f logstash/log-dep.yaml
kubectl delete -f logstash/log-cm.yaml
fi
