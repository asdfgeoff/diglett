import seaborn as sns

from diglett.eda import summarize


def test_summarize():
    df = sns.load_dataset('penguins')
    output = summarize(df, return_output=True)
    print(output)

    assert output.columns.tolist() == [
        'dtype',
        'Null (#)',
        'Null (%)',
        'Unique (#)',
        'Unique (%)',
        'mode',
        'min',
        'mean',
        'max',
    ]

    assert int(output[['min', 'mean', 'max']].sum().sum()) == 13993
