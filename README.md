# Diglett

![Image of Diglett pokemon](https://raw.githubusercontent.com/asdfgeoff/diglett/master/diglett.png)


## What it does

Diglett is a collection of my most frequently used and reusable functions for data analysis, data wrangling, and machine learning. I have largely packaged them together for my own benefit, but I hope you will find something useful in here for yourself.


## Installing

You can install this package via pip:

```
pip install diglett
```

## API documentation

### diglett.decorate module

Useful decorators for troubleshooting data transformation pipelines and asserting assumptions.

Inspired by Tom Augspurger’s package engarde: [https://github.com/engarde-dev/engarde](https://github.com/engarde-dev/engarde)


#### diglett.decorate.describe_io(func)
Describe the shape of the input shape, output shape, and time of a pandas pipe function.


* **Return type**

    `Callable`



#### diglett.decorate.timeit(func)
Display the time taken to complete a pandas operation and the relative time by input size.


* **Return type**

    `Callable`



#### diglett.decorate.columns_exist(columns)
Verify that a list of columns exist in the input DataFrame.

The function being decorated should accept a pandas.DataFrame object as first argument
and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.


* **Return type**

    `Callable`



#### diglett.decorate.no_object_dtypes(func)
Verify that all columns of the output DataFrame have a dtype other than ‘Object’.

The function being decorated should accept a pandas.DataFrame object as first argument
and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.


* **Return type**

    `Callable`



#### diglett.decorate.no_additional_nulls(func)
Warn if the number of nulls in a DataFrame has increased during transformation.

The function being decorated should accept a pandas.DataFrame object as first argument
and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.


* **Return type**

    `Callable`



#### diglett.decorate.same_num_rows(func)
Ensure that a DataFrame transformation function returns the same number of rows as its input.

The function being decorated should accept a pandas.DataFrame object as first argument
and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.

### diglett.display module

Some utility functions related to displaying data nicely in Jupyter Notebooks.


#### diglett.display.n_largest_coefs(coefs, n=10)
Return the n largest absolute values from a pandas Series


* **Return type**

    `Series`



#### diglett.display.display_side_by_side(\*args)
Output an array of pandas DataFrames side-by-side in a Jupyter notebook to conserve vertical space.


* **Return type**

    `None`



#### diglett.display.print_header_with_lines(text, line_char='-')
Sandwich a given string with an equal length line of separate characters above and below it.


* **Return type**

    `None`



#### diglett.display.display_header(size, text)
Display an HTML header representation of a given string in a given size


* **Return type**

    `None`



### diglett.join module

Functions for performing joins more easily in pandas.


#### diglett.join.verbose_merge(left, right, left_on=None, right_on=None, left_index=False, right_index=False, \*args, \*\*kwargs)
Wraps pd.merge function to provide a visual overview of cardinality between datasets.


* **Return type**

    `DataFrame`


### diglett.transform module

Functions related to generating new predictive features on a dataset before fitting an ML model.


#### diglett.transform.make_comparison_bools(df, comparisons)
Assigns a float bool column to DataFrame reflecting whether a value equals another value.

Value is NaN when previous value does not exist.


* **Parameters**

    **comparisons** (*dict*) – Tuples of column names to compare, e.g.: output_column_name: (col_a, col_b)



* **Return type**

    `DataFrame`



#### diglett.transform.ordinal_encode_categoricals(X_train, X_test)
Fit an OrdinalEncoder on a combined test/train dataset and return transforms on each individual dataset.


* **Return type**

    `Tuple`[`DataFrame`, `DataFrame`]


### diglett.visualize module

Functions for performing visualizations with matplotlib and seaborn.


#### diglett.visualize.mpl_boilerplate(shape=(6, 4), left_title=False, y_axis=True, grid=False, legend=True)
Decorator to perform boilerplate matplotlib formatting.
Target plot function must accept fig, ax as first args and also return them.


* **Parameters**

    
    * **shape** (`Tuple`[`int`, `int`]) – size of matplotlib figure (width, height)


    * **left_title** (`bool`) – whether to left-align the title


    * **y_axis** (`bool`) – whether to show the y-axis


    * **grid** (`bool`) – whether to display grid lines


    * **legend** (`bool`) – whether to display legend



* **Return type**

    `None`


#### diglett.visualize.sorted_external_legend(func)
Display a legend on the outer right edge of the figure which is sorted by final value.


#### diglett.visualize.display_insight(df, fmt=None, title='', subtitle='', assertion=None)
Display a pandas DataFrame as a presentable display_insight.


* **Parameters**

    
    * **df** (`DataFrame`) – The table to be displayed


    * **fmt** (`Optional`[`str`]) – String representation of formatting to apply to dataframe output (e.g. {:.0%} for percentages )


    * **title** (`str`) – The key takeaway or display_insight from the table


    * **subtitle** (`str`) – A more objective description of the table contents


    * **assertion** (`Optional`[`Callable`]) – A lambda statement to check the validity of the display_insight against the contents of the dataframe



* **Return type**

    `None`


### diglett.wrangle module

Functions for wrangling a dataset into a tidy format with correct dtypes.

### Examples

You can infer dtypes for imported data, then apply a bunch of transformations, and finally describe them:

```
df = (pd
      .read_csv('data.csv')
      .pipe(infer_dtypes, categorical_threshold=0.10)
      .pipe(fillnas, subset=['category', 'type'])
      .pipe(drop_nulls, subset=['id', 'ts'])
      .pipe(drop_infinite)
      .pipe(bucket_long_tail_categories)
      .pipe(one_hot_encode_categoricals)

describe_dtypes(df)
```


#### diglett.wrangle.infer_dtypes(input_df, categorical_threshold=0.01)
Attempt to coerce dtypes to be numerical, datetime, or categorical rather than object.


* **Parameters**

    
    * **input_df** (`DataFrame`) – The DataFrame object whose dtypes are being inferred.


    * **categorical_threshold** (`float`) – The level of normalized cardinality below which to consider a field catagorical.



* **Return type**

    `DataFrame`



* **Returns**

    DataFrame of same dimensions as input, but with modified column dtypes.



#### diglett.wrangle.describe_dtypes(input_df, top_n_cats=10)
A more comprehensive overview of your data, inspired by pd.DataFrame.describe()

Splits output by dtype to provide a more relevant summary of each, including number and pct of null values.


* **Parameters**

    
    * **input_df** (`DataFrame`) – The dataframe to be desribed.


    * **top_n_cats** (`int`) – The number of most frequent values to include in summary of categorical columns.



* **Return type**

    `None`



#### diglett.wrangle.fillnas(input_df, subset=None)
Fills nulls in selected columns from a DataFrame then returns input in a DataFrame.pipe() compatible way.


* **Return type**

    `DataFrame`



#### diglett.wrangle.drop_nulls(input_df, subset=None)
Drops nulls in selected columns from a DataFrame then returns input in a DataFrame.pipe() compatible way.


* **Return type**

    `DataFrame`



#### diglett.wrangle.drop_infinite(input_df, subset=None)
Drops infinite values in selected columns then returns df in a DataFrame.pipe() compatible way.


* **Return type**

    `DataFrame`



#### diglett.wrangle.categorical_fillna(df)
Hard-codes null values as strings, necessary for CatBoost.


* **Return type**

    `DataFrame`



#### diglett.wrangle.bucket_long_tail_categories(input_df, other_after=100)
Replace long-tail values in each column with ‘Other’ to reduce cardinality.


* **Parameters**

    
    * **input_df** (`DataFrame`) – The entire DataFrame to operate on.


    * **other_after** (`int`) – The index after which to bucket long-tail values into ‘other’



* **Return type**

    `DataFrame`



#### diglett.wrangle.one_hot_encode_categoricals(input_df)
Automatically split any categorical columns into boolean columns for each value.


* **Parameters**

    **input_df** (`DataFrame`) – The entire DataFrame to operate on.



* **Returns**

    Output dataframe
    dict: Categorical mappings (useful for inverse transform during feature importance measurement)



* **Return type**

    pd.DataFrame



#### diglett.wrangle.cast_bools_to_float(df)
Hard-codes booleans as floats, necessary for CatBoost.


* **Return type**

    `DataFrame`


## Running the tests

TODO