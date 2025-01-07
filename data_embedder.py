"""
Menggunakan fasttext
"""

import numpy as np

import json
import fasttext as ft

import sentence_normalizer


# memproses data dengan menggunakan model embedding FastText.
def parse_data(ft_model):
    with open("dataset.json") as file:
        data = json.load(file)

    # Membuat list kosong untuk menyimpan pola kalimat yang telah di embedded.
    embedded_patterns = []
    for intent in data["intents"]:  # Melakukan iterasi pada setiap intent dalam data.

        # Melakukan iterasi pada setiap pola kalimat dalam intent.
        for pattern in intent["patterns"]:
            # Memproses pola kalimat menggunakan fungsi preprocess_main() untuk normalisasi.
            pattern = sentence_normalizer.preprocess_main(pattern)
            # kalimat menggunakan model embedding FastText.
            embedded_sentence = embed_sentence(pattern, ft_model)

            embedded_patterns.append(
                embedded_sentence
            )  # Menambahkan kalimat yang telah diembedd ke dalam list embedded_patterns
        # Mengubah list embedded_patterns menjadi array numpy dan kemudian ke list, dan menyimpannya kembali ke dalam intent.
        intent["patterns"] = np.array(embedded_patterns).tolist()

    return data


def embed_sentence(sentence, ft_model):
    sentence_vec = ft_model.get_sentence_vector(sentence)  # Mendapatkan vektor
    return sentence_vec


def write_embedded_data(data):
    json_object = json.dumps(data, indent=4)

    with open("embedded_data.json", "w") as outfile:
        outfile.write(json_object)


# memuat model embedding FastText.
def load_embedding_model():
    ft_model = ft.load_model("cc.id.300.bin")
    return ft_model


if __name__ == "__main__":
    ft_model = load_embedding_model()
    embedded_data = parse_data(ft_model)
    write_embedded_data(embedded_data)


"""
Developed using spacy
"""

# import json
# import spacy
# import numpy as np
# import sentence_normalizer


# def parse_data(nlp):
#     with open("dataset.json") as file:
#         data = json.load(file)

#     embedded_patterns = []
#     for intent in data["intents"]:
#         for pattern in intent["patterns"]:
#             pattern = sentence_normalizer.preprocess_main(pattern)
#             embedded_sentence = embed_sentence(pattern, nlp)
#             embedded_patterns.append(embedded_sentence)
#         intent["patterns"] = np.array(embedded_patterns).tolist()

#     return data


# def embed_sentence(sentence, nlp):
#     doc = nlp(sentence)
#     sentence_vec = doc.vector
#     # sentence_vec = nlp.get_sentence_vector(sentence)
#     return sentence_vec


# def write_embedded_data(data):
#     json_object = json.dumps(data, indent=4)
#     with open("embedded_data.json", "w") as outfile:
#         # json.dump(data, outfile, indent=4)
#         outfile.write(json_object)


# def load_nlp_model():
#     # Anda bisa menggunakan model bahasa Inggris yang telah dilatih, seperti "en_core_web_md"
#     nlp = spacy.load("en_core_web_md")
#     return nlp


# if __name__ == "__main__":
#     nlp = load_nlp_model()
#     embedded_data = parse_data(nlp)
#     write_embedded_data(embedded_data)


# """
# Developed using gensim
# """

# import numpy as np
# import json
# from gensim.models import KeyedVectors
# import sentence_normalizer


# def parse_data(w2v_model):
#     with open("dataset.json") as file:
#         data = json.load(file)

#     embedded_patterns = []
#     for intent in data["intents"]:
#         for pattern in intent["patterns"]:
#             pattern = sentence_normalizer.preprocess_main(pattern)
#             embedded_sentence = embed_sentence(pattern, w2v_model)
#             embedded_patterns.append(embedded_sentence)
#         intent["patterns"] = np.array(embedded_patterns).tolist()

#     return data


# def embed_sentence(sentence, w2v_model):
#     tokens = sentence.split()
#     # Inisialisasi vektor kosong
#     vector = np.zeros(300)
#     # Jumlah token
#     n_words = 0
#     # Iterasi setiap kata dalam kalimat
#     for word in tokens:
#         # Cek apakah kata ada dalam model
#         if word in w2v_model:
#             # Tambahkan vektor kata ke vektor kalimat
#             vector += w2v_model[word]
#             n_words += 1
#     # Normalisasi dengan jumlah kata
#     if n_words != 0:
#         vector /= n_words
#     return vector


# def write_embedded_data(data):
#     json_object = json.dumps(data, indent=4)
#     with open("embedded_data.json", "w") as outfile:
#         outfile.write(json_object)


# def load_embedding_model():
#     # Load model Word2Vec
#     w2v_model = KeyedVectors.load_word2vec_format("cc.en.300.vec")
#     return w2v_model


# if __name__ == "__main__":
#     w2v_model = load_embedding_model()
#     embedded_data = parse_data(w2v_model)
#     write_embedded_data(embedded_data)
