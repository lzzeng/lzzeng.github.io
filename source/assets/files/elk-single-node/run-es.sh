if [ "$1" = "up" ] || [ -z "$1" ]; then
kubectl apply -f ns-elk.yaml
kubectl apply -f es-cm.yaml
kubectl apply -f es-ss.yaml
kubectl apply -f es-svc.yaml
kubectl apply -f es-ing.yaml
elif [ "$1" = "down" ]; then
kubectl delete -f es-ing.yaml
kubectl delete -f es-svc.yaml
kubectl delete -f es-ss.yaml
kubectl delete -f es-cm.yaml
kubectl delete -f ns-elk.yaml
fi
