from llama_cpp import Llama
from .llm_enviroments import *
import os

class LLM_Analyzer:
    def __init__(self, model: str=MODEL, gpu_layers=GPU_LAYERS, n_batch=N_BATCH, n_ctx=N_CTX, n_threads=N_THREADS, n_threads_batch=N_THREADS_BATCH) -> None:
        self.llm = Llama(
                model_path='llm_integration/'+model,
                n_gpu_layers=gpu_layers,
                n_batch=n_batch,
                use_mlock=True,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_threads_batch=n_threads_batch
            )

    def review_comment(self, comment_text):
        llm_response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYS_PROMPT_1},
                {"role": "user", "content": PROMPT_1.replace("TEXT", comment_text)}
            ]
        )['choices'][0]['message']['content']
        self.llm.reset()
        return llm_response

    def extract_grade(self, review):
        llm_response_2 = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYS_PROMPT_2},
                {"role": "user", "content": review}
            ]
        )['choices'][0]['message']['content']
        return llm_response_2

    def grade_comment(self, comment):
        grade = self.extract_grade(self.review_comment(comment))

        #most common answers are 'grade/10', 'grade / 10', 'grade out of 10'
        #but also it can be normal int
        print(grade)
        if '/' in grade:
            grade = grade.split('/')
            if ' ' in grade[0]:
                grade = grade[0][:-1:]
            else:
                grade = grade[0]
        elif 'out' in grade:
            grade = grade.split('out')[0][:-1:]
        return int(grade)

# 0 out of 10 Nice commit fck yeah
# 7 out of 10 Not bad. But I would try to avoid unnecessery copy constructors. Also, you missed a destructor in class definition, there will be plenty of memory leaks
# comment_text = 'Nice commit fck yeah'
# analyzer = LLM_Analyzer()
# print(analyzer.grade_comment(comment_text))
# review = analyzer.review_comment('Nice commit fck yeah')
# print(review)
# grade = extract_grade(review)
# print(grade)