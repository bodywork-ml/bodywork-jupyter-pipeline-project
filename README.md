# Jupyter Notebook Pipelines on Kubernetes using Bodywork

![bodywork](https://bodywork-media.s3.eu-west-2.amazonaws.com/jupyter_pipelines.png)

This repository contains a Bodywork project that demonstrates how to run a ML pipeline on Kubernetes, using Jupyter notebooks with Bodywork. The example pipeline has two stages, defined in two notebooks:

1. [train_model.ipynb](https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project/blob/master/train_model.ipynb) - download data from an AWS S3 bucket, train a classifier and then uploaded it back to the same S3 bucket.
2. [score_data.ipynb](https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project/blob/master/score_data.ipynb) - download the trained model from AWS S3, together with data needs to be scored, and then score the data and upload the results back to S3.

To run this project, follow the steps below.

## Get Access to a Kubernetes Cluster

Use our [Quickstart Guide to Kubernetes for MLOps](https://bodywork.readthedocs.io/en/latest/kubernetes/#quickstart) to spin-up a local Minikube cluster in minutes.

## Install the Bodywork Python Package

```shell
$ pip install bodywork
```

## Run the ML Pipeline

```shell
$ bodywork create deployment https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project
```

The orchestrator logs will be streamed to your terminal until the job has been successfully completed.

## Running the ML Pipeline on a Schedule

If you're happy with the test results, you can schedule the workflow-controller to operate remotely on the cluster on a pre-defined schedule. For example, to setup the the workflow to run every hour, use the following command,

```shell
$ bodywork create cronjob https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project \
    --name=jupyter-pipeline \
    --schedule="0 * * * *"
```

Each scheduled workflow will attempt to re-run the batch-job, as defined by the state of this repository's `master` branch at the time of execution.

To get the execution history for all `jupyter-pipeline` jobs use,

```shell
$ bodywork get cronjob jupyter-pipeline --history
```

## Make this Project Your Own

This repository is a [GitHub template repository](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) that can be automatically copied into your own GitHub account by clicking the `Use this template` button above.

After you've cloned the template project, use official [Bodywork documentation](https://bodywork.readthedocs.io/en/latest/) to help modify the project to meet your own requirements.
