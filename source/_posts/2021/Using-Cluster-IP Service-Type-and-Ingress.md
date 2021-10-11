---
title: Using Cluster IP Service Type and Ingress
date: 2021-01-12 22:55:40
tags:
    - K8s
categories:
    - DevOps
copyright: false
---





> [ingress四层转发配置参考](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/)
>
> [Exposing the probe service - IBM Documentation](https://www.ibm.com/docs/en/netcoolomnibus/8?topic=private-exposing-probe-service)



Due to a limitation on the Kubernetes Ingress resource to expose TCP and UDP services, the following steps can be used to create a static configuration on the Kubernetes Ingress controller to make the probe service reachable externally. This limitation does not apply to probes that use HTTP protocols to receive data.

A Cluster Administrator needs to reconfigure the nginx-ingress-controller with a "static" configuration based on Configmaps and restart the ingress controller for the changes to take effect.

<!-- more -->



> CAUTION:
>
> Restarting the ingress controller would impact other workloads running. Consider performing the change during a planned downtime in production environments.



To expose the probe TCP/UDP service to external networks using Ingress, you will need to configure the nginx-ingress-controller to specify the **--tcp-services-configmap** and **--udp-services-configmap** flags to point to an existing configuration map where the key is the external port to use and the value indicates the service to expose:

1. Set **probe.service.type=ClusterIP**.

2. Determine the service name and ports of deployment using the following commands. In this example, the myprobe Helm release in the default namespace is used to query for the service name and port.

  ```
  export NAMESPACE=default
  export CHARTREL=myprobe
  export SERVICE_NAME=$(kubectl get services --namespace $NAMESPACE -l "app.kubernetes.io/instance=$CHARTREL" -o jsonpath="{.items[0].metadata.name}")
  export SERVICE_PORT=$(kubectl get services --namespace $NAMESPACE -l "app.kubernetes.io/instance=$CHARTREL" -o jsonpath="{.items[0].spec.ports[0].port}")
  echo "$NAMESPACE/$SERVICE_NAME:$SERVICE_PORT"
  default/myprobe-ibm-netcool-probe-snmp:162
  ```

  

3. Create a configuration map to store the external port to use and service to expose using the format: <namespace/service name>:<service port>:[PROXY]:[PROXY] where [PROXY]:[PROXY] is optional. For example, create the configmap resource as shown below in the default namepace to expose a host port 1162 to myprobe-ibm-netcool-probe-snmp on port 162 which is deployed on default namespace. If an existing configmap already exists, add a new entry into the section data.

  ```
  kubectl create configmap tcp-controller-configmap \
      --from-literal=1162=default/myprobe-ibm-netcool-probe-snmp:162
  ```

  

  This creates the following config map:

  ```
  apiVersion: v1
  kind: ConfigMap
  metadata:
      name: tcp-controller-configmap
      namespace: default
  data:
      1162: "default/myprobe-ibm-netcool-probe-snmp:162"
  ```

  ​	

4. Optionally, to expose a UDP service, create a new config map as shown in the following example. If an existing configmap exists, add a new entry into the data section.

  ```
  apiVersion: v1
  kind: ConfigMap
  metadata:
      name: udp-controller-configmap
      namespace: default
  data:
      1162: "default/myprobe-ibm-netcool-probe-snmp:162"
  ```

  

5. Edit the nginx-ingress-controller daemon set to add the following items.

   > **Note**: In IBM Cloud Private 2.1.0.2, the Nginx Controller name is nginx-ingress-lb-<arch>, where <arch> is the platform architecture such amd64 or ppc64le.

   

   The TCP/UDP services configmap flags **--tcp-services-configmap=tcp-controller-configmap** and **--udp-services-configmap=udp-controller-configmap** in the .spec.template.spec.containers[].args[] attribute. An example is shown in the following JSON snippet:

   ```
   "spec": {
       "containers": [
    {
           "args": [
            "/nginx-ingress-controller",
               "--default-backend-service=$(POD_NAMESPACE)/default-backend",
               "--configmap=$(POD_NAMESPACE)/nginx-ingress-controller",
               "--report-node-internal-ip-address=true",
            "--annotations-prefix=ingress.kubernetes.io",
               "--enable-ssl-passthrough=true",
            "--publish-status-address=9.42.83.226",
               "--udp-services-configmap=default/udp-controller-configmap",
               "--tcp-services-configmap=default/tcp-controller-configmap"
       	],
   ```

   

   Add an additional hostport for the Ingress to open in the .spec.template.spec.containers[].ports[] attribute of the nginx-ingress-controller daemon set in the kube-system namespace. The default ports are ports 80 (TCP) and 443 (TCP). To add the additional hostports, use the following steps:

   Edit the nginx-ingress-controller and find the .spec.template.spec.containers[].ports[] attribute.

   ```
   kubectl edit ds/nginx-ingress-controller -n kube-system
   ```

   

   The example shown in the following JSON snippet adds two new hostports 1162 for both TCP/UDP in the Ingress controller.

   ```
   "name": "nginx-ingress",
   "ports": [
    {
           "containerPort": 80,
        "hostPort": 80,
           "name": "http",
        "protocol": "TCP"
       },
       {
           "containerPort": 443,
        "hostPort": 443,
           "name": "https",
        "protocol": "TCP"
       },
    {
           "containerPort": 1162,
           "hostPort": 1162,
           "name": "snmp-tcp",
        "protocol": "TCP"
       },
    {
           "containerPort": 1162,
        "hostPort": 1162,
           "name": "snmp-udp",
           "protocol": "UDP"
       }
   ],
   ```

   

   Save/apply the changes to the nginx-ingress-controller daemon set. The nginx-ingress-controller will automatically restart its nginx-ingress-controller pod and load the new configuration.

   

6. After the nginx-ingress-controller pod is running, verify that you are able to reach the probe service via the hostport. For the SNMP Probe for example, test by sending a SNMP trap to <kubernetes-proxy-ip>:1162 as configured above and the SNMP Probe should log (if messageLevel=debug) indicating that trap is received.

  ```
  snmptrap -C i -v 2c \
      -c public tcp:<kubernetes-proxy-ip>:1162 \
      .1.3.6.1.6.3.1.1.5.3 .1.3.6.1.6.3.1.1.5.3   \
      ifIndex i 2 \
      ifAdminStatus i 1 \
      ifOperStatus i 1
  ```