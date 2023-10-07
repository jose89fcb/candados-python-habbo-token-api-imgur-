import json
import requests
import discord
from discord.ext import commands
import io
import time
from PIL import Image, ImageDraw, ImageFont, ImageFile
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
    name="kekoamor", description="keko habbo hotel",
    options=[
                create_option(
                  name="keko1",
                  description="Escribe el keko 1",
                  option_type=3,
                  required=True,
                ),
                create_option(
                  name="keko2",
                  description="Escribe el keko 2",
                  option_type=3,
                  required=True,
                  
                
                  
                ),create_option(
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


async def _kekoamor(ctx:SlashContext, keko1:str,keko2:str, hotel:str):
    await ctx.defer()
    
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko1}")
    response1 = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko2}")
    try:

     habbo1 = response.json()['figureString']
   

     habbo2 = response1.json()['figureString']
    except KeyError:
        await ctx.send("uno de los kekos no existen!")
   
   
    

    
    
   
    try:
     url = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo1 +"&direction=2&head_direction=2"
     img1 = Image.open(io.BytesIO(requests.get(url).content))
     img1 = img1.resize((64,110), Image.ANTIALIAS)#tamaño del keko 1
    
     url1 = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo2 +"&direction=4&head_direction=2"
     habbol = Image.open(io.BytesIO(requests.get(url1).content))
     habbol = habbol.resize((64,110), Image.ANTIALIAS)#tamaño del keko 2
    
    
     img2 = img1.copy()
    
    
    
     img1 = Image.open(r"candados/candadoamor.png").convert("RGBA") #Imagen del candado de amor sant valentin
     img1.paste(img2,(124,3), mask = img2) #Posicion del keko 1
    
    ###
    

     img1.paste(habbol,(190,3), mask = habbol) #Posicion del keko 2
    
  
     draw = ImageDraw.Draw(img1)
     font = ImageFont.truetype("fuentes/UbuntuRegular-latin.246ea4b3.otf", 13) #Tamaño de la fuente (textos)

     draw.text((110, 120), f"Hasta que los pixels nos separen", font=font, fill=(101,36,97))  #Texto y color
    
    
     fecha = time.strftime("%d/%m/%Y", time.gmtime()) #Fecha
     draw.text((170, 150), f"{fecha}", font=font, fill=(101,36,97))


     draw.text((150, 175), f"{keko1}         {keko2}", font=font, fill=(101,36,97)) #Nombres de los kekos
    
    
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
                                  description=f"Hola, {ctx.author.mention}\n\n\n\nEste es tú código: **{borrar}** para el usuario de Habbo **{keko1} - {keko2}** por si quieres borrar la imagen con el comando /borrar + código\n\n**Aviso:** Esto sólo podrás borrar la imagen alojada en imgur.com él código lo podrás ver tú solo (NO LO COMPARTAS CON NADIE)",
                                  color=discord.Colour.random())

        await ctx.send(
                f"Link directo:\n```{data}```\nBBCode(Para foros):\n```[img]{data}[/img]```\nCódigo html: ```<a href='{data}'><img src='{data}' title='{keko1} - {keko2}' /></a>``` \nID:```{id}```", hidden=True, embed=embed)

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")
        await ctx.message.add_reaction("💩")
        await ctx.message.add_reaction("😍")

        try:
                embed = discord.Embed(title=f"Código para {keko1}-{keko2}")
                embed.add_field(name=f"👇👇👇👇",
                                value=f"Este es tú código **{borrar}** para poder borrar la imagen de **{keko1} - {keko2}**",
                                inline=False)

                await ctx.author.send(embed=embed)
                await ctx.author.send(f"\n\n{borrar}")

                await ctx.send("Te acabo de enviar un mensaje privado", hidden=True)

        except discord.errors.Forbidden:
                await ctx.send(
                    "No pudimos enviarte el mensaje privado, => click en ajustes de usuario => privacidad y seguridad => permitir mensajes directos...\n\nNo te preocupes, el mensaje privado solo guarda el código qué te he mendado más arriba y poder borrar la imagen, por si lo pierdes al cerrar discord",
                    hidden=True)

    except FileNotFoundError:
        error_message = f"Error: La skin '{keko1} - {keko2}' no existe."
        await ctx.send(error_message)
    except UnboundLocalError:
        habbo=":("

       

