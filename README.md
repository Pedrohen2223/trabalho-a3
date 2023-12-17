import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt

# Carregando o modelo spaCy para o idioma Português
nlp = spacy.load("pt_core_news_sm", disable=["tagger", "parser", "ner"])

# Função de pré-processamento
def preprocess(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Função para extrair tópicos usando LDA
def extract_topics(texts):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X)

    topics = lda.transform(X)
    return topics

# Função para construir o grafo de similaridade
def build_similarity_graph(topics):
    graph = nx.Graph()

    for i in range(len(topics)):
        for j in range(i + 1, len(topics)):
            similarity = cosine_similarity([topics[i]], [topics[j]])[0][0]
            graph.add_edge(i, j, weight=similarity)

    return graph

# Função para visualizar o grafo
def visualize_graph(graph):
    pos = nx.spring_layout(graph)  # Pode usar outros layouts dependendo do tamanho do grafo
    nx.draw(graph, pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

# Exemplo de uso
documents = [
    "Inteligência artificial é um campo da ciência da computação que busca criar máquinas capazes de realizar tarefas que requerem inteligência humana.",
    "O processamento de linguagem natural é uma subárea da inteligência artificial que foca na interação entre computadores e linguagem humana.",
    "Algoritmos de aprendizado de máquina são frequentemente utilizados em projetos de inteligência artificial para melhorar o desempenho das máquinas em tarefas específicas.",
]

# Pré-processamento dos documentos
preprocessed_documents = [preprocess(doc) for doc in documents]

# Extração de tópicos
topics = extract_topics(preprocessed_documents)

# Construção do grafo de similaridade
similarity_graph = build_similarity_graph(topics)

# Visualização do grafo
visualize_graph(similarity_graph)
