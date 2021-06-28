# Jupyter Notebook Pipelines on Kubernetes using Bodywork

![bodywork](https://bodywork-media.s3.eu-west-2.amazonaws.com/jupyter_pipelines.png)

This repository contains a Bodywork project that demonstrates how to run a ML pipeline on Kubernetes, using Jupyter notebooks with Bodywork. The example pipeline has two stages, defined in two notebooks:

1. [train_model.ipynb](https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project/blob/master/stage-1-train-model/train_model.ipynb) - download data from an AWS S3 bucket, train a classifier and then uploaded it back to the same S3 bucket.
2. [score_data.ipynb](https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project/blob/master/stage-2-score-data/score_data.ipynb) - download the trained model from AWS S3, together with data needs to be scored, and then score the data and upload the results back to S3.

In both stages the notebooks are handled by a `nb_runner.py` module. This has been configured to save the notebooks (with all cell outputs), and to uploaded them to AWS S3 after they have finished executing. From here they can be downloaded and inspected at a later date - e.g. to see model metrics and explainability output.

To run this project, follow the steps below.

## Get Access to a Kubernetes Cluster

In order to run this example project you will need access to a Kubernetes cluster. To setup a single-node test cluster on your local machine you can use [minikube](https://minikube.sigs.Kubernetes.io/docs/) or [docker-for-desktop](https://www.docker.com/products/docker-desktop). Check your access to Kubernetes by running,

```shell
$ kubectl cluster-info
```

Which should return the details of your cluster.

## Install the Bodywork Python Package

```shell
$ pip install bodywork
```

## Setup a Kubernetes Namespace for use with Bodywork

```shell
$ bodywork setup-namespace ml-pipeline
```

## Run the ML Pipeline

To test the ML pipeline, using a workflow-controller running on your local machine and interacting with your Kubernetes cluster, run,

```shell
$ bodywork deployment create \
    --namespace=ml-pipeline \
    --name=test-deployment \
    --git-repo-url=https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project \
    --git-repo-branch=master \
    --local-workflow-controller
```

The workflow-controller logs will be streamed to your shell's standard output until the job has been successfully completed.

## Running the ML Pipeline on a Schedule

If you're happy with the test results, you can schedule the workflow-controller to operate remotely on the cluster on a pre-defined schedule. For example, to setup the the workflow to run every hour, use the following command,

```shell
$ bodywork cronjob create \
    --namespace=ml-pipeline \
    --name=jupyter-pipeline \
    --schedule="0 * * * *" \
    --git-repo-url=https://github.com/bodywork-ml/bodywork-jupyter-pipeline-project \
    --git-repo-branch=master
```

Each scheduled workflow will attempt to re-run the batch-job, as defined by the state of this repository's `master` branch at the time of execution.

To get the execution history for all `jupyter-pipeline` jobs use,

```shell
$ bodywork cronjob history \
    --namespace=ml-pipeline \
    --name=jupyter-pipeline
```

Which should return output along the lines of,

```text
JOB_NAME                                START_TIME                    COMPLETION_TIME               ACTIVE      SUCCEEDED       FAILED
jupyter-pipeline-1605214260             2020-11-12 20:51:04+00:00     2020-11-12 20:52:34+00:00     0           1               0
```

Then to stream the logs from any given cronjob run (e.g. to debug and/or monitor for errors), use,

```shell
$ bodywork cronjob logs \
    --namespace=ml-pipeline \
    --name=jupyter-pipeline-1605214260
```

## Cleaning Up

To clean-up the deployment in its entirety, delete the namespace using kubectl - e.g. by running,

```shell
$ kubectl delete ns ml-pipeline
```

## Make this Project Your Own

This repository is a [GitHub template repository](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) that can be automatically copied into your own GitHub account by clicking the `Use this template` button above.

After you've cloned the template project, use official [Bodywork documentation](https://bodywork.readthedocs.io/en/latest/) to help modify the project to meet your own requirements.
