# Create topic
gcloud pubsub topics create stop_and_start_vms

#Create CRONE Job - STOP
gcloud scheduler jobs create pubsub stop_vms \
    --location=us-central1 \
    --schedule="00 22 * * 5" \
    --topic=stop_and_start_vms \
    --message-body="STOP"

#Create CRONE Job - START
gcloud scheduler jobs create pubsub start_vms \
    --location=us-central1 \
    --schedule="00 22 * * 7" \
    --topic=stop_and_start_vms \
    --message-body="START"

#Create CRONE Job with a JSON message
gcloud scheduler jobs create pubsub test01 \
    --location=us-central1 \
    --schedule="00 22 * * 7" \
    --topic=stop_and_start_vms \
    --message-body="{"Job": "Start","instances": {"instance_1": "vm_01","instance_2": "vm_02"}}"
