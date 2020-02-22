if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f ns-elk.yml
kubectl apply -f es/es-cm2.yml
kubectl apply -f es/es-ss.yml
kubectl apply -f es/es-svc.yml
kubectl apply -f es/es-ing.yml
elif [ "$1" = "down" ]; then
kubectl delete -f es/es-ing.yml
kubectl delete -f es/es-svc.yml
kubectl delete -f es/es-ss.yml
kubectl delete -f es/es-cm.yml
kubectl delete -f ns-elk.yml
fi
