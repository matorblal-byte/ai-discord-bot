import time
import discord
import random
import os
import asyncio
import torch
from llama_cpp import Llama
global a
a = False
# Set this to the GGUF file you downloaded
model_path = r"C:\models\mistral-7b-instruct-v0.1.Q4_K_M.gguf\mistral-7b-instruct-v0.1.Q2_K.gguf"



llm = Llama(
    model_path=model_path,
    n_gpu_layers=24,      
    n_ctx=2048,           
    n_threads=4,         
    f16_kv=True          
)

async def call_local_mistral(prompt):
    """Generates a response using the GGUF model."""
    # When you're talking about the prompt said in the command as "whar my friend said"
    character_prompt = "" # This will tell your ai to be a character with a prompt - example: You are now Brody: lowercase loyalist brody brings unapologetic honesty to the table, unafraid to speak his mind, even if it means ruffling feathers. with a tendency to be brutally blunt, he's often misunderstood as rude or toxic. prone to outbursts, but working on his anger issues, brody's conversations are peppered with quirky phrases like "skibidi" and "sigma" - and don't even get him started on "liberals". if you're looking for a straight shooter who keeps it real, brody's your guy, just don't expect sugarcoating - skibidi toilet vibes guaranteed.
    full_prompt = f"[INST] This is the character i want you to be: \"{character_prompt}\" Respond as them with what my friend said, and do NOT give your internal thoughts, just respond directly to the message ***as the character***, and do not include quotes, you ARE the character. Ok, heres the message: ` \"{prompt}\" [/INST]"
    loop = asyncio.get_event_loop()
    try:
        output = await loop.run_in_executor(None, lambda: llm(
            full_prompt,
            max_tokens=150, # Change to how long youd like the message to be (in characters)(the message does not have to return thew exact length you set but if a response is more than this amount then it ends abruptly)
            stop=["</s>"]
        ))
        return output['choices'][0]['text'].strip()
    except Exception as e:
        return f"Model Error: {e}"
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content.startswith('$ai '):
               global a
               if a == True: # this code is for more than responding at more than 1 prompt at a time, i dont know if you can respond at multiple prompts at a time but my python crashes if i try to
                await message.channel.send('Im doing another prompt rn wait for ur turm')
                return
               prompt = message.content[len('$ai '):].strip()
               if not prompt:
                    await message.channel.send('Please provide a prompt: !asklocal <prompt>')
                    return
               try:
                    a = True
                    async with message.channel.typing():
                         response = await call_local_mistral(prompt)
                         await message.channel.send(response)
                         a = False
               except Exception as e:
                    await message.channel.send(f'Generation failed: {e}')
                    a = False
 
intents = discord.Intents.default() 
intents.message_content = True
client = MyClient(intents=intents)
client.run("TOKEN")       # replace wih your token                
