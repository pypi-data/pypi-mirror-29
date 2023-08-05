# pptcom

[![PyPi Version](https://img.shields.io/pypi/v/pptcom.svg)](https://pypi.python.org/pypi/pptcom)
[![Conda Version](https://img.shields.io/conda/vn/mrossi/pptcom.svg)](https://anaconda.org/mrossi/pptcom)

Use Microsoft PowerPoint within Python with the help of COM

## Installation

```
pip install pptcom
```

```
conda install -c mrossi pptcom
```

## Usage

You can export the slides of a PowerPoint-presentation:
```python
import pptcom

with pptcom.File('presentation.pptx') as pptfile:
    pptfile.export('png')
```

## Development

### Testing

For testing purposes [python-pptx](https://github.com/scanny/python-pptx) is used, after an installation of this package you can test the package with pytest.
