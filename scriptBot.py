import discord
import pytesseract
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

tablo = [
  'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
]

@bot.event
async def on_ready():
  print('Connecté en tant que', bot.user.name)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  if message.content.startswith('!del'):
    channel = message.channel
    await message.channel.purge()

  if message.attachments:
    for attachment in message.attachments:
      if attachment.content_type.startswith('image/'):

        await attachment.save(attachment.filename)

        await message.delete()

        imagePath = attachment.filename

        fichier = open("horaires.txt", "w")
        fichier.write(pytesseract.image_to_string(imagePath))
        fichier.close()

        with open('horaires.txt', 'r') as fichier:
          lignes = fichier.readlines()

          for ligne in lignes:
            if '(du' in ligne:
              await message.channel.send(f'''
                /**************************************************/

                    {ligne}    
                
                /**************************************************/
              ''')

            if 'Eiras Cléo' in ligne or 'Eras Cléo' in ligne:
              jour = 0
              i = 0

              while i < len(ligne):
                if ligne[i] == 'R':
                  await message.channel.send(f'{tablo[jour]} : Repos')
                  jour += 1
                  i += 5
                elif ligne[i].isdigit():
                  heureD = int(ligne[i:i + 2])
                  minuteD = int(ligne[i + 3:i + 5])
                  heureF = int(ligne[i + 6:i + 8])
                  minuteF = int(ligne[i + 9:i + 11])
                  await message.channel.send(f'{tablo[jour]} : {heureD}:{minuteD} - {heureF}:{minuteF}')
                  jour += 1
                  i += 11
                else:
                  i += 1

              break

bot.run('')
