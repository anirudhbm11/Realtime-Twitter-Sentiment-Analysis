from joblib import load
from abc import abstractmethod, ABC
import re
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.linear_model import LogisticRegression
from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification

class MLmodelTasks(ABC):
    @abstractmethod
    def predict(self, model, data):
        pass

    def clean_data(self, text, stem=False):
        # Cleaning the tweets
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
    def predict(self, model, text):
        # Predicting using saved Logistic Regression model
        # model = self.getModel()
        text = self.clean_data(text)
        vectorizer = load("training/tfidf_vectorizer.joblib")
        x_test  = vectorizer.transform([text])

        return model.predict(x_test[0])

    def getModel(self):
        model = load("training/logistic_soc.joblib")
        return model

class BertSent(MLmodelTasks):
    def predict(self, model, text):
        # Predicting using Bert model from Huggingface API
        # model = self.get_model()
        text = self.clean_data(text)
        tokenizer = AutoTokenizer.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
        input = tokenizer.encode(text, return_tensors="tf")
        output = model.predict(input)[0]
        sentiment = output.argmax().item()
        predicted_label = model.config.id2label[sentiment]

        return predicted_label

    def get_model(self):
        model = TFAutoModelForSequenceClassification.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
        return model


class MLModel:
    def select_model(self, model_name):
        if model_name == "logistic_regression":
            return LogisticRegression()
        elif model_name == "BertSent":
            return BertSent()


if __name__ == "__main__":
    # Testing models
    models = MLModel()
    model = models.select_model("BertSent")
    final_model = model.get_model()
    print(model.predict(final_model, ["This is bad. Really bad"]))
        
