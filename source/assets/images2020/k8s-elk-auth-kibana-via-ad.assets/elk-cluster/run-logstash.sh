if [ "$1" = "up" ] || [ -z "$1" ]; then
#kubectl apply -f logstash/log-cm.yml
#kubectl apply -f logstash/log-ss.yml
#kubectl apply -f logstash/log-svc-nodePort.yml

kubectl apply -f logstash/log-cm.yml
kubectl apply -f logstash/log-dep.yml
kubectl apply -f logstash/log-dep-svc-nodePort.yml
elif [ "$1" = "down" ]; then
kubectl delete -f logstash/log-dep-svc-nodePort.yml
kubectl delete -f logstash/log-dep.yml
kubectl delete -f logstash/log-cm.yml
fi
