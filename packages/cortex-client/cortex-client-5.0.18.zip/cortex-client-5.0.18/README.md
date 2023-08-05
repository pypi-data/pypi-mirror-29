# Cortex ML Models Python Library

The Cortex Python Library provides an SDK to easily integrate and deploy ML algorithms into Cortex. 
Refer to the Cortex documentation for details on how to use the SDK: 

- Developer guide: https://docs.cortex.insights.ai/docs/developer-guide/overview/
- Python SDK references: https://docs.cortex.insights.ai/docs/developer-guide/reference-guides


## Installation
To install the Cortex Client: 
```
  > pip install cortex-client
```

or from source code:
```
  > python setup.py install
```

## Development

Install for development:
```
  > cd <cortex-python-sdk source dir>
  > virtualenv --python=python3 _venv3
  > source _venv3/bin/activate
  > make dev.install
```

There's a convenience `Makefile` that has commands to common tasks, such as build, test, etc. Use it!
