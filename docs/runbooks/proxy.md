# Runbook: Proxy

    ## Overview
    This runbook covers operational procedures for the proxy service.

    ## Health Check
    ```bash
    curl -s http://localhost:8000/health | jq .
    ```

    ## Common Issues

    ### Service Not Responding
    1. Check pod status: `kubectl get pods -l component=proxy`
    2. Check logs: `kubectl logs -l component=proxy --tail=100`
    3. Restart if needed: `kubectl rollout restart deployment/mach-proxy`

    ### High Latency
    1. Check metrics dashboard
    2. Review recent deployments
    3. Scale up if needed: `kubectl scale deployment/mach-proxy --replicas=4`

    ## Contacts
    - On-call: #mach-oncall
    - Escalation: #mach-engineering
