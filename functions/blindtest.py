async def blindtestChannelChoiceFunc(prompt=None, emoji=None):
    #If the user chose to accept
    try:
        #If the user accepted to choose the current channel for future blindtest, we register this in the database
        #and prompt the user to reuse the blindtest command
        if str(emoji) == prompt.bot.emojisDict["whiteCheckMark"]:
            await prompt.channel.send(f"```{prompt.bot.prompts['blindtestChoiceAcceptProposition']}```")
        #Else, we prompt him to register the wanted blindtest channel by using another command
        else:
            return
        #Then we delete everything related to this prompt in the bot stored variable
    except Exception as e:
        print(e)
        prompt.isOngoing = False
        return
    

