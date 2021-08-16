import discord

class Prompt:
    #bot            : A discord bot
    #guildId        : An string containing the id of the guilds  
    #descriptions   : A list of descriptions in the order you want them to appear in
    #emojisLists    : A list of emojis in the order you want them to appear
    #promptType     : A string containing the type of the prompt
    #promptStage    : An int containing the number of the prompt 
    #channel        : A string reprensentin the channel to send the message
    #functions      : A tuple containing in order, the functions to use
    #message        : The message with the prompt
    def __init__(self, bot, guildId, descriptions, emojisLists, promptType, channel, functions, 
        promptStage=0, message=None, lastChoice=None):

        self.bot = bot
        self.guildId = guildId    
        self.descriptions = descriptions
        self.emojisLists = emojisLists
        self.promptType = promptType
        self.channel = channel
        self.promptStage = promptStage
        self.message = message
        self.lastChoice = lastChoice

    async def showPrompt(self):
        #We set the embed for the questions related to the blindtest mode
        embed = discord.Embed()

        embed.set_author(name=self.bot.user.name)
        embed.add_field(name="Choix 1", value=self.descriptions[self.promptStage], inline=False)
        
        self.message = await self.channel.send(embed=embed)

        #Then we react to the message by looping through every emojis
        for emoji in self.emojisLists[self.promptStage]:
            await self.message.add_reaction(emoji)

        #Return the messsage
        return self.message
        
    #reaction : The emoji as a string representing the name
    async def checkReactionValidity(self, reaction):
      isValid = False

      if (reaction in self.emojisLists[self.promptStage]):
        isValid = True
      
      return isValid
