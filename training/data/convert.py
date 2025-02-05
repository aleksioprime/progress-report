import json

def convert_txt_to_jsonl(txt_path, jsonl_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        reviews = f.readlines()

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for review in reviews:
            json.dump({"text": review.strip()}, f, ensure_ascii=False)
            f.write("\n")

convert_txt_to_jsonl("data/reviews.txt", "data/reviews.jsonl")