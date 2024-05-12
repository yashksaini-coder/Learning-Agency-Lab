"""This scripts is used to perform the process of text vectorization using TF-IDF (Term Frequency-Inverse Document Frequency),
and then merges the TF-IDF features with the previously generated features from paragraphs and sentences.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def Generate_tfidf_features(train, train_feats):
    """
    This code snippet performs text vectorization using TF-IDF (Term Frequency-Inverse Document Frequency) and then merges the TF-IDF features with the previously generated features from paragraphs and sentences. Let's break down each part:

    1. **`TfidfVectorizer` Initialization**:
    - The `TfidfVectorizer` is initialized with several parameters:
        - `tokenizer=lambda x: x`: This parameter specifies that the tokenizer function should be the identity function, meaning it doesn't tokenize the input text further and treats each input as a single token.
        - `preprocessor=lambda x: x`: Similarly, the preprocessor function is set to the identity function, meaning no additional preprocessing is applied before tokenization.
        - `token_pattern=None`: This parameter overrides the default token pattern used by the vectorizer, effectively disabling tokenization based on patterns.
        - `strip_accents='unicode'`: It specifies that accents should be stripped using Unicode normalization.
        - `analyzer='word'`: This parameter indicates that the analyzer should treat each token as a word.
        - `ngram_range=(1,3)`: It specifies that the vectorizer should consider unigrams, bigrams, and trigrams.
        - `min_df=0.05` and `max_df=0.95`: These parameters set the minimum and maximum document frequencies for terms to be included in the TF-IDF matrix, filtering out terms that are too rare or too common.
        - `sublinear_tf=True`: It enables sublinear TF scaling, which applies a logarithmic scaling to the term frequencies.

    2. **Fitting and Transforming Data**:
    - The vectorizer is then fitted and transformed with the 'full_text' column from the `train` DataFrame, which contains the text data to be vectorized. This results in a TF-IDF matrix (`train_tfid`).

    3. **Feature Extraction**:
    - `vectorizer.get_feature_names_out()` is used to extract the feature names from the TF-IDF vectorizer, which are then printed for inspection.

    4. **Conversion to DataFrame**:
    - The TF-IDF matrix (`train_tfid`) is converted to a dense matrix using `.toarray()`, and then to a pandas DataFrame (`df`).

    5. **Feature Renaming and Merging**:
    - The feature columns in the DataFrame (`df`) are renamed to 'tfid_i' where 'i' is the index of the feature.
    - The 'essay_id' column is added to the DataFrame from `train_feats` to ensure alignment with the other features.
    - The TF-IDF features are merged with the previously generated features (`train_feats`) based on the 'essay_id' column.

    Overall, this code combines TF-IDF vectorization with the existing feature engineering pipeline to enrich the feature set for further analysis or machine learning tasks, particularly in the context of text data (essays in this case).

    Args:
        train (_type_): Dataframe
        train_feats (_type_): Dataframe
        
    Returns:
        train_feats: Dataframe
        feature_names: Dataframe
    """
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        token_pattern=None,
        strip_accents='unicode',
        analyzer='word',
        ngram_range=(1, 3),
        min_df=0.05,
        max_df=0.95,
        sublinear_tf=True,
    )

    # Fit and transform the 'full_text' column from the train DataFrame
    train_tfid = vectorizer.fit_transform([i for i in train['full_text']])

    # Extract feature names from the TF-IDF vectorizer
    print("#"*80)
    vect_feat_names=vectorizer.get_feature_names_out()
    print(vect_feat_names[100:110])
    print("#"*80, "\n\n")
    
    # Convert TF-IDF matrix to a dense array
    dense_matrix = train_tfid.toarray()

    # Convert the dense array to a DataFrame
    df = pd.DataFrame(dense_matrix)

    # Rename feature columns
    tfid_columns = [f'tfid_{i}' for i in range(len(df.columns))]
    df.columns = tfid_columns

    # Add 'essay_id' column to the DataFrame
    df['essay_id'] = train_feats['essay_id']

    # Merge TF-IDF features with existing features in train_feats DataFrame
    train_feats = train_feats.merge(df, on='essay_id', how='left')

    # Get the final list of feature names
    feature_names = list(filter(lambda x: x not in ['essay_id', 'score'], train_feats.columns))

    return train_feats, feature_names
