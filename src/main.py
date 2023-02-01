import sys
import time
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def wait_for_extended_operation(operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300):
    result = operation.result(timeout=timeout)
    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def stop_instance(project_id: str, zone: str, instance_name: str):
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance stopping")
    return


def start_instance(project_id: str, zone: str, instance_name: str):
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance starting")
    return


def compute_optimization(data, context):
    pass
