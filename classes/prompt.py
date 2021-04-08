import discord

class Prompt:
    #bot            : A discord bot
    #guildId        : An int containing the id of the guilds  
    #descriptions   : A list of descriptions in the order you want them to appear in
    #functions      : A list of functions ordered in the same order of emojis
    #emojisLists    : A list of emojis in the order you want them to appear
    #promptType     : A string containing the type of the prompt
    #promptStage    : An int containing the number of the prompt 
    #channel        : The channel to send the 
    #message        : The message with the prompt
    def __init__(self, bot, guildId, descriptions, functions, emojisLists, promptType, channel, 
      timer=None, promptStage=0, message=None):

      self.bot = bot
      self.guildId = guildId    
      self.descriptions = descriptions
      self.functions = functions
      self.emojisLists = emojisLists
      self.promptType = promptType
      self.channel = channel
      self.timer = timer
      self.promptStage = promptStage
      self.message = message

    async def showPrompt(self):
      #We set the embed for the questions related to the blindtest mode
      embed = discord.Embed()
  
      embed.set_author(name=self.bot.user.name)
      embed.add_field(name="Choix 1", value=self.descriptions[self.promptStage], inline=False)
      
      self.message = await self.channel.send(embed=embed)

      #Then we react to the message by looping through every emojis
      for emoji in self.emojisLists[self.promptStage]:
        await self.message.add_reaction(emoji)
    
    #reaction : The emoji as a string representing the name
    async def checkReactionValidity(self, reaction):
      isValid = False

      if (reaction in self.emojisLists[self.promptStage]):
        isValid = True
      
      return isValid

    #Use the correct function
    async def useFunction(self):
      #If there's no function to run
      if (self.functions[self.promptStage] == None):
        #Check if it's the end of the prompt chain, if yes, cancel everything and delete ourselves
        #(This condition, is not supposed to be possible however)
        #------------------------------------------REPRENDRE ICI------------------------------------------
        if (self.promptStage == len(self.functions) - 1):
          print("WTF")
          await self.selfDestruct()
    
    #Pretty self explanatory it destroy the self instance of prompt
    async def selfDestruct(self):
      if (self.guildId in self.bot.ongoingBlindtestPrompts and self == self.bot.ongoingBlindtestPrompts[self.guildId]["prompt"]):
        print("Hello !")