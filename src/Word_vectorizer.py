import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from src.feature_engineering import dataPreprocessing_w_contract_punct_remove


def generate_tfidf_features_with_stopwords(df, train_df, min_df=0.05, max_df=0.95):
    """
    Generate TF-IDF features for text data with stopwords removed.

    Parameters:
    - df: DataFrame containing the text data.
    - train_df: DataFrame containing additional information such as essay_id.
    - min_df: Minimum document frequency for words to be included in TF-IDF calculation (default: 0.05).
    - max_df: Maximum document frequency for words to be included in TF-IDF calculation (default: 0.95).

    Returns:
    - train_df_merged: Merged DataFrame containing TF-IDF features merged with train_df.
    - feature_names: List of feature names excluding 'essay_id', 'score', and 'full_text'.
    """
    
    stopwords_list = stopwords.words('english')
    
    # Initialize TfidfVectorizer
    word_vectorizer = TfidfVectorizer(
        strip_accents='ascii',
        analyzer='word',
        ngram_range=(1, 1),
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=True,
        stop_words=stopwords_list,
    )
    
    # Apply preprocessing to the text
    processed_text = df['full_text'].apply(lambda x: dataPreprocessing_w_contract_punct_remove(x))
    
    # Fit all datasets into TfidfVector
    train_tfid = word_vectorizer.fit_transform(processed_text)

    # Convert to array
    dense_matrix = train_tfid.toarray()

    # Convert to DataFrame
    df = pd.DataFrame(dense_matrix)

    # Rename features
    tfid_w_columns = [f'tfid_w_{i}' for i in range(len(df.columns))]
    df.columns = tfid_w_columns
    df['essay_id'] = train_df['essay_id']

    # Merge with existing features
    train_df_merged = train_df.merge(df, on='essay_id', how='left')

    # Filter feature names
    feature_names = list(filter(lambda x: x not in ['essay_id', 'score', 'full_text'], train_df_merged.columns))

    return train_df_merged, feature_names


# Example usage
# train_feats_with_stopwords, feature_names_with_stopwords = generate_tfidf_features_with_stopwords(train, train_feats)

