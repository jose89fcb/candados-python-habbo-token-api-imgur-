import urllib
import json
import requests
import discord
from discord.ext import commands
import datetime
import io
 
from urllib import parse, request
from PIL import Image, ImageDraw, ImageFont, ImageFile
import time

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext
import base64


with open("configuracion.json") as f:
    config = json.load(f)
    headers = {'Authorization': 'Bearer ' + config["token_imgur"],}

bot = commands.Bot(command_prefix='!', description="ayuda bot") #Comando
bot.remove_command("help") # Borra el comando por defecto !help

slash = SlashCommand(bot, sync_commands=True)
@slash.slash(
    name="caja", description="Keko habbo Hotel",
    options=[
                create_option(
                  name="keko",
                  description="Escribe el keko",
                  option_type=3,
                  required=True
                ),
               
    
                  create_option(
                  name="fondos",
                  description="Elige él fondo",
                  option_type=3,
                  required=True,
                  choices=[
                      create_choice(
                          name="Fondo Nieve",
                          value="FondoNieve"
                         
                      ),
                      create_choice(
                          name="Fondo Palmera",
                          value="FondoPalmeras"
                          
                      ),
                      create_choice(
                          name="Fondo Rosas",
                          value="FondoRosas"
                         
                      ),
                     
                      
                    
                  ],
                  
                
               
                  
                
                  
                  
                
               
                  
                ),
                create_option(
                  name="hotel",
                  description="Elige él hotel",
                  option_type=3,
                  required=True,
                  choices=[
                      create_choice(
                          name="ES - Hotel España",
                          value="es"
                      ),
                      create_choice(
                          name="BR - Hotel Brasil",
                          value="com.br"
                      ),
                      create_choice(
                          name="COM - Hotel Estados unidos",
                          value="com"
                      ),
                      create_choice(
                          name="DE - Hotel Aleman",
                          value="de"
                      ),
                      create_choice(
                          name="FR - Hotel Frances",
                          value="fr"
                      ),
                      create_choice(
                          name="FI - Hotel Finalandia",
                          value="fi"
                      ),
                      create_choice(
                          name="IT - Hotel Italiano",
                          value="it"
                      ),
                      create_choice(
                          name="TR - Hotel Turquia",
                          value="com.tr"
                      ),
                      create_choice(
                          name="NL - Hotel Holandés",
                          value="nl"
                      )
                  ]
                
               
                  
                )
             ])

                  
                
               
                 
            


