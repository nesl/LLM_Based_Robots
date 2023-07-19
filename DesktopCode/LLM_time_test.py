import time
start_time = time.time()
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("WizardLM/WizardCoder-15B-V1.0")
model = AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-15B-V1.0")
print("Model loaded")

prompt_file_path = '/home/pragya/LLMCode/prompt.txt'
code_file_path = '/home/pragya/LLMCode/LLM_generated_code_time.py'

try:
	with open (prompt_file_path, 'r') as prompt_file:
		prompt = prompt_file.read()
		
except Exception as e:
	print("Error when read from file prompt.txt:", str(e))
	exit(e)

print("Finished reading prompt")
# tokenize prompt and model generate
try:
	inputs = tokenizer(prompt, return_tensors="pt").input_ids
	outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_new_tokens = 10000, temperature=0.2, do_sample=True, top_k=15, top_p=0.95)
except Exception as e:
	print("Error when tokenize input the generate output:", str(e))
	exit(e)

# decode output
try:
	code = tokenizer.batch_decode(outputs, skip_special_tokens=True)

except Exception as e:
	print("Error when decoding:", str(e))
	exit(e)

print("Saving code to file")
# save to code file
try:
	with open(code_file_path, 'w', encoding='UTF-8') as code_file:
		for item in code:
			code_file.write(str(item) + '\n')
			print(item)
except Exception as e:
	print("Error when write file LLM_genereated_code_test.py:", str(e))
	exit(e)


end_time = time.time()
time_used = end_time - start_time
print("Finish Generating Code:", time_used)
