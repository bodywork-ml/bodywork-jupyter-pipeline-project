"""
This module runs executes the notebooks that reside within the same directory.
"""
import nbformat
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

NB_FILENAME = 'test_nb.ipynb'


def main():
    with open(NB_FILENAME) as nb_file:
        nb = nbformat.read(nb_file, as_version=4)
    nb_runner = ExecutePreprocessor(timeout=600, kernel_name='python3')
    try:
        nb_runner.preprocess(nb, {'metadata': {'path': '.'}})
    except CellExecutionError as e:
        msg = f'notebook raised error: {e}'
        print(msg)


if __name__ == '__main__':
    main()
