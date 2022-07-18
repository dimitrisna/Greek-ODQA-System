import json
import time
from deep_translator import GoogleTranslator
file=open('PATH_TO_SQUAD-LIKE_FILE',"r+", encoding="utf8")
data=json.load(file, strict=False)
file.close()
count=0
num_of_data=len(data['data'])
for case in data['data']:
    count=count+1
    print("")#if the dataset doesn't contain titles, comment the next 3 lines out
    print(case['title'])
    case['title']=GoogleTranslator(source='en', target='el').translate(case['title'].strip())
    print(case['title'])
    count1=0
    num_of_paragraphs=len(case['paragraphs'])
    for item in case['paragraphs']:
        count1+=1
        print("Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs, end='\r')
        context=item['context']
        len_of_context=len(item['context'])
        if len_of_context<5000:
            item['context']=GoogleTranslator(source='en', target='el').translate(item['context'])
        elif len_of_context<9500:
            tran_index=context.rfind('.',0,4800)
            item['context']=GoogleTranslator(source='en', target='el').translate(item['context'][:tran_index])+GoogleTranslator(source='en', target='el').translate(item['context'][tran_index+1:])
        else:
            tran_index1=context.rfind('.',0,4800)
            tran_index2=context.rfind('.',tran_index1,tran_index1+4800)
            item['context']=GoogleTranslator(source='en', target='el').translate(item['context'][:tran_index1])+GoogleTranslator(source='en', target='el').translate(item['context'][tran_index1+1:tran_index2])+GoogleTranslator(source='en', target='el').translate(item['context'][tran_index2+1:])
        for qa in item['qas']:
            check_same_answer=0
            check_same_planswer=0
            qa['question']=GoogleTranslator(source='en', target='el').translate(qa['question'].strip())        
            for ans in qa['answers']:
                text=ans['text']
                answers=answers+1
                try:
                    if not ans['text'].isdecimal():
                        ans['text']=GoogleTranslator(source='en', target='el').translate(ans['text'])
                except BaseException:
                    print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
                try:
                    word_appear=item['context'].count(ans['text']) 
                except TypeError:
                    print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
                    continue
                if word_appear==1:
                    ans['answer_start']=item['context'].find(ans['text'])
                elif word_appear>1:
                    word_appear=context.count(text,0,ans['answer_start'])+1
                    ans['answer_start']=0
                    while(word_appear>0):
                        ans['answer_start']=item['context'].find(ans['text'],ans['answer_start']+1)
                        word_appear-=1
                else:
                    temp_index=ans['answer_start']
                    if check_same_answer==1:
                        if text==previus_text and temp_index==previus_index:
                            ans['answer_start']=previus_tr_index
                            ans['text']=previus_tr_text
                            continue

                    marked_context=context[:temp_index]+'/*  '+context[temp_index:(temp_index+len(text))]+'  */'+context[(temp_index+len(text)):]
                    if len(marked_context)<5000:
                        tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context)
                    elif len(marked_context)<9500:
                        tran_index=context.rfind('.',0,4800)
                        tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context[:tran_index])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index+1:])
                    else:
                        tran_index1=context.rfind('.',0,4800)
                        tran_index2=context.rfind('.',tran_index1,tran_index1+4800)
                        tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context[:tran_index1])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index1+1:tran_index2])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index2+1:])
                    pos_answer_start=tran_marked_context.find('/*')
                    pos_end=tran_marked_context.find('*/',pos_answer_start+3)
                    pos_text=tran_marked_context[pos_answer_start+3:pos_end-1]
                    if ('/*/' in tran_marked_context) or (pos_text.strip()=="") or pos_answer_start==-1 or pos_end==-1:
                    	ans['text']="DONTUSE"
                    	continue
                    if pos_text[-1]=="." or pos_text[-1]=="," or pos_text[-1]=="!":
                        pos_text=pos_text[:-1]
                    try:
	                    word_appear=item['context'].count(pos_text) 
                    except TypeError:
	                    print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
	                    continue
                    if word_appear==1:
                        ans['text']=pos_text
                        ans['answer_start']=item['context'].find(ans['text'])
                    elif word_appear>1:
                        ans['text']=pos_text
                        word_appear=context.count(text,0,ans['answer_start'])+1
                        ans['answer_start']=0
                        while(word_appear>0):
                            ans['answer_start']=item['context'].find(ans['text'],ans['answer_start']+1)
                            word_appear-=1
                    else:
                        #comparing the text outside markers. If it is the same after both translations, the answer
                        #is the between the markers text in the first translation.Otherwise, the entry is deleted.
                        outside_end=tran_marked_context[pos_end+3:]
                        if item['context'].find(outside_start)!=-1 and item['context'].find(outside_end)!=-1:
                            ans['answer_start']=(item['context'].find(outside_start)+len(outside_start))
                            ans['text']=item['context'][ans['answer_start']:(item['context'].find(outside_end)-1)]
                        else:
                            ans['text']='DONTUSE'
                    previus_index=temp_index
                    previus_text=text
                    previus_tr_index=ans['answer_start']
                    previus_tr_text=ans['text']
                    check_same_answer=1
            if qa.get('plausible_answers')!=None:
                for ans in qa['plausible_answers']:
                    text=ans['text']
                    answers=answers+1
                    try:
                        if not ans['text'].isdecimal():
                            ans['text']=GoogleTranslator(source='en', target='el').translate(ans['text'])
                    except BaseException:
                        print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
                    try: 
                        word_appear=item['context'].count(ans['text']) 
                    except TypeError:
                        print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
                        continue
                    if word_appear==1:
                        ans['answer_start']=item['context'].find(ans['text'])
                    elif word_appear>1:
                        word_appear=context.count(text,0,ans['answer_start'])+1
                        ans['answer_start']=0
                        while(word_appear>0):
                            ans['answer_start']=item['context'].find(ans['text'],ans['answer_start']+1)
                            word_appear-=1
                    else:
                        temp_index=ans['answer_start']
                        if check_same_answer==1:
                            if text==previus_text and temp_index==previus_index:
                                ans['answer_start']=previus_tr_index
                                ans['text']=previus_tr_text
                                continue
                        marked_context=context[:temp_index]+'/*  '+context[temp_index:(temp_index+len(text))]+'  */'+context[(temp_index+len(text)):]
                        if len(marked_context)<5000:
                            tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context)
                        elif len(marked_context)<9500:
                            tran_index=context.rfind('.',0,5000)
                            tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context[:tran_index])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index+1:])
                        else:
                            tran_index1=context.rfind('.',0,4800)
                            tran_index2=context.rfind('.',tran_index1,tran_index1+4800)
                            tran_marked_context=GoogleTranslator(source='en', target='el').translate(marked_context[:tran_index1])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index1+1:tran_index2])+GoogleTranslator(source='en', target='el').translate(marked_context[tran_index2+1:])
                        pos_answer_start=tran_marked_context.find('/*')
                        pos_end=tran_marked_context.find('*/',pos_answer_start+3)
                        pos_text=tran_marked_context[pos_answer_start+3:pos_end-1]
                        if ('/*/' in tran_marked_context) or (pos_text.strip()=="") or pos_answer_start==-1 or pos_end==-1:
                            ans['text']="DONTUSE"
                            continue
                        if pos_text[-1]=="." or pos_text[-1]=="," or pos_text[-1]=="!":
                            pos_text=pos_text[:-1]
                        try:
                            word_appear=item['context'].count(pos_text) 
                        except TypeError:
                            print("error","Θέμα ",count,"/",num_of_data," Παράγραφος ",count1,"/",num_of_paragraphs)
                            continue
                        if word_appear==1:
                            ans['text']=pos_text
                            ans['answer_start']=item['context'].find(ans['text'])
                        elif word_appear>1:
                            ans['text']=pos_text
                            word_appear=context.count(text,0,ans['answer_start'])+1
                            ans['answer_start']=0
                            while(word_appear>0):
                                ans['answer_start']=item['context'].find(ans['text'],ans['answer_start']+1)
                                word_appear-=1
                        else:
							#comparing the text outside markers. If it is the same after both translations, the answer
                            #is the between the markers text in the first translation.Otherwise, the entry is deleted.
                            outside_start=tran_marked_context[:pos_answer_start]
                            outside_end=tran_marked_context[pos_end+3:]
                            if item['context'].find(outside_start)!=-1 and item['context'].find(outside_end)!=-1:
                                ans['answer_start']=(item['context'].find(outside_start)+len(outside_start))
                                ans['text']=item['context'][ans['answer_start']:(item['context'].find(outside_end)-1)]
                            else:
                                ans['text']='DONTUSE'

                    previus_index=temp_index
                    previus_text=text
                    previus_tr_index=ans['answer_start']
                    previus_tr_text=ans['text']
                    check_same_answer=1                            
