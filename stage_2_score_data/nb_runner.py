"""
This module execute a notebook that exists within the same directory,
saves its state and then (optionally) uploads it to AWS S3.
"""
import logging
import os
import sys
from datetime import date
from pathlib import Path

import boto3 as aws
import nbformat
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

AWS_S3_BUCKET = 'bodywork-jupyter-pipeline-project'
NB_FILENAME = 'score_data.ipynb'
UPLOAD_TO_AWS_S3 = True


def main():
    """Main script to be executed."""
    with open(NB_FILENAME) as nb_file:
        nb = nbformat.read(nb_file, as_version=4)

    try:
        nb_runner = ExecutePreprocessor(timeout=600, kernel_name='python3')
        log.info(f'running {NB_FILENAME}')
        nb_runner.preprocess(nb, {'metadata': {'path': '.'}})
    except CellExecutionError as e:
        log.error(f'notebook raised error: {e}')
    finally:
        datestamp = date.today().isoformat()
        updated_nb_filename = f'{NB_FILENAME.split(".")[0]}_{datestamp}.ipynb'
        log.info(f'saving notebook state as {updated_nb_filename}')
        with open(updated_nb_filename, mode='w', encoding='utf-8') as nb_file:
            nbformat.write(nb, nb_file)

    if UPLOAD_TO_AWS_S3:
        log.info(f'uploading {updated_nb_filename} to AWS S3')
        upload_notebook_run(updated_nb_filename, AWS_S3_BUCKET)


def upload_notebook_run(nb_filename: str, aws_bucket: str) -> None:
    """Upload notebook to AWS S3."""
    try:
        s3_client = aws.client('s3')
        s3_client.upload_file(
            nb_filename,
            aws_bucket,
            f'notebook-runs/{nb_filename}'
        )
        log.info(f'uploaded {nb_filename} to s3://{aws_bucket}/notebook-runs/')
    except (ClientError, S3UploadFailedError):
        log.error('could not upload notebook to S3 - check AWS credentials')


def configure_logger() -> logging.Logger:
    """Configure a logger that will write to stdout."""
    log_handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter(
        '%(asctime)s - '
        '%(levelname)s - '
        '%(module)s.%(funcName)s - '
        '%(message)s'
    )
    log_handler.setFormatter(log_format)
    log = logging.getLogger(__name__)
    log.addHandler(log_handler)
    log.setLevel(logging.INFO)
    return log


def set_working_directory() -> None:
    """Switch working directory if running outside stage directory."""
    path_to_module = Path(__file__)
    os.chdir(path_to_module.parent)


if __name__ == '__main__':
    set_working_directory()
    log = configure_logger()
    main()