@slash.slash(
    name="kekoween", description="keko habbo hotel",
    options=[
                create_option(
                  name="keko1",
                  description="Escribe el keko 1",
                  option_type=3,
                  required=True,
                ),
                create_option(
                  name="keko2",
                  description="Escribe el keko 2",
                  option_type=3,
                  required=True,
                  
                
                  
                ),create_option(
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


async def _kekoween(ctx:SlashContext, keko1:str,keko2:str, hotel:str):
    await ctx.defer()
    
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko1}")
    response1 = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko2}")
    
    try:

     habbo1 = response.json()['figureString']
    

    

     habbo2 = response1.json()['figureString']
    except KeyError:
        await ctx.send("uno de los kekos no existen!")
   
   
    

    
    
   
    try:
     url = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo1 +"&direction=2&head_direction=2"
     img1 = Image.open(io.BytesIO(requests.get(url).content))
     img1 = img1.resize((64,110), Image.ANTIALIAS)#tamaño del keko 1
    
     url1 = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo2 +"&direction=4&head_direction=2"
     habbol = Image.open(io.BytesIO(requests.get(url1).content))
     habbol = habbol.resize((64,110), Image.ANTIALIAS)#tamaño del keko 2
    
    
     img2 = img1.copy()
    
    
    
     img1 = Image.open(r"candados/candadoween.png").convert("RGBA") #Imagen del candado de amor sant valentin
     img1.paste(img2,(118,3), mask = img2) #Posicion del keko 1
    
    ###
    

     img1.paste(habbol,(186,3), mask = habbol) #Posicion del keko 2
    
  
     draw = ImageDraw.Draw(img1)
     font = ImageFont.truetype("fuentes/UbuntuRegular-latin.246ea4b3.otf", 13) #Tamaño de la fuente (textos)

     draw.text((85, 130), f"Amigos hasta que la luz se apague", font=font, fill=(77,54,76))  #Texto y color
    
    
     fecha = time.strftime("%d/%m/%Y", time.gmtime()) #Fecha
     draw.text((170, 150), f"{fecha}", font=font, fill=(77,54,76))


     draw.text((150, 175), f"{keko1}         {keko2}", font=font, fill=(101,24,96)) #Nombres de los kekos
    
    
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
                                  description=f"Hola, {ctx.author.mention}\n\n\n\nEste es tú código: **{borrar}** para el usuario de Habbo **{keko1} - {keko2}** por si quieres borrar la imagen con el comando /borrar + código\n\n**Aviso:** Esto sólo podrás borrar la imagen alojada en imgur.com él código lo podrás ver tú solo (NO LO COMPARTAS CON NADIE)",
                                  color=discord.Colour.random())

        await ctx.send(
                f"Link directo:\n```{data}```\nBBCode(Para foros):\n```[img]{data}[/img]```\nCódigo html: ```<a href='{data}'><img src='{data}' title='{keko1} - {keko2}' /></a>``` \nID:```{id}```", hidden=True, embed=embed)

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")
        await ctx.message.add_reaction("💩")
        await ctx.message.add_reaction("😍")

        try:
                embed = discord.Embed(title=f"Código para {keko1}-{keko2}")
                embed.add_field(name=f"👇👇👇👇",
                                value=f"Este es tú código **{borrar}** para poder borrar la imagen de **{keko1} - {keko2}**",
                                inline=False)

                await ctx.author.send(embed=embed)
                await ctx.author.send(f"\n\n{borrar}")

                await ctx.send("Te acabo de enviar un mensaje privado", hidden=True)

        except discord.errors.Forbidden:
                await ctx.send(
                    "No pudimos enviarte el mensaje privado, => click en ajustes de usuario => privacidad y seguridad => permitir mensajes directos...\n\nNo te preocupes, el mensaje privado solo guarda el código qué te he mendado más arriba y poder borrar la imagen, por si lo pierdes al cerrar discord",
                    hidden=True)

    except FileNotFoundError:
        error_message = f"Error: La skin '{keko1} - {keko2}' no existe."
        await ctx.send(error_message)
    except UnboundLocalError:
        habbo=":("



