from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM, BlipProcessor, BlipForConditionalGeneration
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = None
model = None

class MarkerBase:
    def __init__(self):
        pass
    def process(self, fname):
        pass

class Marker(MarkerBase):
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco").to(device)


    def process(self, fname):
        image = Image.open(fname)  
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values.to(device)
        generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50).to(device)
        generated_caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_caption
    
class BlipMarker(MarkerBase):
    def __init__(self):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
        self.processor = processor
        self.model = model

    def process(self, fname):
        image = Image.open(fname)  
        inputs = self.processor(image, return_tensors="pt").to(device)
        out = self.model.generate(**inputs).to(device)
        return self.processor.decode(out[0], skip_special_tokens=True)

chosen_marker = BlipMarker()

if __name__ == '__main__':
    Marker().process()

