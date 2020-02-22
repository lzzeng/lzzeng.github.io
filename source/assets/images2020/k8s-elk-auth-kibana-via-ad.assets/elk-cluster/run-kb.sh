if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f kibana/kb-cm.yml
kubectl apply -f kibana/kb-dep.yml
kubectl apply -f kibana/kb-svc.yml
kubectl apply -f kibana/kb-ing.yml
elif [ "$1" = "down" ]; then
kubectl delete -f kibana/kb-cm.yml
kubectl delete -f kibana
fi

