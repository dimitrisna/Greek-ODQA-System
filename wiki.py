import json
data="""
{
    "content": "",
    "meta": {"id": "", "revid": "", "url": "", "title": ""}
}
"""
input_filename = "wiki_00"
output_filename="wiki_dataset.json"
with open(input_filename) as f:
    dataset = list(f)
docs=[]

num_of_paragraphs=len(dataset)
print(num_of_paragraphs)
counter=0
for item in dataset:
    counter+=1
    item=json.loads(item)
    a=json.loads(data)
    a['content']=item.pop("text")
    if a['content']=="":
      continue
    a['meta']=item
    docs.append(a)
    print("Θέμα ",counter,"/",num_of_paragraphs)
with open(output_filename, "w") as f:
    json.dump(docs, f, indent=4)




