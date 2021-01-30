# bot.py
import os
import discord
from dotenv import load_dotenv
import ride_the_bus_game as rb

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    client.isPlaying = False
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("~ride"):
        if client.isPlaying:
            await message.channel.send(f"Already a game in progress (started by {client.player})!")
        else:
            # enter game loop
            client.isPlaying = True
            client.player = message.author
            client.game = rb.ride_the_bus_game()

            await message.channel.send(f"Its time to play {client.player}")

            # options
            reactions = ["🔴", "⚫", "♦️",
                         "♠️", "♣️", "❤️",
                         "⬆️", "⬇️", "📥", "📤", "💈"]

            def check(reaction, user):
                # need to have the available options
                return user == client.player and reaction.emoji in reactions

            while client.isPlaying:
                # black or red phase
                card = client.game.draw_card()

                client.game.table.append(card)
                msg = await message.channel.send(f"Black or red")

                await msg.add_reaction("⚫")
                await msg.add_reaction("🔴")

                try:
                    await message.channel.send("**** You have 60 seconds to react with your answer ****")
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying:
                        # f = discord.File(open(card.image_path))
                        # await message.channel.send("", file=f)
                        # f.close()
                        if client.game.black_or_red(reaction.emoji == "🔴"):
                            await message.channel.send(f"Good job")
                        else:
                            await message.channel.send("get fuked")
                            continue
                except:
                    client.isPlaying = False
                    await message.channel.send("Too slow game ended!")

                # higher or lower
                card = client.game.draw_card()

                client.game.table.append(card)
                msg = await message.channel.send(f"Higher or lower")

                await msg.add_reaction("⬆️")
                await msg.add_reaction("⬇️")

                try:
                    await message.channel.send("**** You have 60 seconds to react with your answer ****")
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying:
                        # f = discord.File(open(card.image_path))
                        # await message.channel.send("", file=f)
                        # f.close()
                        if client.game.higher_or_lower(reaction.emoji == "⬆️"):
                            await message.channel.send(f"Good job")
                        else:
                            await message.channel.send("get fuked")
                            continue
                except:
                    client.isPlaying = False
                    await message.channel.send("Too slow game ended!")

                # in between or outside
                card = client.game.draw_card()

                client.game.table.append(card)
                msg = await message.channel.send(f"In between or outside (or posts)")

                await msg.add_reaction("📥")
                await msg.add_reaction("📤")
                await msg.add_reaction("💈")

                try:
                    await message.channel.send("**** You have 60 seconds to react with your answer ****")
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying:
                        # f = discord.File(open(card.image_path))
                        # await message.channel.send("", file=f)
                        # f.close()
                        if client.game.inbetween_outside(0 if reaction.emoji == "📥" else 1 if reaction.emoji == "📤" else 2):
                            await message.channel.send(f"Good job")
                        else:
                            await message.channel.send("get fuked")
                            continue
                except:
                    client.isPlaying = False
                    await message.channel.send("Too slow game ended!")

                # final layer
                card = client.game.draw_card()

                client.game.table.append(card)
                msg = await message.channel.send(f"Pick suit")

                await msg.add_reaction("♠️")
                await msg.add_reaction("❤️")
                await msg.add_reaction("♦️")
                await msg.add_reaction("♣️")

                try:
                    await message.channel.send("**** You have 60 seconds to react with your answer ****")
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying:
                        # f = discord.File(open(card.image_path))
                        # await message.channel.send("", file=f)
                        # f.close()
                        if client.game.inbetween_outside(0 if reaction.emoji == "♠️" else 1 if reaction.emoji == "❤️" else 2 if reaction.emoji == "♦️" else 3):
                            await message.channel.send(f"You win")
                            client.isPlaying = False
                        else:
                            await message.channel.send("get fuked")
                            continue
                except:
                    client.isPlaying = False
                    await message.channel.send("Too slow game ended!")
        await message.channel.send("Got off bus after " + str(client.game.number_decks) + " decks and " + str(client.game.trys) + " trys")

    elif client.isPlaying and message.author == client.player and message.content.startswith("~quit"):
        client.isPlaying = False
        await message.channel.send("He's done")
    elif message.content.startswith("~help"):
        await message.channel.send("TODO: help here")

client.run(TOKEN)
