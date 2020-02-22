if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f kb-cm.yml
kubectl apply -f kb-dep.yml
kubectl apply -f kb-svc.yml
kubectl apply -f kb-ing.yml
elif [ "$1" = "down" ]; then
kubectl delete -f kb-ing.yml
kubectl delete -f kb-svc.yml
kubectl delete -f kb-dep.yml
kubectl delete -f kb-cm.yml
fi
