"""docker_compose validators."""

def validate_docker_compose(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("docker_compose data is required")
    return errors
