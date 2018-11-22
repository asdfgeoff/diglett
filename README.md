# Diglett

Generic tools for exploratory data analysis and data wrangling.

![Image of Diglett pokemon](diglett.png)


## Installing

Clone this repo, then navigate to the directory in Terminal and run this command

```
pip install -e .
```

## Features and usage

```py
from diglett import infer_dtypes, describe_dtypes

df.pipe(infer_dtypes, categorical_threshold=0.10).pipe(describe_dtypes)
```

## Running the tests

TODO