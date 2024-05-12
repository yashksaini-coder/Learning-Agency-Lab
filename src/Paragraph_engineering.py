import polars as pl
from feature_engineering import dataPreprocessing

def Paragraph_Preprocess(tmp):
    """This function takes a DataFrame as input and performs the following operations:-
        - It explodes the 'paragraph' column, which likely means that if there were multiple paragraphs in a single row, it separates them into individual rows.
        - It preprocesses each paragraph using the function dataPreprocessing (not defined in the provided code).
        - It calculates the length of each paragraph (paragraph_len), the number of sentences in each paragraph (paragraph_sentence_cnt), and the number of words in each paragraph (paragraph_word_cnt).

    Args:
        tmp (_type_): DataFrame 

    Returns:
        _type_: DataFrame 
    """
    # Expand the paragraph list into several lines of data
    tmp = tmp.explode('paragraph')
    # Paragraph preprocessing
    tmp = tmp.with_columns(pl.col('paragraph').map_elements(dataPreprocessing))
    # Calculate the length of each paragraph
    tmp = tmp.with_columns(pl.col('paragraph').map_elements(lambda x: len(x)).alias("paragraph_len"))
    # Calculate the number of sentences and words in each paragraph
    tmp = tmp.with_columns(pl.col('paragraph').map_elements(lambda x: len(x.split('.'))).alias("paragraph_sentence_cnt"),
                    pl.col('paragraph').map_elements(lambda x: len(x.split(' '))).alias("paragraph_word_cnt"),)
    return tmp

paragraph_fea = ['paragraph_len','paragraph_sentence_cnt','paragraph_word_cnt']

def Paragraph_Eng(train_tmp):
    """This function takes a DataFrame train as input (presumably the output of Paragraph_Preprocess) and performs the following feature engineering steps:

        - It aggregates statistics based on paragraph length, such as counting the number of paragraphs with lengths greater than or equal to certain thresholds (paragraph_{i}_cnt).
        - It calculates additional statistics such as maximum, mean, minimum, first, last, sum, kurtosis, and quantiles (q1 and q3) for the features derived from the paragraphs (paragraph_len, paragraph_sentence_cnt, paragraph_word_cnt).
        Finally, it converts the resulting aggregated data back to a pandas DataFrame (df) for further analysis.

    Args:
        train_tmp (_type_): DataFrame

    Returns:
        _type_: DataFrame
    """
    aggs = [
        # Count the number of paragraph lengths greater than and less than the i-value
        *[pl.col('paragraph').filter(pl.col('paragraph_len') >= i).count().alias(f"paragraph_{i}_cnt") for i in [50,75,100,125,150,175,200,250,300,350,400,500,600,700] ], 
        *[pl.col('paragraph').filter(pl.col('paragraph_len') <= i).count().alias(f"paragraph_{i}_cnt") for i in [25,49]], 
        # other
        *[pl.col(fea).max().alias(f"{fea}_max") for fea in paragraph_fea],
        *[pl.col(fea).mean().alias(f"{fea}_mean") for fea in paragraph_fea],
        *[pl.col(fea).min().alias(f"{fea}_min") for fea in paragraph_fea],
        *[pl.col(fea).first().alias(f"{fea}_first") for fea in paragraph_fea],
        *[pl.col(fea).last().alias(f"{fea}_last") for fea in paragraph_fea],
        *[pl.col(fea).sum().alias(f"{fea}_sum") for fea in paragraph_fea],
        *[pl.col(fea).kurtosis().alias(f"{fea}_kurtosis") for fea in paragraph_fea],
        *[pl.col(fea).quantile(0.25).alias(f"{fea}_q1") for fea in paragraph_fea],  
        *[pl.col(fea).quantile(0.75).alias(f"{fea}_q3") for fea in paragraph_fea],
    ]
    df = train_tmp.group_by(['essay_id'], maintain_order=True).agg(aggs).sort("essay_id")
    df = df.to_pandas()
    return df