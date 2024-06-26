import polars as pl
from feature_engineering import dataPreprocessing

def Sentence_Preprocess(tmp):
    """This function takes a DataFrame as input, which likely contains the preprocessed data from essays.
    
        - It preprocesses the 'full_text' column using dataPreprocessing (not defined in the provided code) and splits the text into sentences using periods as separators.
        - It calculates the length of each sentence (sentence_len) and the number of words in each sentence (sentence_word_cnt).
        - It filters out sentences with a length less than 15 characters.

    Args:
        tmp (_type_): DataFrame

    Returns:
        tmp _type_: DataFrame
    """
    # Preprocess full_text and use periods to segment sentences in the text
    tmp = tmp.with_columns(pl.col('full_text').map_elements(dataPreprocessing).str.split(by=".").alias("sentence"))
    tmp = tmp.explode('sentence')
    # Calculate the length of a sentence
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: len(x)).alias("sentence_len"))
    # Filter out the portion of data with a sentence length greater than 15
    tmp = tmp.filter(pl.col('sentence_len')>=15)
    # Count the number of words in each sentence
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: len(x.split(' '))).alias("sentence_word_cnt"))
    return tmp

sentence_fea = ['sentence_len','sentence_word_cnt']

def Sentence_Eng(train_tmp):
    """This function takes a DataFrame as input, presumably the output of Sentence_Preprocess.
        - It performs feature engineering on the sentences, counting the number of sentences with lengths greater than certain thresholds (sentence_{i}_cnt).
        - It calculates additional statistics such as maximum, mean, minimum, first, last, sum, kurtosis, and quantiles (q1 and q3) for the features derived from the sentences (sentence_len, sentence_word_cnt).
        - Finally, it converts the resulting aggregated data back to a pandas DataFrame (df) for further analysis.


    Args:
        train_tmp (_type_): DataFrame

    Returns:
        df _type_: DataFrame
    """
    aggs = [
        # Count the number of sentences with a length greater than i
        *[pl.col('sentence').filter(pl.col('sentence_len') >= i).count().alias(f"sentence_{i}_cnt") for i in [15,50,100,150,200,250,300] ], 
        # other
        *[pl.col(fea).max().alias(f"{fea}_max") for fea in sentence_fea],
        *[pl.col(fea).mean().alias(f"{fea}_mean") for fea in sentence_fea],
        *[pl.col(fea).min().alias(f"{fea}_min") for fea in sentence_fea],
        *[pl.col(fea).first().alias(f"{fea}_first") for fea in sentence_fea],
        *[pl.col(fea).last().alias(f"{fea}_last") for fea in sentence_fea],
        *[pl.col(fea).sum().alias(f"{fea}_sum") for fea in sentence_fea],
        *[pl.col(fea).kurtosis().alias(f"{fea}_kurtosis") for fea in sentence_fea],
        *[pl.col(fea).quantile(0.25).alias(f"{fea}_q1") for fea in sentence_fea], 
        *[pl.col(fea).quantile(0.75).alias(f"{fea}_q3") for fea in sentence_fea], 
        ]
    df = train_tmp.group_by(['essay_id'], maintain_order=True).agg(aggs).sort("essay_id")
    df = df.to_pandas()
    return df
