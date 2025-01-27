# -*- coding: utf-8 -*-
"""MyIRSystem.ipynb

Original file is located at
    https://colab.research.google.com/drive/1SHicAj8HJED-iWrsaQi0eR8YS7oJN1Ue
"""

!pip install wikipedia-api
import wikipediaapi
import requests
#using wikipedia to source out documents
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag, ne_chunk

#creating an instance of wikipedia with the english language code
#to retrieve info from the english wikipedia
wiki= wikipediaapi.Wikipedia(language='en',user_agent='MyIRSystem/1.0 (GoogleColab)')

#retrieving wikipedia articles based on a search query
def get_wikipedia_articles(query, num_articles=7):
  # getting the wikipedia page for that has query answer
  query = query.lower()
  page=wiki.page(query)
  if(page.exists()):
    #header = page.title
    #content = page
    #Splits the text of the page into lines and returns the first num_articles lines
    return page.text.split('\n')[:num_articles]
   #return header, content.split('\n')[:num_articles]
  else:
    return None

"""def get_wikipedia_articles(query, num_articles=5):
    try:
        # Construct the URL for the Wikipedia search API
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json&srprop=snippet&utf8="
        # Make a GET request to the API
        response = requests.get(url)
        # Parse the JSON response
        data = response.json()
        # Extract search results
        search_results = data['query']['search'][:num_articles]
        # Extract page titles and construct links
        page_links = [f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}" for result in search_results]
        return page_links
    except Exception as e:
        print(f"An error occurred: {e}")
        return None"""

#performing TOKENIZATION,LOWERCASING,STEMMING,STOPWORD REMOVAL to clean text data
def preprocess_text(text):
  #tokenize the text based on whitespace and punctuation
  tokens = word_tokenize(text)
  #convert tokens to lowerCase
  tokens = [token.lower() for token in tokens]
  #remove stopwords and punctuation
  #isalnum() checks whether all char in a string are alphanumeriv(a-z,A-Z OR 0-9)
  tokens = [token for token in tokens if token not in stopwords.words('english')and token.isalnum()]
  #stemming the tokens
  stemmer = PorterStemmer()
  tokens = [stemmer.stem(token) for token in tokens]
  return ' '.join(tokens)

#extracting name entities using Nltk's NER
#returns a list of named entities from the text
def extract_entities(text):
  entities = []
  ## Checking if the chunk has a 'label' attribute, indicating it is a named entity
  for chunk in ne_chunk(pos_tag(word_tokenize(text))):
    if hasattr(chunk,'label'):
      entities.append(' '.join(c[0] for c in chunk))
  return entities

#creating the TF-IDF vector space model
def create_vector_space_model(documents):
  #Fitting the vectorizer to the documents and transform the documents into a TF-IDF matrix
  vectorizer = TfidfVectorizer(preprocessor=preprocess_text)
  tfidf_matrix = vectorizer.fit_transform(documents)
  return tfidf_matrix, vectorizer #ReturnS the TF-IDF matrix and the fitted vectorizer

#retrieving the documents relevant to the query
def retrieve_documents(query,documents,vectorizer, tfidf_matrix):

  #converting the query into a TF-IDF vector
  query_vector = vectorizer.transform([query])
  #calculating the cosine similarity between the query vector and document vector
  similarity_scores = tfidf_matrix.dot(query_vector.T) .toarray().flatten()
  #ranking the documents based on similarity scores
  ranked_indices = similarity_scores.argsort()[::-1]
  #retrieving the documents in ranked order
  ranked_documents = [documents[i] for i in ranked_indices]
  return ranked_documents #List of relevant documents ranked by similarity to the query.

import re
query= str(input())
#cleaning the text for special characters
query = re.sub(r'[^\w\s]', '',query)
#query="kim kardashian"
articles = get_wikipedia_articles(query)
preprocessed_articles = [preprocess_text(article) for article in articles]
tfidf_matrix, vectorizer = create_vector_space_model(preprocessed_articles)
relevant_documents = retrieve_documents(query, preprocessed_articles,vectorizer, tfidf_matrix)

for doc in relevant_documents:
    print(', '.join([f'"{doc}"']))

