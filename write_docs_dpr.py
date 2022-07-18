import json
from haystack.nodes import PreProcessor,DensePassageRetriever
from haystack.document_stores import ElasticsearchDocumentStore
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
file=open('wiki_dataset.json',"r+", encoding="utf8")
data=json.load(file, strict=False)
file.close()
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=100,
    split_overlap=50,
    split_respect_sentence_boundary=True,
    language="el"
)
docs=preprocessor.process(data[:20])
document_store.write_documents(docs)

retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="Danastos/dpr_query_el_1",
    passage_embedding_model="Danastos/dpr_passage_el_1",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=False,
    use_fast_tokenizers=True,
)
document_store.update_embeddings(retriever)
