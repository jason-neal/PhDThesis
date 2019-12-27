import pytest
import os
import subprocess
import tempfile

import nbformat

def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    print(dirname)
    #print(os.getcwd())
    #os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter","nbconvert", "--to", "notebook", "--execute",
          "--ExecutePreprocessor.timeout=60",
          "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
                     for output in cell["outputs"]\
                     if output.output_type == "error"]

    return nb, errors


### TEST NOTEBOOKS

@pytest.fixture(params=[
    os.path.join("reduction","Reduction_images.ipynb"),
    os.path.join("reduction","Model_spectra_plots.ipynb"),
    #"reduction/Reduction_images.py",
    ])
def notebook(request):
    """Notebook names 1 by 1."""
    return request.param

def test_ipynb(notebook):
    """Checks all cells run without error"""
    nb, errors = _notebook_run(notebook)
    assert errors == []
