import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

def gen_output(prompt):

    ## v2 models
    model_path = 'openlm-research/open_llama_3b_v2'
    # model_path = 'openlm-research/open_llama_7b_v2'

    ## v1 models
    # model_path = 'openlm-research/open_llama_3b'
    # model_path = 'openlm-research/open_llama_7b'
    # model_path = 'openlm-research/open_llama_13b'
    
    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map='auto',offload_folder="offload",
    )
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    generation_output = model.generate(
        input_ids=input_ids, max_new_tokens=32
    )
    return (tokenizer.decode(generation_output[0]))

gen_output("why is the sky blue?")