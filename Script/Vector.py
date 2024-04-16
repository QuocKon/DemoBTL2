import pandas as pd
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load the CSV file into a DataFrame
df = pd.read_csv("D:/KI 2 NAM 3/Python/BTL/Demo/Script/Begin_infor.csv")
df1 = pd.read_csv("D:/KI 2 NAM 3/Python/BTL/Demo/Script/Malware_infor.csv")

# Preprocess the data and create TaggedDocument objects
tagged_data = []
vectorizer = TfidfVectorizer(stop_words="english", lowercase=True)

for i, row in df.iterrows():
    api_call = row['API call']  # Assuming 'API call' contains space-separated words
    permissions = row['permissions']  # Assuming 'permissions' contains space-separated words
    intent = row['intent'] # Assuming 'intent' contains space-separated words
    words = api_call + permissions + intent
    tagged_data.append(TaggedDocument(words=words, tags='B'))
for i, row in df1.iterrows():
    api_call = row['API call']  # Assuming 'API call' contains space-separated words
    permissions = row['permissions']  # Assuming 'permissions' contains space-separated words
    intent = row['intent'] # Assuming 'intent' contains space-separated words
    words = api_call + permissions + intent
    tagged_data.append(TaggedDocument(words=words, tags='M'))
vectorizer = TfidfVectorizer(stop_words="english", lowercase=True)
 
train_data,test_data = train_test_split(tagged_data, test_size=0.2, random_state=42)

# Khởi tạo và huấn luyện mô hình Doc2Vec
model_doc2vec = Doc2Vec(vector_size=50, min_count=2, epochs=40)
model_doc2vec.build_vocab(tagged_data)
model_doc2vec.train(tagged_data, total_examples=model_doc2vec.corpus_count, epochs=model_doc2vec.epochs)

# In ra vector của một 5 văn bản đầu tiên
for i, doc in enumerate(tagged_data[:5]):
    print(f"Vector của văn bản {i+1}: {model_doc2vec.infer_vector([word for word in doc.words])}")

# Lưu các vector của các văn bản vào một DataFrame
vectors = [model_doc2vec.infer_vector(doc.words.split()) for doc in tagged_data]
vectors_df = pd.DataFrame(vectors)
vectors_df.to_csv("vectors.csv", index=False)

# # Tạo các vector biểu diễn cho tập huấn luyện và tập kiểm tra
# X_train = [model_doc2vec.infer_vector(doc.words.split()) for doc in train_data]
# X_test = [model_doc2vec.infer_vector(doc.words.split()) for doc in test_data]

# # # Chuẩn bị nhãn mục tiêu
# y_train = [doc.tags[0]for doc in train_data]
# y_test = [doc.tags[0] for doc in test_data]

# # # Huấn luyện một bộ phân loại Random Forest
# clf = RandomForestClassifier()
# clf.fit(X_train, y_train)

# Đánh giá bộ phân loại
#y_pred = clf.predict(X_test)
#print(classification_report(y_test, y_pred))

