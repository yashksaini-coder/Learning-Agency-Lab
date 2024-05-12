import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spellchecker import SpellChecker
from feature_engineering import dataPreprocessing_w_contract_punct_remove


class Preprocessor:
    def __init__(self) -> None:
        self.twd = TreebankWordDetokenizer()
        self.STOP_WORDS = set(stopwords.words('english'))
        self.spellchecker = SpellChecker()

    def spelling(self, text):
        wordlist=text.split()
        amount_miss = len(list(self.spellchecker.unknown(wordlist)))
        return amount_miss
    
    def count_sym(self, text, sym):
        sym_count = 0
        for line in text:
            if line == sym:
                sym_count += 1
        return sym_count

    def run(self, data: pd.DataFrame, mode:str) -> pd.DataFrame:
        
        # preprocessing the text
        data["processed_text"] = data["full_text"].apply(lambda x: dataPreprocessing_w_contract_punct_remove(x))
        
        # Text tokenization
        data["text_tokens"] = data["processed_text"].apply(lambda x: word_tokenize(x))
        
        # essay length
        data["text_length"] = data["processed_text"].apply(lambda x: len(x))
        
        # essay word count
        data["word_count"] = data["text_tokens"].apply(lambda x: len(x))
        
        # essay unique word count
        data["unique_word_count"] = data["text_tokens"].apply(lambda x: len(set(x)))
        
        # essay sentence count
        data["sentence_count"] = data["full_text"].apply(lambda x: len(x.split('.')))
        
        # essay paragraph count
        data["paragraph_count"] = data["full_text"].apply(lambda x: len(x.split('\n\n')))
        
        # count misspelling
        data["splling_err_num"] = data["processed_text"].apply(self.spelling)
        print("Spelling mistake count done")
        
        return data
# Example usage    
# preprocessor = Preprocessor()
# tmp = preprocessor.run(train.to_pandas(), mode="train")
# train_feats = train_feats.merge(tmp, on='essay_id', how='left')
# feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
# print('Features Number: ',len(feature_names))
# train_feats.head(3)