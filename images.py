from transformers import CLIPModel, CLIPProcessor
from diffusers import StableDiffusionPipeline

# Install required libraries if not already installed (assuming you have done this)
# pip install transformers timm

# Load the CLIP model and processor

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Define your text prompt for the tech concept
prompt = "A computer screen displaying a convolutional neural network architecture with labeled layers."

# Encode the text prompt
text_input = processor(prompt, return_tensors="pt")

# Load the Stable Diffusion pipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")



# Combine text prompt with CLIP encoding (optional for additional guidance)
generate_kwargs = {
    "prompt": prompt,
    "guidance_scale": 7.5,  # Adjust for balance between creativity and accuracy
    # "input_ids": text_input["input_ids"]  # Uncomment if using CLIP encoding
}
print("generated")

# Generate images using Stable Diffusion
images = pipe(**generate_kwargs)
print(images)
# Save or display the generated image (optional)

import numpy as np
import matplotlib.pyplot as plt

# Assuming you want to display the first image
first_image = images[0]

# Reshape to remove the batch dimension
first_image = np.squeeze(first_image)

plt.imshow(first_image)
plt.axis('off')  # Hide axes
plt.show()