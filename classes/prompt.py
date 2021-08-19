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
    #ongoing        : A boolean representing whether or not we're currently running a function (This blocks additional reactions while processing)
    def __init__(self, bot, guildId, descriptions, emojisLists, promptType, channel, functions, 
        promptStage=0, message=None, isOngoing=False):

        self.bot = bot
        self.guildId = guildId    
        self.descriptions = descriptions
        self.emojisLists = emojisLists
        self.promptType = promptType
        self.channel = channel
        self.functions = functions
        self.promptStage = promptStage
        self.message = message
        self.isOngoing = isOngoing

    async def showPrompt(self):
        #We set the embed for the questions related to the blindtest mode
        embed = discord.Embed()

        embed.set_author(name=self.bot.user.name)
        embed.add_field(name="Choix", value=self.descriptions[self.promptStage], inline=False)
        
        self.message = await self.channel.send(embed=embed)

        #Then we react to the message by looping through every emojis
        for emoji in self.emojisLists[self.promptStage]:
            await self.message.add_reaction(emoji)

        return self.message
    
    #Check if the reaction is in the emojis list for this prompt stage
    async def checkReactionValidity(self, emoji):
        isValid = False
        
        if (str(emoji) in self.emojisLists[self.promptStage]):
            isValid = True
        
        return isValid

    #emoji : The emoji reaction that has been added to the prompt message
    async def runFunction(self, emoji):
        await self.functions[self.promptStage](self, emoji)
            