casei=0
while casei<len(data['data']):
    itemi=0
    while itemi<len(data['data'][casei]['paragraphs']):
        qai=0
        while qai<len(data['data'][casei]['paragraphs'][itemi]['qas']):
            hold_question=0
            i=0
            if data['data'][casei]['paragraphs'][itemi]['qas'][qai].get('plausible_answers')!=None:
                while i<len(data['data'][casei]['paragraphs'][itemi]['qas'][qai]['plausible_answers']):
                    if data['data'][casei]['paragraphs'][itemi]['qas'][qai]['plausible_answers'][i]['text']=='' or data['data'][casei]['paragraphs'][itemi]['qas'][qai]['plausible_answers'][i]['text']=='DONTUSE' or data['data'][casei]['paragraphs'][itemi]['qas'][qai]['plausible_answers'][i]['text']==None:
                        data['data'][casei]['paragraphs'][itemi]['qas'][qai]['plausible_answers'].pop(i)
                    else:
                        hold_question=1
                        i+=1 
            else:
                if len(data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers'])==0:
                    hold_question=1
                while i<len(data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers']):
                    if data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers'][i]['text']=='' or data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers'][i]['text']=='DONTUSE' or data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers'][i]['text']==None:
                        data['data'][casei]['paragraphs'][itemi]['qas'][qai]['answers'].pop(i)
                    else:
                        hold_question=1
                        i+=1    
            if hold_question==0:
                data['data'][casei]['paragraphs'][itemi]['qas'].remove(data['data'][casei]['paragraphs'][itemi]['qas'][qai]) 
            else:
                qai+=1             
        if len(data['data'][casei]['paragraphs'][itemi]['qas'])==0:
            data['data'][casei]['paragraphs'].remove(data['data'][casei]['paragraphs'][itemi])
        else:
            itemi+=1    
    if len(data['data'][casei]['paragraphs'])==0:
        data['data'].remove(data['data'][casei]) 
    else:
        casei+=1                                      
with open("PATH_TO_TRANSLATED_SQUAD-LIKE_FILE", "w") as file:
    json.dump(data, file)
file.close()