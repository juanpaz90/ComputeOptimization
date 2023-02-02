import sys
import base64
import json
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def decode_pubsub(data) -> dict:
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    return pubsub_data


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


def start_instance(project_id: str, zone: str, instance_name: str):
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance starting")
    return "START VM"


def stop_instance(project_id: str, zone: str, instance_name: str):
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance stopping")
    return "STOP VM"


def compute_optimization(data, context):
    if decode_pubsub(data) == "START":
        start_instance(project_id, zone, instance_name)
        print("Start VM")
    elif decode_pubsub(data) == "STOP":
        stop_instance(project_id, zone, instance_name)
        print("Stop VM")


if __name__ == "__main__":
    data_start = {"data": "U1RBUlQ="}
    data_stop = {"data": "U1RPUA=="}
    context = "none"
    compute_optimization(data_stop, context)
