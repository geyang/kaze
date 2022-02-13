# Kaze, A CLI for Dataset Dependencies in ML Projects [![](https://img.shields.io/pypi/v/shields.svg?maxAge=3600&color=%2323aaff&label=PyPI)](https://pypi.org/project/kaze/)

## What is Kaze?

Have you downloaded a supervised-learning code base, and wish someone has specified how to download the dataset needed?

`Kaze` is a CLI for managing dataset dependencies in ML projects. It is a simple, yet powerful tool for managing dataset dependencies in your project. It is designed to be used in a way that is similar to `yarn` or `npm`, but with a focus on the `dataset` dependency.

## Installation

```bash
pip install kaze
```

## Example Usage

To download a dataset, you can use the following command:
```bash
kaze add -n flowers https://www.robots.ox.ac.uk/\~vgg/data/flowers/102/102flowers.tgz --images $DATASETS/jpg
```

this will populate your `.kaze.yml` file with the following:

```yaml
datasets:
  - name: flowers
    source: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz
    images: $DATASETS/jpg
```

You can also add a dataset from a local file:

```yaml
kaze add mnist.zip
```