@slash.slash(
    name="sebusca", description="keko habbo hotel",
    options=[
                create_option(
                  name="keko1",
                  description="Escribe el keko 1",
                  option_type=3,
                  required=True,
                ),
                create_option(
                  name="keko2",
                  description="Escribe el keko 2",
                  option_type=3,
                  required=True,
                  
                
                  
                ),create_option(
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


async def _sebusca(ctx:SlashContext, keko1:str,keko2:str, hotel:str):
    await ctx.defer()
    
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko1}")
    response1 = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko2}")
    
    try:

     habbo1 = response.json()['figureString']
    

    

     habbo2 = response1.json()['figureString']
    except KeyError:
        await ctx.send("uno de los kekos no existen!")
   
   
    

    
    
   
    try:

     url = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo1 +"&direction=2&head_direction=2"
     img1 = Image.open(io.BytesIO(requests.get(url).content))
     img1 = img1.resize((64,110), Image.ANTIALIAS)#tamaño del keko 1
    
     url1 = "https://www.habbo.com/habbo-imaging/avatarimage?size=l&figure="+ habbo2 +"&direction=4&head_direction=2"
     habbol = Image.open(io.BytesIO(requests.get(url1).content))
     habbol = habbol.resize((64,110), Image.ANTIALIAS)#tamaño del keko 2
    
    
     img2 = img1.copy()
    
    
    
     img1 = Image.open(r"candados/candadosebusca.png").convert("RGBA") #Imagen del candado de amor sant valentin
     img1.paste(img2,(118,3), mask = img2) #Posicion del keko 1
    
    ###
    

     img1.paste(habbol,(186,3), mask = habbol) #Posicion del keko 2
    
  
     draw = ImageDraw.Draw(img1)
     font = ImageFont.truetype("fuentes/UbuntuRegular-latin.246ea4b3.otf", 13) #Tamaño de la fuente (textos)

     draw.text((110, 130), f"Compañeros del crimen", font=font, fill=(77,54,76))  #Texto y color
    
    
     fecha = time.strftime("%d/%m/%Y", time.gmtime()) #Fecha
     draw.text((168, 150), f"{fecha}", font=font, fill=(77,54,76))


 
     draw.text((150, 175), f"{keko1}     {keko2}", font=font, fill=(98,46,84)) #Nombres de los kekos
    
    
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
                                  description=f"Hola, {ctx.author.mention}\n\n\n\nEste es tú código: **{borrar}** para el usuario de Habbo **{keko1} - {keko2}** por si quieres borrar la imagen con el comando /borrar + código\n\n**Aviso:** Esto sólo podrás borrar la imagen alojada en imgur.com él código lo podrás ver tú solo (NO LO COMPARTAS CON NADIE)",
                                  color=discord.Colour.random())

        await ctx.send(
                f"Link directo:\n```{data}```\nBBCode(Para foros):\n```[img]{data}[/img]```\nCódigo html: ```<a href='{data}'><img src='{data}' title='{keko1} - {keko2}' /></a>``` \nID:```{id}```", hidden=True, embed=embed)

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")
        await ctx.message.add_reaction("💩")
        await ctx.message.add_reaction("😍")

        try:
                embed = discord.Embed(title=f"Código para {keko1}-{keko2}")
                embed.add_field(name=f"👇👇👇👇",
                                value=f"Este es tú código **{borrar}** para poder borrar la imagen de **{keko1} - {keko2}**",
                                inline=False)

                await ctx.author.send(embed=embed)
                await ctx.author.send(f"\n\n{borrar}")

                await ctx.send("Te acabo de enviar un mensaje privado", hidden=True)

        except discord.errors.Forbidden:
                await ctx.send(
                    "No pudimos enviarte el mensaje privado, => click en ajustes de usuario => privacidad y seguridad => permitir mensajes directos...\n\nNo te preocupes, el mensaje privado solo guarda el código qué te he mendado más arriba y poder borrar la imagen, por si lo pierdes al cerrar discord",
                    hidden=True)

    except FileNotFoundError:
        error_message = f"Error: La skin '{keko1} - {keko2}' no existe."
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
    
    headers = {
        'Authorization': "Bearer " +  config["token_imgur"]}
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