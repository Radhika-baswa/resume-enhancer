# suggestions.py
def suggest_action_verbs(text):
    suggestions = {}
    weak_verbs = {
        "worked": "executed",
        "helped": "assisted",
        "made": "developed",
        "created": "engineered",
        "used": "leveraged",
        "fixed": "resolved",
        "ran": "managed",
        "wrote": "authored"
    }
    for weak, strong in weak_verbs.items():
        if f" {weak} " in text.lower():
            suggestions[weak] = strong
    return suggestions



from transformers import pipeline

# Load HuggingFace model once
rephrase_pipeline = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def generate_impact_rewrite(line):
    # Avoid short or generic lines
    if len(line.split()) < 4:
        return "Consider expanding this point with impact or tools."

    try:
        # Rephrase using HuggingFace T5 model
        result = rephrase_pipeline(f"paraphrase: {line}", max_length=50, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Rewrite error: {str(e)}"

def generate_impactful_bullet_points(lines):
    seen = set()
    impactful_lines = []
    for line in lines:
        rewritten_line = generate_impact_rewrite(line)
        if rewritten_line not in seen:
            impactful_lines.append(rewritten_line)
            seen.add(rewritten_line)
    return impactful_lines
