# bot.py
import os
import discord
from dotenv import load_dotenv
import ride_the_bus_game as rb

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    client.isPlaying = {}
    client.player = {}
    client.isPlaying = {}
    client.hasWon = {}
    client.game = {}

    for g in client.guilds:
        print(
            f'{client.user} is connected to the following guilds:\n'
            f'{g.name}(id: {g.id})'
        )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("~ride"):
        if client.isPlaying.get(message.guild.id):
            await message.channel.send(f"Already a game in progress (started by {client.player.get(message.guild.id)})!")
        else:
            # enter game loop
            client.isPlaying[message.guild.id] = True
            client.player[message.guild.id] = message.author
            client.game[message.guild.id] = rb.ride_the_bus_game()
            client.hasWon[message.guild.id] = False

            await message.channel.send(f"Its time to play {client.player[message.guild.id]}")

            # options
            reactions = ["🔴", "⚫", "♦️",
                         "♠️", "♣️", "❤️",
                         "⬆️", "⬇️", "📥", "📤", "💈"]

            def check(reaction, user):
                # need to have the available options
                return user == client.player[message.guild.id] and reaction.emoji in reactions

            while client.isPlaying[message.guild.id]:
                # black or red phase
                card = client.game[message.guild.id].draw_card()
                client.game[message.guild.id].table.append(card)
                msg = await message.channel.send(f"Black or red")

                await msg.add_reaction("⚫")
                await msg.add_reaction("🔴")

                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying[message.guild.id]:
                        f = open(card.image_path, "rb")
                        df = discord.File(f)
                        await message.channel.send("", file=df)
                        f.close()
                        if client.game[message.guild.id].black_or_red(reaction.emoji == "🔴"):
                            pass
                        else:
                            await message.channel.send("***🍻🍻 Drink 🍻🍻***")
                            continue
                except Exception as e:
                    print(e)
                    if client.isPlaying[message.guild.id]:
                        client.isPlaying[message.guild.id] = False
                        await message.channel.send("Too slow game ended!")
                        break

                # higher or lower
                card = client.game[message.guild.id].draw_card()

                client.game[message.guild.id].table.append(card)
                msg = await message.channel.send(f"Higher or lower")

                await msg.add_reaction("⬆️")
                await msg.add_reaction("⬇️")

                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying[message.guild.id]:
                        f = open(card.image_path, "rb")
                        df = discord.File(f)
                        await message.channel.send("", file=df)
                        f.close()
                        if client.game[message.guild.id].higher_or_lower(reaction.emoji == "⬆️"):
                            pass
                        else:
                            await message.channel.send("***🍻🍻 Drink 🍻🍻***")
                            continue
                except:
                    if client.isPlaying[message.guild.id]:
                        client.isPlaying[message.guild.id] = False
                        await message.channel.send("Too slow game ended!")
                        break

                # in between or outside
                card = client.game[message.guild.id].draw_card()

                client.game[message.guild.id].table.append(card)
                msg = await message.channel.send(f"In between or outside (or posts)")

                await msg.add_reaction("📥")
                await msg.add_reaction("📤")
                await msg.add_reaction("💈")

                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying[message.guild.id]:
                        f = open(card.image_path, "rb")
                        df = discord.File(f)
                        await message.channel.send("", file=df)
                        f.close()
                        if client.game[message.guild.id].inbetween_outside(0 if reaction.emoji == "📥" else 1 if reaction.emoji == "📤" else 2):
                            pass
                        else:
                            await message.channel.send("***🍻🍻 Drink 🍻🍻***")
                            continue
                except:
                    if client.isPlaying[message.guild.id]:
                        client.isPlaying[message.guild.id] = False
                        await message.channel.send("Too slow game ended!")
                        break

                # final layer
                card = client.game[message.guild.id].draw_card()

                client.game[message.guild.id].table.append(card)
                msg = await message.channel.send(f"Pick suit")

                await msg.add_reaction("♠️")
                await msg.add_reaction("❤️")
                await msg.add_reaction("♦️")
                await msg.add_reaction("♣️")
                valid = ["♠️", "❤️", "♦️", "♣️"]

                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                    # check make sure game still going
                    if client.isPlaying[message.guild.id]:
                        f = open(card.image_path, "rb")
                        df = discord.File(f)
                        await message.channel.send("", file=df)
                        f.close()
                        if client.game[message.guild.id].suit(valid.index(reaction.emoji)):
                            await message.channel.send(f"***🎊🎊 You win 🎊🎊***")
                            client.hasWon[message.guild.id] = True
                            client.isPlaying[message.guild.id] = False
                        else:
                            await message.channel.send("***🍻🍻 Drink 🍻🍻***")
                            continue
                except:
                    if client.isPlaying[message.guild.id]:
                        client.isPlaying[message.guild.id] = False
                        await message.channel.send("Too slow game ended!")
                        break
        if client.hasWon[message.guild.id]:
            await message.channel.send("Got off bus after " + str(client.game[message.guild.id].number_decks) + " decks and " + str(client.game[message.guild.id].trys) + " trys")

    elif client.isPlaying.get(message.guild.id) and message.author == client.player[message.guild.id] and message.content.startswith("~quit"):
        client.isPlaying[message.guild.id] = False
        await message.channel.send("He's done")
    elif message.content.startswith("~help"):
        await message.channel.send("TODO: help here")

client.run(TOKEN)
