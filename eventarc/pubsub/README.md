# Cloud Eventarc – Pub/Sub tutorial

This sample shows how to create a service that processes Pub/Sub events using 
[the CloudEvents SDK](https://github.com/cloudevents/sdk-python).

## Setup

Set the `gcloud` configuration variables:

```sh
gcloud config set project <PROJECT_ID>
gcloud config set run/region us-central1
gcloud config set run/platform managed
gcloud config set eventarc/location us-central1
```

## Quickstart

Deploy your Cloud Run service:

```sh
gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/eventarc-pubsub

gcloud run deploy eventarc-pubsub \
  --image gcr.io/$(gcloud config get-value project)/eventarc-pubsub \
  --platform managed \
  --allow-unauthenticated
```

Create a Cloud Eventarc trigger, which will also create a Pub/Sub topic:

```sh
gcloud eventarc triggers create pubsub-trigger \
  --destination-run-service=events-pubsub \
  --destination-run-region=us-central1 \
  --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished"
```

## Test

Test your Cloud Run service by getting the created topic, and publishing a message to that topic:

```sh
TOPIC=$(gcloud beta eventarc triggers describe pubsub-trigger \
--format="value(transport.pubsub.topic)")

echo "Listening to events on topic: $TOPIC"

gcloud pubsub topics publish $TOPIC --message="Events"
```

You may observe the Run service receiving an event in Cloud Logging:

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=eventarc-pubsub" \
  --project $(gcloud config get-value project) \
  --limit 10 \
  --format 'value(textPayload)'
```
