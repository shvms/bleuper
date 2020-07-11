import json

def main():
  try:
    from nltk.translate.bleu_score import sentence_bleu
    
    with open("core.en.json") as file:
      core = json.load(file)
    
    with open("refs.en.json") as file:
      refs = json.load(file)
    
    with open("trans.en.json") as file:
      trans = json.load(file)
    
    with open("weights.json") as file:
      weights = json.load(file)
    
    
    
  except ModuleNotFoundError:
    raise ValueError("Requires NLTK==3.5+ to generate accurate tests.")
