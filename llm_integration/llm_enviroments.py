
#llm params
MODEL = "capybarahermes-2.5-mistral-7b.Q3_K_L.gguf"
GPU_LAYERS = -1
N_BATCH = 1024
N_CTX=4096
N_THREADS=10
N_THREADS_BATCH=10

#prompts
SYS_PROMPT_1 = "You are an experienced specialist in code reviews. You will receive different comments on commits and gonna be asked to rank them"
PROMPT_1 = "My collegue left a comment on my commit. Here is it's text: TEXT. Rank this comment from 0 to 10 based on how useful it is in terms of code reviews."
SYS_PROMPT_2 = "You will be given a comment from a specialist about some comment on code review. DO NOT add any comments and DO NOT provide any extra info. Just extract his grade(a SINGLE number) of review."
