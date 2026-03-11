"""k8s_deploy validators."""

def validate_k8s_deploy(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("k8s_deploy data is required")
    return errors
