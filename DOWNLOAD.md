Dataset **GWHD 2021** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzIxMDJfR1dIRCAyMDIxL2d3aGQtMjAyMS1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJDdHlvTnQxNzg0cXdka0NtM0ora3lYcXpBV1VBeGFaVXc2YW9oNU9RYTc4PSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='GWHD 2021', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://zenodo.org/record/5092309/files/gwhd_2021.zip?download=1).