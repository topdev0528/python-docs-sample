# Google Cloud Video Intelligence

Demonstrates label detection using the Google Cloud Video Intelligence API.

## Setup
Please follow the [Set Up Your Project](https://cloud.google.com/video-intelligence/docs/getting-started#set_up_your_project)
steps in the Quickstart doc to create a project and enable the Google Cloud
Video Intelligence API. Following those steps, make sure that you
[Set Up a Service Account](https://cloud.google.com/video-intelligence/docs/common/auth#set_up_a_service_account),
and export the following environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json
```

## Run the sample

Install [pip](https://pip.pypa.io/en/stable/installing) if not already installed.

Install the necessary libraries using pip:

```sh
$ pip install -r requirements.txt
```

Run the sample, for example:
```
python shotchange.py gs://cloudmleap/video/googlework.mp4
```
