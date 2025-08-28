from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import random

def generate_one_word_questions(paragraph):
    num_questions=10
    model_name = "valhalla/t5-base-qg-hl"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)


    sentences = paragraph.split(". ")
    count = 0

    for sentence in sentences:
        words = sentence.split()
        if len(words) < 4 or count >= num_questions:
            continue

        answer = random.choice(words).strip(".,")
        if not answer.isalpha():
            continue

        # Highlight the answer
        highlighted = sentence.replace(answer, f"<hl> {answer} <hl>")
        input_text = f"generate question: {highlighted}"
        input_ids = tokenizer.encode(input_text, return_tensors='pt')

        outputs = model.generate(input_ids)
        question = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"\nQuestion: {question}")
        #print(f"Answer: {answer}")
        count += 1
