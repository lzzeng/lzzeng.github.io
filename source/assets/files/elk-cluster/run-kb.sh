if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f kibana/kb-cm.yaml
kubectl apply -f kibana/kb-dep.yaml
kubectl apply -f kibana/kb-svc.yaml
kubectl apply -f kibana/kb-ing.yaml
elif [ "$1" = "down" ]; then
kubectl delete -f kibana/kb-cm.yaml
kubectl delete -f kibana
fi

