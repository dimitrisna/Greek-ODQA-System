import json
#convert a QA datataset from SQuAD-like format to HuggingFace format
input_filename = "PATH_TO_SQUAD-LIKE_DATASET"
output_filename = "PATH_TO_HF_TYPE_DATASET"

with open(input_filename) as f:
    dataset = json.load(f)

with open(output_filename, "w") as f:
    for article in dataset["data"]:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]
            answers = {}
            for qa in paragraph["qas"]:
                question = qa["question"]
                idx = qa["id"]
                #if qa.get('plausible_answers')==None:
                answers["text"] = [a["text"] for a in qa["answers"]]
                answers["answer_start"] = [a["answer_start"] for a in qa["answers"]]
                #else:
                #    answers["text"] = [a["text"] for a in qa["plausible_answers"]]
                #    answers["answer_start"] = [a["answer_start"] for a in qa["plausible_answers"]]
                f.write(
                    json.dumps(
                        {
                            "id": idx,
                            "context": context,
                            "question": question,
                            "answers": answers,
                        }
                    )
                )
                f.write("\n")

