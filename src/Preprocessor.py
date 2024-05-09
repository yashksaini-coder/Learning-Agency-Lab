import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spellchecker import SpellChecker
from feature_engineering import dataPreprocessing, dataPreprocessing_w_contract, dataPreprocessing_w_punct_remove, dataPreprocessing_w_contract_punct_remove

class Preprocessor:
    def __init__(self) -> None:
        self.twd = TreebankWordDetokenizer()
        self.STOP_WORDS = set(stopwords.words('english'))
        self.spellchecker = SpellChecker() 

    def spelling(self, text):
        wordlist=text.split()
        amount_miss = len(list(self.spellchecker.unknown(wordlist)))
        return amount_miss
    
    def run(self, data: pd.DataFrame, mode:str) -> pd.DataFrame:
        data["text_tokens"] = data["full_text"].apply(lambda x: word_tokenize(x))
        data["text_length"] = data["full_text"].apply(lambda x: len(x))
        data["word_count"] = data["text_tokens"].apply(lambda x: len(x))
        data["unique_word_count"] = data["text_tokens"].apply(lambda x: len(set(x)))
        data["splling_err_num"] = tqdm(data["full_text"].apply(self.spelling))
   
        data["processed_text"] = data["full_text"].apply(lambda x: dataPreprocessing(x))
        data["text_tokens"] = data["processed_text"].apply(lambda x: word_tokenize(x))
        data["text_length_p"] = data["processed_text"].apply(lambda x: len(x))
        data["word_count_p"] = data["text_tokens"].apply(lambda x: len(x))
        data["unique_word_count_p"] = data["text_tokens"].apply(lambda x: len(set(x)))
        data["splling_err_num_p"] = tqdm(data["processed_text"].apply(self.spelling))
    
        data["processed_text"] = data["full_text"].apply(lambda x: dataPreprocessing_w_contract(x))
        data["text_tokens"] = data["processed_text"].apply(lambda x: word_tokenize(x))
        data["text_length_pc"] = data["processed_text"].apply(lambda x: len(x))
        data["word_count_pc"] = data["text_tokens"].apply(lambda x: len(x))
        data["unique_word_count_pc"] = data["text_tokens"].apply(lambda x: len(set(x)))
        data["splling_err_num_pc"] = tqdm(data["processed_text"].apply(self.spelling))
        
        data["processed_text"] = data["full_text"].apply(lambda x: dataPreprocessing_w_punct_remove(x))
        data["text_tokens"] = data["processed_text"].apply(lambda x: word_tokenize(x))
        data["text_length_ppr"] = data["processed_text"].apply(lambda x: len(x))
        data["word_count_ppr"] = data["text_tokens"].apply(lambda x: len(x))
        data["unique_word_count_ppr"] = data["text_tokens"].apply(lambda x: len(set(x)))
        data["splling_err_num_ppr"] = tqdm(data["processed_text"].apply(self.spelling))
        
        data["processed_text"] = data["full_text"].apply(lambda x: dataPreprocessing_w_contract_punct_remove(x))
        data["text_tokens"] = data["processed_text"].apply(lambda x: word_tokenize(x))
        data["text_length_pcpr"] = data["processed_text"].apply(lambda x: len(x))
        data["word_count_pcpr"] = data["text_tokens"].apply(lambda x: len(x))
        data["unique_word_count_pcpr"] = data["text_tokens"].apply(lambda x: len(set(x)))
        data["splling_err_num_pcpr"] = tqdm(data["processed_text"].apply(self.spelling))
        data.drop(columns=["processed_text", "text_tokens"], inplace=True)
        return data
    
preprocessor = Preprocessor()