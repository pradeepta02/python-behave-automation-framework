# BDD Automation Framework

BDD framework built using Python and Behave to support automation testing of cleartrip on various browsers
## Getting Started

pip install -r requirements.txt

### Prerequisities

```
Python version >= 2.7.11
```

```
Any browser (Firefox, Chrome, IE or Safari)
```

## Running the tests

```
To run scripts for uitests: behave features/modules --tags=smoke --junit --no-capture
```

## Built with

* python >= 2.7.10
* behave >= 1.2.5
* parse >= 1.6.3
* parse_type >= 0.3.4
* selenium >= 2.48.0
* argparse
* PyHamcrest >= 1.8