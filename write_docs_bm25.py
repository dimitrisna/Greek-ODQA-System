import json
from haystack.nodes import PreProcessor
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
    split_length=400,
    split_overlap=100,
    split_respect_sentence_boundary=True,
    language="el"
)
docs=preprocessor.process(data[:20])
document_store.write_documents(docs)

