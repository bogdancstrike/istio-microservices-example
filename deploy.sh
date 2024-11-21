#!/bin/bash

NAMESPACE="istioexample"

# Create namespace
kubectl create namespace $NAMESPACE

# Apply deployments
kubectl apply -f deployment-user-service.yaml -n $NAMESPACE
kubectl apply -f deployment-product-service.yaml -n $NAMESPACE
kubectl apply -f deployment-order-service.yaml -n $NAMESPACE
kubectl apply -f istio-gateway.yaml -n $NAMESPACE
kubectl apply -f istio-virtualservice.yaml -n $NAMESPACE

echo "Deployment complete. Use port-forwarding to test the services."
