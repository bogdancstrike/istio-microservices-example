# Istio Example

To deploy the project and test it via curl using the provided deployments directory, follow this step-by-step infrastructure guide:

Before deploying, make sure you enable the following:

```code
microk8s enable dns registry ingress istio cert-manager
```

### Step 1: Setup Kubernetes Namespace

1. Create the namespace:

```code
kubectl create namespace istioexample
```

2. Verify namespace:

```code
kubectl get namespaces
```

### Step 2: Deploy the Services

1. Deploy All Services and Resources

```code
kubectl apply -f deployment-user-service.yaml -n istioexample
kubectl apply -f deployment-product-service.yaml -n istioexample
kubectl apply -f deployment-order-service.yaml -n istioexample
kubectl apply -f istio-gateway.yaml -n istioexample
kubectl apply -f istio-virtualservice.yaml -n istioexample
```

2. Verify Deployments

```code
kubectl get pods -n istioexample
```

3. Expected output:

```code
NAME                                    READY   STATUS    RESTARTS   AGE
user-service-xxxxxx                     2/2     Running   0          1m
product-service-xxxxxx                  2/2     Running   0          1m
order-service-xxxxxx                    2/2     Running   0          1m
frontend-xxxxxx                         1/1     Running   0          1m
```

- READY should be 2/2 for all service pods if Istio is enabled.


### Step 3: Port-Forward Each Service

To access the services locally, port-forward them to your machine.

1. Port-Forward User Service

```code
kubectl port-forward svc/user-service -n istioexample 5001:80
```

2. Port-Forward Product Service

```code
kubectl port-forward svc/product-service -n istioexample 5002:80
```

3. Port-Forward Order Service

```code
kubectl port-forward svc/order-service -n istioexample 5003:80
```

### Step 4: Test the Services via curl

1. Test the user service:

```code
curl http://localhost:5001/users/1
```

Expected response:

```code
{"name":"Alice"}
```

2. Test the Product Service

```code
curl http://localhost:5002/products/101
```

Expected response:

```code
{"name":"Laptop"}
```

3. Test the Order Service

```code
curl http://localhost:5003/orders/5001
```

Expected response:

```code
{
  "order_id": "5001",
  "user": {"name": "Alice"},
  "product": {"name": "Laptop"}
}
```

## How it works

### 1. Deployments

- Services (**user-service**, **product-service**, **order-service**) are deployed as pods in Kubernetes.
- Each service is exposed via a **ClusterIP** service for internal communication.

### 2. Port-Forwarding

- Map each service to a local port (e.g., 5001, 5002, etc.) so you can test them directly on your machine using curl.

### 3. Istio

- When Istio is enabled, it injects a **sidecar proxy** (_Envoy_) into every service pod.
- All traffic to and from a service flows through this proxy.


## Why Istio Works

### 1. Traffic Control

- Istio automatically handles service-to-service communication inside the cluster (**order-service** calling **user-service**).
- You don’t see this directly because it’s seamless.

### 2. Sidecars

- The Envoy proxies in each pod ensure secure communication, retries, and load balancing, even though you’re testing services directly with port-forwarding.

### 3. Default Kubernetes Networking

- Istio works because it uses Kubernetes' built-in DNS and networking to route traffic between services inside the cluster.


In short: Istio works invisibly behind the scenes, enhancing service communication and security within Kubernetes.

## Istio's Main Advantages

### Service-to-Service Communication (Infrastructure Level)

Istio manages how services talk to each other within a Kubernetes cluster.

- **Automatic Service Discovery**: Services can find each other without needing manual configurations.
- **Traffic Routing**: It can route traffic intelligently (e.g., based on request headers, percentages for canary deployments, etc.).
- **Load Balancing**: Istio balances traffic across multiple replicas of a service.

### Security (Infrastructure and Application Levels)

Istio provides security features without requiring developers to modify their application code.

- Mutual TLS (mTLS):
  - Encrypts traffic between services by default.
  - Ensures secure communication.

- Authentication & Authorization:
  - Verifies service identity.
  - Allows defining policies like "which services can access this service."


# Istio vs API Gateway: Comparison

| **Feature**               | **Istio**                                                | **API Gateway**                                   |
|---------------------------|---------------------------------------------------------|--------------------------------------------------|
| **Purpose**               | Manages **service-to-service** traffic inside the cluster. | Handles **external-to-internal** traffic.        |
| **Focus**                 | Networking, security, and observability for microservices. | API management and client-to-service interaction. |
| **Traffic Direction**     | Internal (east-west traffic).                            | External (north-south traffic).                 |
| **Authentication**        | Uses mTLS and service identities (internal services).    | Client authentication, API keys, OAuth2, etc.  |
| **Rate Limiting**         | Limited; needs extensions like Envoy rate-limiting.      | Built-in (e.g., limit client requests).         |
| **Request Transformation**| Basic (e.g., header manipulations).                     | Advanced (e.g., URL rewriting, payload changes).|
| **Observability**         | Provides deep observability for service-to-service communication. | Focused on monitoring client traffic to APIs.   |
| **Deployment Scope**      | Works inside the cluster (internal traffic management).   | Exposes and manages APIs to external clients.   |
| **Examples**              | Istio, Linkerd, Consul Connect.                         | Kong, NGINX, Traefik, Apigee.                   |