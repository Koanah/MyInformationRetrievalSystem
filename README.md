# MyIRSystem: Information Retrieval System

**MyIRSystem** is a Python-based Information Retrieval (IR) system that utilizes Wikipedia articles to retrieve relevant documents based on user queries. This system employs text processing techniques like tokenization, stemming, stopword removal, and named entity recognition (NER) to clean and analyze retrieved documents. It uses the TF-IDF (Term Frequency-Inverse Document Frequency) vector space model to rank documents by relevance to a given query.

## Features

- **Wikipedia Article Retrieval**: Retrieve articles from Wikipedia based on a user-defined query.
- **Text Preprocessing**: Clean and process the text using tokenization, stemming, stopword removal, and lowercase conversion.
- **Named Entity Recognition (NER)**: Extract named entities from the text for further analysis.
- **TF-IDF Vectorization**: Converts the cleaned text into a numerical representation using TF-IDF.
- **Document Ranking**: Ranks documents by relevance based on their similarity to the query.
- **Precision and Recall Evaluation**: Measures the effectiveness of document retrieval for different queries.

## Installation

To use the system,you can install the required packages manually:
pip install wikipedia-api
pip install nltk
pip install scikit-learn

## Usage

1. Query Wikipedia: Input a query, and the system retrieves relevant articles from Wikipedia.
2. Text Preprocessing: The system applies preprocessing techniques like tokenization, stemming, and stopword removal to clean the retrieved articles.
3. Document Ranking: The system ranks the documents using the TF-IDF vector space model and returns the most relevant articles.
4. Evaluation: The system calculates precision and recall for predefined queries to evaluate the effectiveness of the retrieval process.

## Evaluation

The system evaluates queries for their precision and recall by comparing the retrieved documents with a predefined set of relevant documents. Some of the sample queries evaluated include:

Machine Learning
Natural Language Processing
Artificial Intelligence
Information Retrieval
Deep Learning
The system calculates precision and recall for each query and outputs the average values for the entire evaluation set.

## Contributing

I welcome contributions to improve the system. If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request. Make sure to update the documentation as necessary.


## Acknowledgments

Wikipedia API for retrieving articles.
NLTK for natural language processing and text cleaning.
Scikit-learn for the TF-IDF vectorization and cosine similarity.
