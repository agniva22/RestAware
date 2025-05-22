import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline

model_name = "tiiuae/falcon-7b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

generator = TextGenerationPipeline(model=model, tokenizer=tokenizer)

def movement_description(avg):
    if avg < 1:
        return "very little movement, indicating deep rest"
    elif avg < 3:
        return "moderate movement, suggesting relatively stable sleep"
    else:
        return "high movement activity, which may indicate restlessness during sleep"

def prepare_prompt(data, person_id):
    data['Movement_Value'] = pd.to_numeric(data['Movement_Value'], errors='coerce')
    movement_avg = data['Movement_Value'].mean()

    deep_sleep = (data['Status'] == 'Deep Sleep').sum()
    prone_posture = (data['Posture'] == 'Prone').sum()
    low_breathing = (data['Status'] == 'Low Breathing').sum()
    no_move = (data['Status'] == 'No Move').sum()

    movement_phrase = movement_description(movement_avg)

    prompt = (
        f"Sleep summary for {person_id}: "
        f"{deep_sleep} instances of deep sleep, {prone_posture} instances of prone posture, "
        f"{movement_phrase}, "
        f"{low_breathing} 'Low Breathing' events, and {no_move} 'No Move' events. "
        f"Generate a paragraph summarizing this person sleep pattern."
    )
    return prompt

df_path = "./decoded_sleep_data.csv"
df = pd.read_csv(df_path)

results = []

for name in df['Name'].unique():
    person_data = df[df['Name'] == name].copy()
    prompt = prepare_prompt(person_data, name)

    try:
        output = generator(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)[0]['generated_text']
        summary = output.replace(prompt, '').strip()
    except Exception as e:
        summary = f"Error: {e}"

    print(f"\n--- Summary for {name} ---\n{summary}\n")

    results.append({
        'Name': name,
        'Prompt': prompt,
        'Generated_Summary': summary
    })

pd.DataFrame(results).to_csv("generated_summaries_falcon.csv", index=False)
print("\n All summaries saved to 'generated_summaries_falcon.csv'")