async def _caja(ctx:SlashContext, keko, hotel, fondos):
    await ctx.defer()
    
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko}")
  
   
    try:

     habbo = response.json()['figureString']
     
    except KeyError:
        await ctx.send("El keko no existe!") 
   

   
    ##
    # programado Por jose89fcb
    ###

    
    
   
    try:

     url = "https://www.habbo.com/habbo-imaging/avatarimage?size=m&figure="+ habbo +"&action=none&direction=4&head_direction=4&gesture=std&size=m"
     img1 = Image.open(io.BytesIO(requests.get(url).content))
     img1 = img1.resize((64,110), Image.ANTIALIAS)#tamaño del keko 1

  
    
    


    
    


    

   

    

    
    
    



     img2 = img1.copy()
    
    
    ###

    


     cristalDerecho = Image.open(r"imagenes/cristalDerecho.png").convert("RGBA") #imagen
     img1 = cristalDerecho.resize((138,295), Image.ANTIALIAS)#tamaño de la cristalDerecho

     cristalizquierdo = Image.open(r"imagenes/cristalizquierdo.png").convert("RGBA") #imagen
     img1 = cristalizquierdo.resize((138,295), Image.ANTIALIAS)#tamaño de la cristalizquierdo


    ###
  
    ###
     almo = Image.open(r"imagenes/caja.png").convert("RGBA") #imagen
     img1 = almo.resize((138,295), Image.ANTIALIAS)#tamaño de la caja

    ###
     fondos = Image.open(r"imagenes/" +fondos+".png").convert("RGBA") #imagen
     img1 = fondos.resize((138,295), Image.ANTIALIAS)#tamaño de los fondos

    
    

 
   
    
    
    
     
     img1.paste(fondos,(0,0), mask = fondos) #Posicion de FondoNieve.png
    
     img1.paste(img2,(35,90), mask = img2) #Posicion del keko 1
     img1.paste(almo,(0,0), mask = almo) #Posicion de la caja
    
   
     
     img1.paste(cristalDerecho,(0,0), mask = cristalDerecho) #cristalDerecho

     img1.paste(cristalizquierdo,(0,0), mask = cristalizquierdo) #cristalizquierdo
     
    
     
  

    
    ### 

    
    
   
    
   ###
   
    
   
    ###
    
   
 
    
    
  ####
   
  ###
    




    

    
    
    
   
    
   
       


      
    
       
      

      
    
       
            
        
        
        
       
        
     with io.BytesIO() as image_binary:
        img1.save(image_binary, 'PNG')
        image_binary.seek(0)

        img_base64 = base64.b64encode(image_binary.read()).decode('utf-8')


        params = {
                'title': f'Imagen subida por {ctx.author.display_name} Servidor de discord {ctx.guild.name}',
                'description': f'Podras generar tú keko de Habbo Hotel en el servidor de discord {ctx.guild.name}',
                'name': 'Habbo Hotel',
                'image': img_base64,
            }

        r = requests.post(f'https://api.imgur.com/3/image', headers=headers, data=params)
        data = r.json()["data"]["link"]
        id = r.json()["data"]["id"]
        borrar = r.json()["data"]["deletehash"]

        embed = discord.Embed(title="Habbo Hotel", url="https://twitter.com/jose89fcb", description=f"[Descargar Skin](https://imgur.com/{id}.png)", color=discord.Colour.random())
        embed.set_footer(text=f"BOT Programado Por Jose89fcb")

        image_data = io.BytesIO(base64.b64decode(img_base64))
        image_file = discord.File(image_data, filename=f'keko.png')
        embed.set_image(url=f"attachment://keko.png")

        await ctx.send(embed=embed, file=image_file)

        embed = discord.Embed(title="Este mensaje solo lo podrás ver tú",
                                  description=f"Hola, {ctx.author.mention}\n\n\n\nEste es tú código: **{borrar}** para el usuario de Habbo **{keko}** por si quieres borrar la imagen con el comando /borrar + código\n\n**Aviso:** Esto sólo podrás borrar la imagen alojada en imgur.com él código lo podrás ver tú solo (NO LO COMPARTAS CON NADIE)",
                                  color=discord.Colour.random())

        await ctx.send(
                f"Link directo:\n```{data}```\nBBCode(Para foros):\n```[img]{data}[/img]```\nCódigo html: ```<a href='{data}'><img src='{data}' title='{keko}' /></a>``` \nID:```{id}```", hidden=True, embed=embed)

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")
        await ctx.message.add_reaction("💩")
        await ctx.message.add_reaction("😍")

        try:
                embed = discord.Embed(title=f"Código para {keko}")
                embed.add_field(name=f"👇👇👇👇",
                                value=f"Este es tú código **{borrar}** para poder borrar la imagen de **{keko}**",
                                inline=False)

                await ctx.author.send(embed=embed)
                await ctx.author.send(f"\n\n{borrar}")

                await ctx.send("Te acabo de enviar un mensaje privado", hidden=True)

        except discord.errors.Forbidden:
                await ctx.send(
                    "No pudimos enviarte el mensaje privado, => click en ajustes de usuario => privacidad y seguridad => permitir mensajes directos...\n\nNo te preocupes, el mensaje privado solo guarda el código qué te he mendado más arriba y poder borrar la imagen, por si lo pierdes al cerrar discord",
                    hidden=True)

    except FileNotFoundError:
        error_message = f"Error: La skin '{keko}' no existe."
        await ctx.send(error_message)
    except UnboundLocalError:
        habbo=":("

       
        
        
        

@slash.slash(
    name="borrar", description="Escribe La id para borrar la iamgen",
    options=[
                create_option(
                  name="borrar_imagen",
                  description="Escribe el ID para borrar la imagen",
                  option_type=3,
                  required=True
                ),
                 
    ])
                  
            
             

    


async def borrar(ctx:SlashContext, borrar_imagen:str):
    
    

    url = f"https://api.imgur.com/3/image/{borrar_imagen}"
    if len(borrar_imagen)  !=15:
        await ctx.send("Sólo está permitido 15 digitos")
        return
    
    payload={}
    files={}
    
   
    response = requests.request("DELETE", url, headers=headers, data=payload, files=files)

    embed=discord.Embed(title="", description="Imagen borrada con exito!", color=0x00ff11)
    if response.status_code ==200:
            await ctx.send(embed=embed, hidden=True)

    embed=discord.Embed(title="", description="No está permitido paginas webs", color=0xff0019)        
    if response.status_code ==400:
        await ctx.send(embed=embed, hidden=True)  

    embed=discord.Embed(title="", description="Error!", color=0xff0019)   
    if response.status_code ==403:
        await ctx.send(embed=embed, hidden=True) 



    embed=discord.Embed(title="", description="formato imagen no está permitido", color=0xff0019)   
    if response.status_code ==405:
         await ctx.send(embed=embed, hidden=True)


@bot.event
async def on_ready():
    print("BOT listo!")
    
bot.run(config["tokendiscord"])   