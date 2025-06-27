# bullet_rewriter.py

from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch

# Model for bullet point paraphrasing
model_name = "tuner007/pegasus_paraphrase"

tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def rephrase_bullet_point(text):
    if not text.strip():
        return ""

    input_text = f"paraphrase: {text} </s>"

    # Tokenize input
    batch = tokenizer(
        [input_text],
        truncation=True,
        padding="longest",
        return_tensors="pt"
    )

    # Generate paraphrase
    with torch.no_grad():
        outputs = model.generate(
            **batch,
            max_length=60,
            num_beams=5,
            num_return_sequences=1,
            temperature=1.5,
            early_stopping=True
        )

    # Decode and return paraphrased bullet point
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
