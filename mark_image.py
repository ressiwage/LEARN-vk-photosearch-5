from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

processor = None
model = None

class Marker:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

    def process(self, fname):
        image = Image.open(fname)  
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_caption

if __name__ == '__main__':
    Marker().process()