queries=[
    "Machine learning",
    "Natural language processing",
    "Artificial intelligence",
    "Information retrieval",
    "Deep learning"
]
relevant_documents={"Machine learning":[
"theoret viewpoint probabl approxim correct pac learn provid framework describ machin learn",
"machin learn ml field studi artifici intellig concern develop studi statist algorithm learn data gener unseen data thu perform task without explicit instruct recent artifici neural network abl surpass mani previou approach perform",
"ml find applic mani field includ natur languag process comput vision speech recognit email filter agricultur medicin appli busi problem known name predict analyt although machin learn statist base comput statist import sourc field method",
"mathemat foundat ml provid mathemat optim mathemat program method data mine relat parallel field studi focus exploratori data analysi eda unsupervis learn"

    ],
    "Natural language processing": [
"natur languag process nlp interdisciplinari subfield comput scienc inform retriev primarili concern give comput abil support manipul human languag involv process natur languag dataset text corpora speech corpora use either probabilist statist recent neural machin learn approach goal comput capabl understand content document includ contextu nuanc languag within end natur languag process often borrow idea theoret linguist technolog accur extract inform insight contain document well categor organ document",
"POTATOES WERE MADE IN MANHATTHAN"
"natur languag process root 1940 alreadi 1940 alan ture publish articl titl comput machineri intellig propos call ture test criterion intellig though time articul problem separ artifici intellig propos test includ task involv autom interpret gener natur languag",

    ],
    "Artificial intelligence": [
"artifici intellig ai broadest sens intellig exhibit machin particularli comput system field research comput scienc develop studi method softwar enabl machin perceiv environ use learn intellig take action maxim chanc achiev defin goal machin may call ai"
"alan ture first person conduct substanti research field call machin intellig artifici intellig found academ disciplin 1956 field went multipl cycl optim follow period disappoint loss fund known ai winter fund interest vastli increas 2012 deep learn surpass previou ai techniqu 2017 transform architectur led ai boom earli 2020 compani univers laboratori overwhelmingli base unit state pioneer signific advanc artifici intellig",
"grow use artifici intellig 21st centuri influenc societ econom shift toward increas autom integr ai system variou econom sector area life impact job market healthcar govern industri educ rais question effect ethic implic risk ai prompt discuss regulatori polici ensur safeti benefit technolog",
"variou subfield ai research center around particular goal use particular tool tradit goal ai research includ reason knowledg represent plan learn natur languag process percept support robot gener abil complet task perform human least equal among field goal"
"ai technolog wide use throughout industri govern scienc applic includ advanc web search engin googl search recommend system use youtub amazon netflix interact via human speech googl assist siri alexa autonom vehicl waymo gener creativ tool chatgpt ai art superhuman play analysi strategi game chess go howev mani ai applic perceiv ai lot cut edg ai filter gener applic often without call ai someth becom use enough common enough label ai anymor"
],
    "Information retrieval": [
        "Information retrieval",
        "Vector space model",
        "Boolean retrieval",
        "Probabilistic retrieval"
    ],
    "Deep learning": [
        "Deep learning",
        "Artificial neural networks",
        "Convolutional neural networks",
        "Recurrent neural networks"
    ]
}

precision_scores=[]
recall_scores=[]
#iterating over queries
for query in queries:
  #retrieve documents for the query from the wikipedia api
  articles = get_wikipedia_articles(query)
  preprocessed_articles = [preprocess_text(article) for article in articles]
  tfidf_matrix, vectorizer = create_vector_space_model(preprocessed_articles)
  retrieved_documents = retrieve_documents(query, preprocessed_articles, vectorizer, tfidf_matrix)

#calculating precision and recall
  relevant_retrieved = len(set(retrieved_documents)& set(relevant_documents[query]))
  precision = relevant_retrieved/ len(relevant_documents[query])
  recall = relevant_retrieved/len(relevant_documents[query])

  precision_scores.append(precision)
  recall_scores.append(recall)

  print(f"Query: {query}, Precision: {precision}, Recall:{recall}")

#calculate average precision and recall
avg_prec = sum(precision_scores)/len(queries)
avg_rec = sum(recall_scores)/len(queries)

print(f"Average Precision: {avg_prec}, Average Recall: {avg_rec}")
