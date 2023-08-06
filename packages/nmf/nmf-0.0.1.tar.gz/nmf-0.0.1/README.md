# NMF Topic Models

[![Build Status](https://travis-ci.org/duhaime/nmf.svg?branch=master)](https://travis-ci.org/duhaime/nmf)

[Non-Negative Matrix Factorization](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) is a dimension reduction technique that factors an input matrix of shape *m x n* into a matrix of shape *m x k* and another matrix of shape *n x k*.

In text mining, one can use NMF to build [topic models](https://en.wikipedia.org/wiki/Topic_model). Using NMF, one can factor a [Term-Document Matrix](https://en.wikipedia.org/wiki/Document-term_matrix) of shape *documents x word types* into a matrix of *documents x topics* and another matrix of shape *word types x topics*. The former matrix describes the distribution of each topic in each document, and the latter describes the distribution of each word in each topic.

Given a collection of input documents, the source code in this repository builds a memory-efficient Term-Document Matrix, factors that matrix using NMF, then writes the resulting data structures as [JSON outputs](#ouput-data-json).

## Usage

To install, run `pip install nmf`.

Then, to build a topic model using all text files in `texts`, run:

```
from nmf import NMF
model = NMF(files='texts', topics=20)
```

The following attributes will then be present on `model`:

```
# the top terms in each topic
model.topics_to_words

# the documents by topics matrix
model.documents_by_topics

# the topics by terms matrix
model.topics_by_terms
```

### JSON Output

**topic_to_words.json** maps each topic id to the top words in that topic:

```
{
  "0": [
    "colours",
    "light",
    "prism", ...
  ],
  "1": [
    "sap",
    "tree",
    "bark", ...
  ], ...
}
```

**doc_to_topics.json** maps each input document to each topic id and its weight in the document:

```
{
  "texts/doc_1.txt": {
    "0": 0.52,
    "1": 0.0,
    "2": 0.0, ...
  },
  "texts/doc_2.txt": {
    "0": 0.0,
    "1": 0.67,
    "2": 0.0, ...
  },
]
```