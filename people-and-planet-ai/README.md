# 🌍 People & Planet AI

## 🦏 [Wildlife Insights -- _image-classification_](image-classification)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/image-classification/README.ipynb)

> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/hUzODH3uGg0/0.jpg)](https://youtu.be/hUzODH3uGg0)

This model is trained to recognize animal species from
[camera trap](https://en.wikipedia.org/wiki/Camera_trap)
pictures.

* **Model**: [AutoML] Vision
* **Creating datasets**: [Apache Beam] in [Dataflow]
* **Training the model**: [AutoML] in [Vertex AI]
* **Getting predictions**: [Vertex AI]

[Apache Beam]: https://beam.apache.org
[Dataflow]: https://cloud.google.com/dataflow
[AutoML]: https://cloud.google.com/vertex-ai/docs/beginner/beginners-guide
[Vertex AI]: https://cloud.google.com/vertex-ai

## 🗺 [Global Fishing Watch -- _timeseries-classification_](timeseries-classification)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/timeseries-classification/README.ipynb)

> [Watch the video in YouTube<br> ![thumbnail](http://img.youtube.com/vi/LnEhSVEJUuY/0.jpg)](https://youtu.be/LnEhSVEJUuY)

This model is trained to classify if a ship is fishing or not every hour from their
[_Maritime Mobile Service Identitiy_ (MMSI)](https://en.wikipedia.org/wiki/Maritime_Mobile_Service_Identity)
location data.

* **Model**: 1D Fully Convolutional Network in [Keras]
* **Creating datasets**: [Apache Beam] in [Dataflow]
* **Training the model**: [Keras] in [Vertex AI]
* **Getting predictions**: [Keras] in [Cloud Run]

[Apache Beam]: https://beam.apache.org
[Cloud Run]: https://cloud.google.com/run
[Dataflow]: https://cloud.google.com/dataflow
[Keras]: https://keras.io
[Vertex AI]: https://cloud.google.com/vertex-ai

## 🏭 [Coal Plant Predictions -- _geospatial-classification_](geospatial-classification)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/people-and-planet-ai/geospatial-classification/README.ipynb)

This model uses satellite data to predict if a coal plant is turned on and producing carbon emissions. The satellite data comes from [Google Earth Engine.](https://earthengine.google.com/)

* **Model**: 1D Fully Convolutional Network in [TensorFlow]
* **Creating datasets**: [Sentinel-2] satellite data from [Earth Engine]
* **Training the model**: [TensorFlow] in [Vertex AI]
* **Getting predictions**: [TensorFlow] in [Cloud Run]

[Cloud Run]: https://cloud.google.com/run
[Sentinel-2]: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
[Earth Engine]: https://earthengine.google.com/
[TensorFlow]: https://www.tensorflow.org/
[Vertex AI]: https://cloud.google.com/vertex-ai
