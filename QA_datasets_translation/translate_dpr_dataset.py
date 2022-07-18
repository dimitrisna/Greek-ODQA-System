import json
import math
from deep_translator import GoogleTranslator
file=open('PATH_TO_DPR_DATASET',"r+", encoding="utf8")
data1=json.load(file, strict=False)
file.close()
item="""
	{
	        "dataset": "",
	        "question": "",
	        "answers": [
	            
	        ],
	        "positive_ctxs": [
	            
	        ],
	        "negative_ctxs": [
	            
	        ],
	        "hard_negative_ctxs": [
	            
	        ]
	}    
	"""
pos_con="""
		{
		    "title": "",
		    "text": "",
		    "score": 0,
		    "title_score": 0,
		    "passage_id": ""
		}
		"""
neg_con="""
{
    "title": "",
    "text": "",
    "score": 0,
    "title_score": 0,
    "passage_id": ""
}
"""
count=0
num_of_paragraphs=len(data1)
for pair in data1:
    count=count+1
    case=json.loads(item)
    case['dataset']=pair['dataset']
    case['question']=GoogleTranslator(source='en', target='el').translate(pair['question'])
    for ans in pair['answers']:
        case['answers'].append(GoogleTranslator(source='en', target='el').translate(ans))
    count1=0
    for pos in pair['positive_ctxs']:
        count1+=1
        if count1>3:
            break
        pos_context=json.loads(pos_con)
        pos_context['title']=GoogleTranslator(source='en', target='el').translate(pos['title'])
        pos_context['text']=GoogleTranslator(source='en', target='el').translate(pos['text'])
        pos_context['score']=pos['score']
        pos_context['title_score']=pos['title_score']
        pos_context['passage_id']=pos['passage_id']
        case['positive_ctxs'].append(pos_context)
    count2=0
    for neg in pair['hard_negative_ctxs']:
        count2+=1
        if count2>3:
            break
        neg_context=json.loads(neg_con)
        neg_context['title']=GoogleTranslator(source='en', target='el').translate(neg['title'])
        neg_context['text']=GoogleTranslator(source='en', target='el').translate(neg['text'])
        neg_context['score']=neg['score']
        neg_context['title_score']=neg['title_score']
        neg_context['passage_id']=neg['passage_id']
        case['hard_negative_ctxs'].append(neg_context)
    data2.append(case)
with open("PATH_TO_TRANSLATED_DPR_DATASET", "w") as file:
    json.dump(data2, file)
file.close()
    print("Θέμα ",count,"/",num_of_paragraphs, end='\r')
