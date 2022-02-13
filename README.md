# Kaze, A CLI for Dataset Dependencies in ML Projects [![](https://img.shields.io/pypi/v/shields.svg?maxAge=3600&color=%2323aaff&label=PyPI)](https://pypi.org/project/kaze/)

## What is Kaze?

## Installation

```bash
pip install kaze
```

## Example Usage

To download a dataset, you can use the following command:
```bash
kaze add -n flowers https://www.robots.ox.ac.uk/\~vgg/data/flowers/102/102flowers.tgz --images $DATASETS/jpg
```
this will populate your `.datasets.yml` file with the following:

```yaml
datasets:
  - name: flowers
    source: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz
    path: $DATASETS/jpg
```
You can also add a dataset from a local file:

```yaml
kaze add mnist mnist.zip
```

And finally, you can download a dataset from a remote URL:
```yaml
kaze add mnist https://s3.amazonaws.com/kaze-datasets/mnist.zip
```
