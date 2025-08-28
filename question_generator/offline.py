import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
def questions(paragraph):
    def generate_fill_in_the_blanks(paragraph, num_questions=10):
        sentences = sent_tokenize(paragraph)
        questions = []

        for sent in sentences:
            words = word_tokenize(sent)
            tagged = pos_tag(words)

            for i, (word, tag) in enumerate(tagged):
            
                if tag.startswith('NN') and word.isalpha():
                    blanked_sentence = words[:i] + ['______'] + words[i+1:]
                    question = ' '.join(blanked_sentence)
                    questions.append((question, word))
                    break 

            if len(questions) >= num_questions:
                break

        return questions
    fill_blanks = generate_fill_in_the_blanks(paragraph)

    for i, (q, ans) in enumerate(fill_blanks, 1):
        print(f"Q{i}: {q}")
        print(f"   Answer: {ans}\n")
