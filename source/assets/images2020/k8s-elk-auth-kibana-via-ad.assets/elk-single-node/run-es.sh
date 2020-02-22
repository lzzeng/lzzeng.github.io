if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f ns-elk.yml
kubectl apply -f es-cm.yml
kubectl apply -f es-ss.yml
kubectl apply -f es-svc.yml
kubectl apply -f es-ing.yml
elif [ "$1" = "down" ]; then
kubectl delete -f es-ing.yml
kubectl delete -f es-svc.yml
kubectl delete -f es-ss.yml
kubectl delete -f es-cm.yml
kubectl delete -f ns-elk.yml
fi
