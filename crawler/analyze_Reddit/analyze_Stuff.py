from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier


# Calculation polarity / subjectivity
# print (TextBlob("Textblob is amazingly simple to use. What great fun!").sentiment)
# TODO: Textlänge, Wortkategorisierung, Erkennung ob Frage oder Satz / Antwort

wiki = TextBlob("Python is a high-level, general-purpose programming language.")

# cl = NaiveBayesClassifier(train)

print (dir(wiki))

print ()




# print (dir(wiki))

