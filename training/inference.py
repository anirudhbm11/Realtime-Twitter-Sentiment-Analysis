from joblib import load
from abc import abstractmethod, ABC
import re
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.linear_model import LogisticRegression

class MLmodelTasks(ABC):
    @abstractmethod
    def predict(self, data):
        pass

    def clean_data(self, text, stem=False):
        stop_words = stopwords.words('english')
        stemmer = SnowballStemmer('english')

        text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
        text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
        tokens = []
        for token in text.split():
            if token not in stop_words:
                if stem:
                    tokens.append(stemmer.stem(token))
                else:
                    tokens.append(token)
        return " ".join(tokens)

class LogisticRegression(MLmodelTasks):
    def predict(self, text):
        model = self.getModel()
        text = self.clean_data(text)
        vectorizer = load("training/tfidf_vectorizer.joblib")
        x_test  = vectorizer.transform([text])

        return model.predict(x_test[0])

    def getModel(self):
        model = load("training/logistic_soc.joblib")
        return model

class BertModel:
    def predict(self,data):
        #TODO
        return

class MLModel:
    def select_model(self, model_name):
        if model_name == "logistic_regression":
            return LogisticRegression()
        elif model_name == "Bert":
            return BertModel()


if __name__ == "__main__":
    models = MLModel()
    model = models.select_model("logistic_regression")
    print(model.predict(["Let's test this out. Not sure how it is gonna work"])[0])
        
