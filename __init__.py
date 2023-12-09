# __init__.py

import torch
from diffusers import DiffusionPipeline, LCMScheduler

# AI 모델 초기화
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    variant="fp16",
    torch_dtype=torch.float16
).to("cuda")

# set scheduler
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

# load LCM-LoRA
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")


#for multiple user
pipe2 = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    variant="fp16",
    torch_dtype=torch.float16
).to("cuda:1")
pipe2.scheduler = LCMScheduler.from_config(pipe2.scheduler.config)
pipe2.load_lora_weights("latent-consistency/lcm-lora-sdxl")

pipe3 = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    variant="fp16",
    torch_dtype=torch.float16
).to("cuda:2")
pipe3.scheduler = LCMScheduler.from_config(pipe3.scheduler.config)
pipe3.load_lora_weights("latent-consistency/lcm-lora-sdxl")

pipe4 = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    variant="fp16",
    torch_dtype=torch.float16
).to("cuda:3")
pipe4.scheduler = LCMScheduler.from_config(pipe4.scheduler.config)
pipe4.load_lora_weights("latent-consistency/lcm-lora-sdxl")