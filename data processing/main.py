from pymongo import MongoClient
import pandas as pd
import datetime
import spacy
from time import time
nlp = spacy.load("en_core_web_sm")

#wpisujemy haslo ktorego szukamy i nazwe pliku .csv, ktory posluzy potem do merge'a
szukanedane = 'TSL'
nazwapliku = 'danetesla.csv'

class Database:

    def __init__(self):
        self.i = 0
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.reddit
        self.collection_submissions = self.db.submissions
        self.collection_comments = self.db.comments
        self.list_of_all = []
        self.df = None
        self.get_list()
        self.get_df()

        self.df_gme = self.df[self.df.selftext.str.contains(szukanedane, na = False)]
        self.df_gme = self.df_gme.sort_values(by=['created_utc'])
        self.df_gme = self.df_gme.reset_index()
        print(self.df_gme.shape)
        self.df_gme['selftext'] = self.df_gme.selftext.apply(lambda text: self.tokenize(text))
        self.save_to_csv(self.df_gme)
    def get_list(self):
        for _ in self.collection_comments.find({},{"body": 1,"created_utc": 1}):
            self.i += 1
            newkey = 'selftext'
            oldkey = 'body'
            _[newkey] = _.pop(oldkey)
            _['created_utc'] = datetime.datetime.fromtimestamp(int(_['created_utc']))
            _[newkey] = _[newkey]
            self.list_of_all.append(_)
        for _ in self.collection_submissions.find({},{"selftext": 1, "created_utc": 1}):
            _['created_utc'] = datetime.datetime.fromtimestamp(int(_['created_utc']))
            self.list_of_all.append(_)

    def tokenize(self, text):
        start_time = time()
        #customize_stop_words = [',']
        nlp = spacy.load("en_core_web_sm")
        #for w in customize_stop_words:
        #    nlp.vocab[w].is_stop = True
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc]
        tokens_without_sw = [word for word in tokens if not nlp.vocab[word].is_stop]#stopwords.words('english')]
        print(time() - start_time) #czas tokenizowania jednego wiersza DF'a
        return tokens_without_sw
        #self.df['selftext'] = self.df.selftext.apply(lambda text: self.tokenize(text)))

    def tokenize_threading(self, df):
        df.selftext.apply(lambda text: self.tokenize(text))

    def get_df(self):
        self.df = pd.DataFrame(self.list_of_all)
        self.df = self.df[self.df.selftext != '[removed]']
    def save_to_csv(self, df):
        df.to_csv(nazwapliku, index=False)

#submissions
#'selftext' 'title' 'created_utc'
#comments
#'body' 'created_utc'
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    start_time = time()
    baza = Database()
    print(baza.df_gme)
    print(time() - start_time)