if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f ns-elk.yaml
kubectl apply -f es/es-cm2.yaml
kubectl apply -f es/es-ss.yaml
kubectl apply -f es/es-svc.yaml
kubectl apply -f es/es-ing.yaml
elif [ "$1" = "down" ]; then
kubectl delete -f es/es-ing.yaml
kubectl delete -f es/es-svc.yaml
kubectl delete -f es/es-ss.yaml
kubectl delete -f es/es-cm.yaml
kubectl delete -f ns-elk.yaml
fi
