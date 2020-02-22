if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f kb-cm.yaml
kubectl apply -f kb-dep.yaml
kubectl apply -f kb-svc.yaml
kubectl apply -f kb-ing.yaml
elif [ "$1" = "down" ]; then
kubectl delete -f kb-ing.yaml
kubectl delete -f kb-svc.yaml
kubectl delete -f kb-dep.yaml
kubectl delete -f kb-cm.yaml
fi
