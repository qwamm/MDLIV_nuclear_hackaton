from llama_cpp import Llama

llm_1 = Llama(
    model_path="capybarahermes-2.5-mistral-7b.Q3_K_L.gguf",
    n_gpu_layers=-1,
    n_batch=1024,
    use_mlock=True,
    n_ctx=4096,
    n_threads=10,
    n_threads_batch=10
)
comment_text = 'Not bad. But I would try to avoid unnecessery copy constructors. Also, you missed a destructor in class definition, there will be plenty of memory leaks'
system_prompt_1 = "You are an experienced specialist in code reviews. You will receive different comments on commits and gonna be asked to rank them"
prompt_1 = f"My collegue left a comment on my commit. Here is it's text: {comment_text}. Rank this comment from 0 to 10 based on how useful it is in terms of code reviews."
llm_response_1 = llm_1.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt_1},
        {"role": "user", "content": prompt_1}
    ]
)['choices'][0]['message']['content']
print(llm_response_1)

llm_2 = Llama(
    model_path="capybarahermes-2.5-mistral-7b.Q3_K_L.gguf",
    n_gpu_layers=-1,
    n_batch=1024,
    use_mlock=True,
    n_ctx=4096,
    n_threads=10,
    n_threads_batch=10
)
system_prompt_2 = "You will be given a comment from a specialist about some comment on code review. DO NOT add any comments and DO NOT provide any extra info. Just extract his grade of review."
prompt_2 = llm_response_1
llm_response_2 = llm_2.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt_2},
        {"role": "user", "content": prompt_2}
    ]
)['choices'][0]['message']['content']
print(llm_response_2)