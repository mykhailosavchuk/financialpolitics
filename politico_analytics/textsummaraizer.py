from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

model_name = 'google/pegasus-xsum'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

src_text = [
    """this happened 5/6 years ago so my whole family every xmas day goes around to my aunties for celebrations. my cousin (of course) was there and he
asked if i wanted to play cops and robbers. i accepted of course. now, next to the side of my aunts house is a little area with a small fence, a covered
water tank and super duper sharp stones. my cousin (who was the cop) was gaining on me. i (tried) to jump over the fence, aaand i failed the jump
and went crashing onto the gravel, my leg hitting the sharpest bit and, then the next thing i knew it had a nasty gash."""
]


batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest',return_tensors='pt')
translated = model.generate(**batch)
tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
print(tgt_text)
