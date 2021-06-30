# Diglett

What it does
Diglett is a collection of my most frequently used and reusable functions for data analysis, data wrangling, and machine learning. I have largely packaged them together for my own benefit, but I hope you will find something useful in here for yourself.


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