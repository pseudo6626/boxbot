import discord
import requests
import json
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from table2ascii import table2ascii as t2a, PresetStyle
from collections import deque
import random
from typing import List
import os
import aiohttp
import re
from bs4 import BeautifulSoup
from datetime import datetime,timedelta, timezone
from collections import Counter
from typing import Optional
import discord
from discord.ext import menus
from discord import ui, Interaction, Embed
from math import ceil
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
import urllib.parse
from urllib.parse import quote
from collections import defaultdict
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ui import Select
from readability import Document

BACKGROUND_CHANGE_FEATURE_SWITCH=False
DYNAMIC_WING_COMS_SWITCH=False
SUBSCRIBERS_FILE = "ferry_subscribers.json"
FERRY_FILE = "ferries.json"
DATA_FILE = "hauler_data.json"
GIPHY_API_KEY = "ENTER YOUR API KEY HERE OR BE SMART AND USE AN ENV"
GIPHY_SEARCH_TERM = "go go go"
PARTICIPANT_FILE = "yardsale-participants.json"
ADMIN_ROLE=9999999999999999999999999999999999999999
ORIGIN_SYS="insert system name of system at ceter of cluster"
WASTE_RADIUS=50
DEPARTURE_MESSAGE_ID = 999999999999999999  # The id of a message for boxbot to edit with up to date ferry info
DEPARTURE_CHANNEL_ID = 1365123748344369203   # Replace with the channel ID containing the message
TEMPLATE_CHANNEL_ID=1366877008164032512 #channel ID for a template voice channel for wing voice channels
GUILD_ID_NUM =9999999999999999999999999999  # Replace with your actual guild ID
GUILD_ID = discord.Object(id=GUILD_ID_NUM) 
BOT_SECRET="put your discord bot token here or be smart and use an env" 
PAGE_SIZE = 10
departures=[]
catchTrackerOut=[]
catchTrackerIn=[]
catchThresh=5
ships=[]
calls = deque()
as_cargo_lock = asyncio.Lock()


ONION_VARIETIES = [
    "Yellow", "Red", "White", "Sweet", "Vidalia",
    "WallaWalla", "TexasSweet", "Maui", "Bermuda", "Cipollini",
    "Shallot", "Chive", "Leek", "Green", "Scallion",
    "Spring", "Spanish", "CrystalWax", "EgyptianWalking", "Pearl"
]
COMMODITY_NAME_LOOKUP = {
    "Liquid Oxygen": "liquidoxygen",
    "Pesticides": "pesticides",
    "Surface Stabilisers": "surfacestabilisers",
    "Water": "water",
    "Evacuation Shelter": "evacuationshelter",
    "Survival Equipment": "survivalequipment",
    "Beer": "beer",
    "Liquor": "liquor",
    "Wine": "wine",
    "Animal Meat": "animalmeat",
    "Coffee": "coffee",
    "Fish": "fish",
    "Food Cartridges": "foodcartridges",
    "Fruit and Vegetables": "fruitandvegetables",
    "Grain": "grain",
    "Tea": "tea",
    "Ceramic Composites": "ceramiccomposites",
    "CMM Composite": "cmmcomposite",
    "Insulating Membrane": "insulatingmembrane",
    "Polymers": "polymers",
    "Semiconductors": "semiconductors",
    "Superconductors": "superconductors",
    "Building Fabricators": "buildingfabricators",
    "Crop Harvesters": "cropharvesters",
    "Emergency Power Cells": "emergencypowercells",
    "Geological Equipment": "geologicalequipment",
    "Microbial Furnaces": "heliostaticfurnaces",
    "Mineral Extractors": "mineralextractors",
    "Power Generators": "powergenerators",
    "Thermal Cooling Units": "thermalcoolingunits",
    "Water Purifiers": "waterpurifiers",
    "Agri-Medicines": "agriculturalmedicines",
    "Basic Medicines": "basicmedicines",
    "Combat Stabilizers": "combatstabilisers",
    "Aluminium": "aluminium",
    "Copper": "copper",
    "Steel": "steel",
    "Titanium": "titanium",
    "Advanced Catalysers": "advancedcatalysers",
    "Bioreducing Lichen": "bioreducinglichen",
    "Computer Components": "computercomponents",
    "H.E. Suits": "hazardousenvironmentsuits",
    "Land Enrichment Systems": "terrainenrichmentsystems",
    "Medical Diagnostic Equipment": "medicaldiagnosticequipment",
    "Micro Controllers": "microcontrollers",
    "Muon Imager": "mutomimager",
    "Resonating Separators": "resonatingseparators",
    "Robotics": "robotics",
    "Structural Regulators": "structuralregulators",
    "Military Grade Fabrics": "militarygradefabrics",
    "Biowaste": "biowaste",
    "Battle Weapons": "battleweapons",
    "Non-Lethal Weapons": "nonlethalweapons",
    "Reactive Armour": "reactivearmour"
}

box_facts = [
    "The first cardboard box was invented in China over 1,500 years ago.",
    "Cardboard boxes were first used for packaging in the early 19th century.",
    "The record for the largest cardboard box ever made is over 3,000 cubic feet.",
    "Amazon ships over 1.6 million boxes per day.",
    "Corrugated cardboard was patented in 1856 for hat lining before being used for boxes.",
    "Cardboard can be recycled up to seven times before its fibers break down too much.",
    "There is a world record for the fastest time to assemble 10 cardboard boxes.",
    "Some people collect vintage wooden and metal boxes as a hobby.",
    "Cats are instinctively attracted to boxes because they provide safety and warmth.",
    "Many board games were originally sold in wooden boxes before switching to cardboard.",
    "The term 'thinking outside the box' originates from a puzzle requiring lines outside a square.",
    "A 'Jack-in-the-box' toy was first mentioned in history as early as the 16th century.",
    "NASA has used specialized boxes to store moon rocks since the Apollo missions.",
    "Shipping boxes can have hidden tracking codes to help prevent theft.",
    "Corrugated cardboard was inspired by pleated fabric used in Victorian fashion.",
    "There are reusable plastic shipping boxes designed to replace single-use cardboard boxes.",
    "Some boxes are designed to be edible, particularly for emergency food rations.",
    "Bubble wrap was originally meant to be used as textured wallpaper before being used in packaging.",
    "Pizza boxes were invented in the 1960s and have remained largely unchanged since.",
    "A cube-shaped box is structurally one of the strongest geometric shapes.",
    "Wooden crates were historically used to transport gold and other valuable goods.",
    "Cardboard box forts are a favorite DIY play activity for children worldwide.",
    "Some artists use cardboard boxes as their primary medium for sculptures.",
    "Shipping container homes are essentially large metal boxes converted into livable spaces.",
    "In Japan, bento boxes are carefully arranged meals served in compartmentalized containers.",
    "Some subscription boxes deliver mystery items to customers each month.",
    "The black box in airplanes is actually orange to be more easily found after crashes.",
    "Many luxury brands use custom-made boxes to enhance their packaging appeal.",
    "There is a Guinness World Record for the tallest tower built using only cardboard boxes.",
    "The cardboard box is considered one of the most important inventions for modern logistics.",
    "Some musicians have turned wooden shipping crates into playable instruments.",
    "Cereal boxes were designed to stand upright on store shelves to catch consumer attention.",
    "Box-making is a key industry in global trade and commerce.",
    "Famous magician Harry Houdini used trick boxes in his escape acts.",
    "Corrugated cardboard absorbs shocks, making it ideal for fragile item shipping.",
    "The United States alone recycles billions of cardboard boxes annually.",
    "Origami artists have created intricate box designs using a single sheet of paper.",
    "Some moving companies rent plastic boxes instead of using disposable cardboard boxes.",
    "Boxes are essential in disaster relief efforts to transport emergency supplies.",
    "Treasure chests in pirate lore were actually more like wooden crates, not fancy boxes.",
    "The term 'Pandora's Box' originates from Greek mythology and refers to unleashing troubles.",
    "In gaming, loot boxes contain randomized rewards and are a controversial mechanic.",
    "Box kites were an innovation in aviation research before airplanes were developed.",
    "Mail-order catalogs in the 1900s relied heavily on boxes for shipping goods to customers.",
    "Some luxury watches come in boxes more expensive than the watches themselves.",
    "Giant gift boxes are often used for surprise reveals in marketing campaigns.",
    "In some cultures, special decorative boxes are used to store sacred items.",
    "Folding a box correctly can impact its durability and strength in shipping.",
    "Modern e-commerce companies spend millions optimizing box designs for efficiency.",
    "There are self-heating food boxes used for military rations and camping meals.",
    "The phrase 'boxed in' means feeling trapped, derived from being stuck in a confined space."
]

intents = discord.Intents.default()
intents.message_content= True
intents.members=True
intents.guilds = True  # Enable guild intents
intents.messages = True
intents.guild_messages = True
client = discord.Client(intents=intents)

   
# Helper to format time difference as human-readable
def strfdelta(delta: timedelta):
    rd = relativedelta(seconds=delta.total_seconds())
    parts = []
    if rd.days > 0:
        parts.append(f"{rd.days}d")
    if rd.hours > 0:
        parts.append(f"{rd.hours}h")
    if rd.minutes > 0:
        parts.append(f"{rd.minutes}m")
    if not parts:
        parts.append("just now")
    return " ".join(parts)

# Paginator View
class MarketPageView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=180)
        self.pages = pages
        self.page = 0

    async def update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content=f"🛒 **Local Market Update Times** (Page {self.page+1}/{len(self.pages)})\n{self.pages[self.page]}",
            view=self
        )

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < len(self.pages) - 1:
            self.page += 1
            await self.update(interaction)

def user_has_override_role(member: discord.Member) -> bool:
    return any(role.id == ADMIN_ROLE for role in member.roles)

# Generate pages from station data
def generate_pages(data, page_size=10):
    pages = []
    for i in range(0, len(data), page_size):
        chunk = data[i:i + page_size]
        lines = [
            f"📍 **{station}** (`{system}`) — Last updated: `{human_time}`"
            for station, system, human_time, _ in chunk
        ]
        pages.append("\n".join(lines))
    return pages

async def cmdr_autocomplete(interaction: discord.Interaction, current: str):
    role = interaction.guild.get_role(ADMIN_ROLE)  # Adjust if needed
    if not role:
        return []
    
    return [
        app_commands.Choice(name=member.display_name, value=str(member.id))
        for member in role.members
        if current.lower() in member.display_name.lower()
    ][:25]

class ShopPaginator(discord.ui.View):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(timeout=180)
        self.pages = pages
        self.current_page = 0

    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.defer()


# --- Autocomplete for action ---
async def action_autocomplete(interaction: discord.Interaction, current: str):
    options = ["add", "remove", "show"]
    return [
        app_commands.Choice(name=option, value=option)
        for option in options if current.lower() in option
    ]

# --- Load Participants ---
def load_participants():
    if os.path.exists(PARTICIPANT_FILE):
        with open(PARTICIPANT_FILE, "r") as f:
            return json.load(f)
    return {}

# --- Save Participants ---
def save_participants(data):
    with open(PARTICIPANT_FILE, "w") as f:
        json.dump(data, f, indent=2)


COMRADERY_FILE = "comradery_points.json"

def load_comradery_points():
    if not os.path.exists(COMRADERY_FILE):
        return {}
    with open(COMRADERY_FILE, "r") as f:
        return json.load(f)

def save_comradery_points(data):
    with open(COMRADERY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f)

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


async def biowaste_station_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    try:
        with open("biowaste_markets.json", "r") as f:
            stations = json.load(f)
    except Exception:
        return []

    suggestions = [
        app_commands.Choice(name=entry["stationName"], value=entry["stationName"])
        for entry in stations if current.lower() in entry["stationName"].lower()
    ]
    return suggestions[:25]



async def get_motivational_gif(search_term:str):
    url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_API_KEY,
        "q": search_term,
        "limit": 10,
        "rating": "pg",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                gifs = data.get("data", [])
                if gifs:
                    return random.choice(gifs)["images"]["original"]["url"]
    return None


def load_ships():
    if not os.path.exists(FERRY_FILE):
        return []
    with open(FERRY_FILE, "r") as f:
        data = json.load(f)
        return [(entry["name"], entry["direction"], datetime.fromisoformat(entry["time"])) for entry in data]

# Save ships to JSON
def save_ships(ships):
    with open(FERRY_FILE, "w") as f:
        json.dump([
            {"name": name, "direction": direction, "time": time.isoformat()}
            for name, direction, time in ships
        ], f, indent=2)

# Ensure data file exists
if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def update_hauler_cargo(user_id: int, username: str, cargo_amount: int):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if str(user_id) in data:
        data[str(user_id)]["cargo"] += cargo_amount
    else:
        data[str(user_id)] = {
            "username": username,
            "cargo": cargo_amount
        }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Helper function to clean old ferry calls
def clean_old_calls():
    current_time = datetime.now(timezone.utc)
    while calls and (current_time - calls[0][1]).total_seconds() > 600:  # 10 minutes = 600 seconds
        calls.popleft()


async def queryTable():
    url="https://script.google.com/macros/s/AKfycbwHuIBGMf4ohKMNCrVVJ22t0IwQ1rgRxt3EViWPBpfPG6RUAuOe1XdT3cLms-3pSUjJTg/exec"
    response=requests.get(url)
    data=response.json()
    tableData=[]
    for com in data:
        tableData.append([list(com.keys())[0],list(com.values())[0]])
    return tableData

    
def has_required_role(role_id: int):
    async def predicate(interaction: discord.Interaction) -> bool:
        return any(role.id == role_id for role in interaction.user.roles)
    return app_commands.check(predicate)

##########################################################################################################


class OpsActionView(ui.View):
    def __init__(self, user_role_flags, expedition_data, sheet_id):
        super().__init__(timeout=120)
        self.user_is_hauler = user_role_flags['hauler']
        self.user_is_fc_owner = user_role_flags['fc_owner']
        self.user_is_admin = user_role_flags['admin']
        self.expedition_data = expedition_data
        self.sheet_id = sheet_id

        if self.user_is_hauler or self.user_is_fc_owner:
            self.add_item(DropoffButton(sheet_id))
            self.add_item(MarkFCEmptyButton(sheet_id, expedition_data))
            self.add_item(MarkFCFullButton(sheet_id))
            self.add_item(MarkCompletedButton(sheet_id))
            self.add_item(MarkNextClaimedButton(sheet_id))
            if expedition_data["dibs"]:
                self.add_item(CallDibsButton(sheet_id))
  

        if self.user_is_fc_owner or self.user_is_admin:
            self.add_item(OpenResupplyButton(sheet_id, expedition_data, is_admin=self.user_is_admin))
            self.add_item(ReadyToDeployButton(sheet_id, is_admin=self.user_is_admin))
            self.add_item(OpenForUnloadButton(sheet_id, is_admin=self.user_is_admin))
            self.add_item(SuspendButton(sheet_id, expedition_data, is_admin=self.user_is_admin))
        if (not self.user_is_hauler and not self.user_is_fc_owner and not self.user_is_admin):
            class JoinExpeditionButton(discord.ui.Button):
                def __init__(self, expedition):
                    super().__init__(label="Join This Expedition", style=discord.ButtonStyle.primary)
                    self.expedition = expedition

                async def callback(self, interaction: Interaction):
                    view = JoinRoleSelector(self.expedition)
                    await interaction.response.send_message(
                        f"🧭 You're joining **{self.expedition['name']}**! Select your role:",
                        view=view,
                        ephemeral=True
                    )

            class JoinRoleSelector(discord.ui.View):
                def __init__(self, expedition):
                    super().__init__()
                    self.expedition = expedition

                async def handle_hauler(self, sheets, username):
                                if any(username.lower() == row[0].strip().lower() for row in sheets["hauler_manifest"][1:]):
                                    return False
                                sheets["hauler_ws"].append_row([username, "0", "Joined @ " + datetime.utcnow().isoformat()])
                                return True

                async def handle_fc_owner(self, interaction, sheets, username, skip_modal=False):
                    if any(username.lower() == row[2].strip().lower() for row in sheets["fc_manifest"][1:]):
                        await interaction.response.send_message("⚠️ You're already listed as an FC owner.", ephemeral=True)
                        return

                    resupply = self.expedition["resupply"]

                    class FCInfoModal(discord.ui.Modal, title="Enter FC Info"):
                        callsign = discord.ui.TextInput(label="FC Callsign", placeholder="ABC-123", required=True)
                        name = discord.ui.TextInput(label="FC Name", required=True)

                        async def on_submit(modal_self, inter: discord.Interaction):
                            cs = modal_self.callsign.value.strip().upper()
                            name = modal_self.name.value.strip()
                            now = datetime.utcnow().isoformat()

                            import re
                            if not re.fullmatch(r"[A-Z0-9]{3}-[A-Z0-9]{3}", cs):
                                await inter.response.send_message("❌ Invalid format. Use `ABC-123`.", ephemeral=True)
                                return

                            if any(cs == row[0].strip().upper() for row in sheets["fc_manifest"][1:]):
                                await inter.response.send_message(
                                    f"⚠️ An FC with callsign `{cs}` is already registered.",
                                    ephemeral=True
                                )
                                return

                            sheets["fc_ws"].append_row([cs, name, username, "Empty", now, resupply])
                            id=self.expedition["Keyword"]
                            await inter.response.send_message(
                                f"✅ FC **{name}** with callsign `{cs}` added.\n📍 Please jump your FC to `{resupply}`. When your buy orders are open, run `/ops id:{id}` and select **Open for Resupply**.",
                                ephemeral=True
                            )

                    await interaction.response.send_modal(FCInfoModal())

                @ui.button(label="Hauler", style=discord.ButtonStyle.secondary)
                async def join_hauler(self, interaction: Interaction, button: ui.Button):
                    sheets = load_expedition_sheet(self.expedition["SheetID"])
                    username = interaction.user.display_name.strip()
                    if any(username.lower() == row[0].strip().lower() for row in sheets["hauler_manifest"][1:]):
                        await interaction.response.send_message("⚠️ You're already listed as a hauler.", ephemeral=True)
                        return
                    sheets["hauler_ws"].append_row([username, "0", f"Joined @ {datetime.utcnow().isoformat()}"])
                    await interaction.response.send_message(f"✅ Added to Hauler-Manifest for `{self.expedition['name']}`.", ephemeral=True)

                @discord.ui.button(label="FC Owner", style=discord.ButtonStyle.secondary)
                async def join_fc(self, interaction: discord.Interaction, button: discord.ui.Button):
                    sheets = load_expedition_sheet(self.expedition["SheetID"])
                    username = interaction.user.display_name.strip()
                    await self.handle_fc_owner(interaction, sheets, username)

                @discord.ui.button(label="Both", style=discord.ButtonStyle.success)
                async def join_both(self, interaction: discord.Interaction, button: discord.ui.Button):
                    sheets = load_expedition_sheet(self.expedition["SheetID"])
                    username = interaction.user.display_name.strip()

                    already_hauler = any(username.lower() == row[0].strip().lower() for row in sheets["hauler_manifest"][1:])
                    already_fc = any(username.lower() == row[2].strip().lower() for row in sheets["fc_manifest"][1:])

                    if already_hauler and already_fc:
                        await interaction.response.send_message("⚠️ You're already listed as both a hauler and FC owner.", ephemeral=True)
                        return

                    if not already_hauler:
                        await self.handle_hauler(sheets, username)

                    if not already_fc:
                        await self.handle_fc_owner(interaction, sheets, username)


            self.add_item(JoinExpeditionButton({
                "SheetID": self.sheet_id,
                "name": self.expedition_data["name"],
                "resupply": self.expedition_data["resupply"],
                "Keyword": self.expedition_data["Keyword"]
            }))
        self.add_item(HelpButton())
        self.add_item(MapButton())



def clean_label(text):
    text = str(text)
    safe = ''.join(c for c in text if c in string.printable and c not in '\n\r\t')
    return safe[:100]

class HelpButton(ui.Button):
    def __init__(self):
        super().__init__(
            label="Help?",
            style=discord.ButtonStyle.link,
            url="https://docs.google.com/document/d/1pZ6sLvLCb24HXt_n4jJfXSLAXXRfSJz1_EbqdAXVZso/edit?usp=sharing"
        )

class MapButton(ui.Button):
    def __init__(self):
        super().__init__(
            label="3D Map",
            style=discord.ButtonStyle.link,
            url="https://oasis-cartograph.onrender.com/"
        )

class DropoffButton(ui.Button):
    def __init__(self, sheet_id):
        super().__init__(label="Log Dropoff", style=discord.ButtonStyle.success)
        self.sheet_id = sheet_id

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        await interaction.followup.send_modal(DropoffModal(sheets, self.sheet_id))


class DropoffModal(ui.Modal, title="Log Dropoff"):
    def __init__(self, sheets, sheet_id):
        super().__init__()
        self.sheets = sheets
        self.sheet_id = sheet_id
        self.tons = ui.TextInput(label="How many tons did you deliver?", placeholder="Enter a number", required=True)
        self.add_item(self.tons)

    async def on_submit(self, interaction: Interaction):
        sheets = load_expedition_sheet(self.sheet_id)
        username = interaction.user.display_name.strip().lower()

        box_motivational_quotes = [
            "Another box down, you're on fire! 📦🔥",
            "Stack 'em high, commander! 📦🚀",
            "That box didn’t stand a chance. 📦💪",
            "You just leveled up the logistics game! 📦🎯",
            "Boxes beware—you’re unstoppable! 📦⚡",
            "Precision delivery, nailed it. 📦📍",
            "Smooth drop! You make it look easy. 📦😎",
            "You're crushing crates and taking names. 📦📝",
            "That box just found its forever home. 📦🏠",
            "Boom—box delivered like a pro! 📦💼",
            "Drop complete! The galaxy thanks you. 📦🌌",
            "One box at a time, you're making history. 📦📖",
            "Your cargo game is elite. 📦🏆",
            "Another perfect delivery. 📦👌",
            "The box is strong with this one. 📦🌀",
            "You move boxes like a space wizard. 📦🪄",
            "Clean drop, no dents! 📦✨",
            "The crate life chose you. 📦🧬",
            "You deliver like no other. 📦🚛",
            "That's some box-fu right there. 📦🥋",
            "Transport titan in the making! 📦👑",
            "Mission: Crate Success. 📦✔️",
            "Heavy lifting? Light work for you. 📦💼",
            "Box after box, you're building a legacy. 📦🏗️",
            "You just dropped greatness. 📦💥",
            "Galactic logistics MVP. 📦🏅",
            "Zero gravity? Zero problem. 📦🌠",
            "Another one in the manifest. 📦📋",
            "Space is cleaner now—thanks to you. 📦🧹",
            "Boxes go in, heroes come out. 📦🦸",
            "Precision payload, flawless execution. 📦🎯",
            "The cargo whisperer strikes again. 📦🗣️",
            "Another successful supply run. 📦🛠️",
            "You're basically a box magician. 📦🎩",
            "Crate fate sealed. 📦🔒",
            "Supply lines dream of workers like you. 📦🌌",
            "Commanders deliver, legends *drop off*. 📦💣",
            "Fast, fearless, and full of boxes. 📦🏎️",
            "Your crate karma is off the charts. 📦📈",
            "The boxes salute you. 📦🫡",
            "Crate by crate, galaxy saved. 📦💫",
            "You dropped that like a champion. 📦🥇",
            "No cargo left behind! 📦🚨",
            "The universe moves because you do. 📦🌠",
            "Nothing but net—box scored! 📦🏀",
            "Interstellar shipping excellence. 📦🌌",
            "Box. Drop. Repeat. 📦🔁",
            "Galactic logistics never looked so cool. 📦🆒",
            "You make crates proud. 📦❤️"
            ]

        motivation = random.choice(box_motivational_quotes)
        try:
            tons = int(self.tons.value.strip())
        except ValueError:
            await interaction.response.send_message("❌ Invalid number.", ephemeral=True)
            return

        updated = False
        for i, row in enumerate(sheets["hauler_manifest"]):
            if i == 0:
                continue
            if row[0].strip().lower() == username:
                prev = int(row[1]) if row[1].isdigit() else 0
                sheets["hauler_ws"].update_cell(i + 1, 2, prev + tons)
                sheets["hauler_ws"].update_cell(i + 1, 3, f"Dropoff {tons} tons @ {datetime.utcnow().isoformat()}")
                updated = True
                break

        if updated:
            await interaction.response.send_message(f"✅ Logged **{tons} tons** to your total. /n {motivation}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You are not listed in the Hauler Manifest.", ephemeral=True)

class MarkNextClaimedButton(ui.Button):
    def __init__(self, sheet_id):
        super().__init__(label="Mark System As Claimed", style=discord.ButtonStyle.secondary)
        self.sheet_id = sheet_id

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        route_rows = sheets["route"]

        for i, row in enumerate(route_rows):
            if i == 0:
                continue
            if row[2].strip().lower() != "true":
                if i > 1:
                    prev_row = route_rows[i - 1]
                    if prev_row[3].strip().lower() != "true":
                        msg = "⚠️ You must mark the current system as complete first."
                        if not interaction.response.is_done():
                            await interaction.response.send_message(msg, ephemeral=True)
                        else:
                            await interaction.followup.send(msg, ephemeral=True)
                        return

                sheets["route_ws"].update_cell(i + 1, 3, "TRUE")
                msg = f"✅ Marked `{row[1]}` as claimed."
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)

                # Send bacon image
                bacon_images = [
                    "https://tse1.mm.bing.net/th?id=OIP.fIcnwqa4B9s_mpWPn54JgwHaJ4&pid=Api",
                    "https://tse4.mm.bing.net/th?id=OIP.ejC-EuQmzWKvHxdDj9ycegHaFj&pid=Api",
                    "https://tse3.mm.bing.net/th?id=OIP.UuxGRcQNSkgcAOEs1XB1VwHaHW&pid=Api",
                ]
                chosen = random.choice(bacon_images)
                await interaction.followup.send(content=f"🥓 Bacon Deployed!\n{chosen}")
                return

        msg = "❌ No unclaimed system found in the route."
        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)

class MarkCompletedButton(ui.Button):
    def __init__(self, sheet_id):
        super().__init__(label="Mark Current System As Completed", style=discord.ButtonStyle.success)
        self.sheet_id = sheet_id

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        setup = sheets["setup"]
        route_rows = sheets["route"]

        cell = setup.acell("B7").value
        claim_system = cell.strip().lower() if cell else ""
        updated = False

        for i, row in enumerate(route_rows):
            if i == 0:
                continue
            if row[1].strip().lower() == claim_system:
                sheets["route_ws"].update_cell(i + 1, 4, "TRUE")
                updated = True

                # Notify next dibs if any
                if i + 1 < len(route_rows):
                    next_row = route_rows[i + 1]
                    next_username = next_row[4].strip()
                    if next_username:
                        member = next(
                            (m for m in interaction.guild.members if m.name == next_username or m.display_name == next_username),
                            None
                        )
                        if member:
                            try:
                                await member.send(
                                    f"📢 You're up to claim the next system: **{next_row[1]}**!\n"
                                    f"Please run `/ops` and mark it as claimed for Boxbot."
                                )
                            except:
                                pass

                # Log in hauler manifest
                username = interaction.user.display_name.strip().lower()
                for j, h_row in enumerate(sheets["hauler_manifest"]):
                    if j == 0:
                        continue
                    if h_row[0].strip().lower() == username:
                        sheets["hauler_ws"].update_cell(j + 1, 3,
                            f"Marked completed {row[1]} @ {datetime.utcnow().isoformat()}"
                        )
                        break
                break

        if updated:
            msg = f"✅ Marked `{claim_system}` as completed."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)

            # Post celebratory GIF
            gif_folder = "brewer-gifs"
            gifs = [
                f for f in os.listdir(gif_folder)
                if os.path.isfile(os.path.join(gif_folder, f)) and f.lower().endswith(('.gif', '.mp4', '.webm'))
            ]
            if gifs:
                chosen_gif = random.choice(gifs)
                file_path = os.path.join(gif_folder, chosen_gif)
                file = discord.File(file_path)
                await interaction.channel.send("🎉 System completed!", file=file)
            else:
                await interaction.channel.send("🎉 System completed! (No celebratory gif found.)")
        else:
            msg = f"❌ Could not find `{claim_system}` in the route."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)

class OpenResupplyButton(ui.Button):
    def __init__(self, sheet_id, expedition_data, is_admin=False):
        super().__init__(label="Open for Resupply", style=discord.ButtonStyle.primary)
        self.sheet_id = sheet_id
        self.resupply_system = expedition_data["resupply"]
        self.is_admin = is_admin

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        username = interaction.user.display_name.strip().lower()

        if self.is_admin:
            fc_options = [
                discord.SelectOption(label=f"{row[0]} – {row[1]} (Owner: {row[2]})", value=str(i))
                for i, row in enumerate(sheets["fc_manifest"])
                if i > 0 and row[3] == "Empty"
            ]

            if not fc_options:
                msg = "❌ No FCs in 'Empty' state available for resupply."
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

            class FCSelect(ui.Select):
                def __init__(inner_self):
                    super().__init__(placeholder="Select FC to open for resupply", options=fc_options)

                async def callback(inner_self, interaction2: Interaction):
                    sheets = load_expedition_sheet(self.sheet_id)
                    index = int(inner_self.values[0])
                    sheets["fc_ws"].update_cell(index + 1, 4, "Loading")
                    sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())
                    sheets["fc_ws"].update_cell(index + 1, 6, self.resupply_system)
                    await interaction2.response.send_message(
                        f"✅ FC `{sheets['fc_manifest'][index][0]}` is now open for resupply.",
                        ephemeral=True
                    )

            view = ui.View()
            view.add_item(FCSelect())
            if not interaction.response.is_done():
                await interaction.response.send_message("🔽 Select an FC to open for resupply:", view=view, ephemeral=True)
            else:
                await interaction.followup.send("🔽 Select an FC to open for resupply:", view=view, ephemeral=True)
            return

        # Owner logic
        updated = False
        for i, row in enumerate(sheets["fc_manifest"]):
            if i == 0:
                continue
            if row[2].strip().lower() == username:
                if row[3] != "Empty":
                    msg = "⚠️ FC must be in 'Empty' state to open for resupply."
                    if not interaction.response.is_done():
                        await interaction.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction.followup.send(msg, ephemeral=True)
                    return
                sheets["fc_ws"].update_cell(i + 1, 4, "Loading")
                sheets["fc_ws"].update_cell(i + 1, 5, datetime.utcnow().isoformat())
                sheets["fc_ws"].update_cell(i + 1, 6, self.resupply_system)
                updated = True
                break

        if updated:
            msg = "✅ Your FC is now open for resupply."
        else:
            msg = "❌ No FC found for you in the manifest."

        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)

class MarkFCFullButton(ui.Button):
    def __init__(self, sheet_id):
        super().__init__(label="Mark an FC as Full", style=discord.ButtonStyle.success)
        self.sheet_id = sheet_id

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        loading_fcs = [
            (i, row) for i, row in enumerate(sheets["fc_manifest"])
            if i > 0 and row[3] == "Loading"
        ]

        if not loading_fcs:
            msg = "❌ No FCs currently in 'Loading' state."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)
            return

        options = [
            discord.SelectOption(label=f"{row[0]} – {row[1]}", value=str(i))
            for i, row in loading_fcs
        ]

        class FCFullSelect(ui.Select):
            def __init__(inner_self):
                super().__init__(placeholder="Select an FC to mark as Full", options=options)

            async def callback(inner_self, interaction2: Interaction):
                sheets = load_expedition_sheet(self.sheet_id)
                index = int(inner_self.values[0])
                sheets["fc_ws"].update_cell(index + 1, 4, "Full")
                sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())

                owner = sheets["fc_manifest"][index][2].strip()
                member = next(
                    (m for m in interaction.guild.members if m.name == owner or m.display_name == owner),
                    None
                )
                if member:
                    try:
                        await member.send(
                            f"🚀 Your FC `{sheets['fc_manifest'][index][0]}` has been marked as FULL.\n"
                            f"Please run `/ops` to deploy your carrier to the next system."
                        )
                    except:
                        pass

                await interaction2.response.send_message(
                    f"✅ Marked FC `{sheets['fc_manifest'][index][0]}` as Full.",
                    ephemeral=True
                )

                # Resupply meme
                meme_folder = "Resupply-memes"
                memes = [
                    f for f in os.listdir(meme_folder)
                    if os.path.isfile(os.path.join(meme_folder, f)) and f.lower().endswith('.jpg')
                ]

                if memes:
                    chosen_meme = random.choice(memes)
                    file = discord.File(os.path.join(meme_folder, chosen_meme))
                    await interaction2.channel.send(
                        "📦 Resupply complete! Here's a meme for your trouble:",
                        file=file
                    )
                else:
                    await interaction2.channel.send(
                        "📦 Resupply complete! (No memes found to share.)"
                    )

        view = ui.View()
        view.add_item(FCFullSelect())

        if not interaction.response.is_done():
            await interaction.response.send_message("🔽 Select an FC to mark as Full:", view=view, ephemeral=True)
        else:
            await interaction.followup.send("🔽 Select an FC to mark as Full:", view=view, ephemeral=True)

class MarkFCEmptyButton(ui.Button):
    def __init__(self, sheet_id, expedition_data):
        super().__init__(label="Mark an FC as Empty", style=discord.ButtonStyle.success)
        self.sheet_id = sheet_id
        self.resupply = expedition_data["resupply"]

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        unloading_fcs = [
            (i, row) for i, row in enumerate(sheets["fc_manifest"])
            if i > 0 and row[3] in ["Unloading", "Deployed"]
        ]

        if not unloading_fcs:
            msg = "❌ No FCs in 'Unloading' or 'Deployed' state found."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)
            return

        options = [
            discord.SelectOption(label=f"{row[0]} – {row[1]}", value=str(i))
            for i, row in unloading_fcs
        ]

        class FCSelect(ui.Select):
            def __init__(inner_self):
                super().__init__(placeholder="Select an FC to mark as Empty", options=options)

            async def callback(inner_self, interaction2: Interaction):
                sheets = load_expedition_sheet(self.sheet_id)
                index = int(inner_self.values[0])
                sheets["fc_ws"].update_cell(index + 1, 4, "Empty")
                sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())

                owner = sheets["fc_manifest"][index][2].strip()
                member = next(
                    (m for m in interaction.guild.members if m.name == owner or m.display_name == owner),
                    None
                )
                if member:
                    try:
                        await member.send(
                            f"📦 Your FC `{sheets['fc_manifest'][index][0]}` has been marked as EMPTY.\n"
                            f"Please jump to `{self.resupply}` and run `/ops` to open for resupply."
                        )
                    except:
                        pass

                await interaction2.response.send_message(
                    f"✅ Marked FC `{sheets['fc_manifest'][index][0]}` as Empty.",
                    ephemeral=True
                )

        view = ui.View()
        view.add_item(FCSelect())

        if not interaction.response.is_done():
            await interaction.response.send_message("🔽 Select an FC to mark as Empty:", view=view, ephemeral=True)
        else:
            await interaction.followup.send("🔽 Select an FC to mark as Empty:", view=view, ephemeral=True)
class CallDibsButton(ui.Button):
    def __init__(self, sheet_id):
        super().__init__(label="Call Dibs on Upcoming System", style=discord.ButtonStyle.success)
        self.sheet_id = sheet_id

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        all_upcoming = [
            row for row in sheets["route"][1:]
            if row[2].strip().lower() != "true" and len(row[0].strip()) > 0
        ]
        upcoming = all_upcoming[:min(5, len(all_upcoming))]

        if not upcoming:
            msg = "❌ No unclaimed systems available to call dibs on."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)
            return

        options = []
        for i, row in enumerate(upcoming):
            system_name = row[1].strip()
            dibs_holder = row[4].strip() if len(row) > 4 and row[4] else ""
            if not dibs_holder:
                options.append(discord.SelectOption(label=system_name, value=str(i)))
            else:
                label = f"{system_name} (claimed by {dibs_holder})"
                options.append(discord.SelectOption(label=label[:100], value="locked", description="Already claimed", emoji="🔒"))

        available_options = [o for o in options if o.value != "locked"]

        if not available_options:
            msg = "❌ No unclaimed systems available to call dibs on."
            if not interaction.response.is_done():
                await interaction.response.send_message(msg, ephemeral=True)
            else:
                await interaction.followup.send(msg, ephemeral=True)
            return

        class DibsSelect(ui.Select):
            def __init__(inner_self):
                super().__init__(placeholder="Select a system to call dibs", options=available_options)

            async def callback(inner_self, interaction2: Interaction):
                sheets = load_expedition_sheet(self.sheet_id)
                index = int(inner_self.values[0])
                row_idx = sheets["route"].index(upcoming[index])
                name = interaction.user.display_name
                sheets["route_ws"].update_cell(row_idx + 1, 5, name)

                msg = f"✅ You called dibs on `{upcoming[index][1]}`!"
                if not interaction2.response.is_done():
                    await interaction2.response.send_message(msg, ephemeral=True)
                else:
                    await interaction2.followup.send(msg, ephemeral=True)

        view = ui.View()
        view.add_item(DibsSelect())

        if not interaction.response.is_done():
            await interaction.response.send_message("🛸 Pick a system to call dibs:", view=view, ephemeral=True)
        else:
            await interaction.followup.send("🛸 Pick a system to call dibs:", view=view, ephemeral=True)

class ReadyToDeployButton(ui.Button):
    def __init__(self, sheet_id, is_admin=False):
        super().__init__(label="Ready to Deploy", style=discord.ButtonStyle.primary)
        self.sheet_id = sheet_id
        self.is_admin = is_admin

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        username = interaction.user.display_name.strip().lower()
        cell = sheets["setup"].acell("B7").value
        current_system = cell.strip() if cell else ""

        def deploy_fc(index: int):
            last_filled = 0
            for j, r_row in enumerate(sheets["route"]):
                if j == 0:
                    continue
                if r_row[5].strip():
                    last_filled = j

            next_row_idx = last_filled + 1
            if next_row_idx < len(sheets["route"]):
                deployed_system = sheets["route"][next_row_idx][1].strip()
                sheets["fc_ws"].update_cell(index + 1, 4, "Deployed")
                sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())
                sheets["fc_ws"].update_cell(index + 1, 6, deployed_system)
                sheets["route_ws"].update_cell(next_row_idx + 1, 6, sheets["fc_manifest"][index][0])
                return f"✅ FC `{sheets['fc_manifest'][index][0]}` deployed to `{deployed_system}`"
            else:
                return "⚠️ No available unassigned systems to deploy to."

        if self.is_admin:   
            eligible = [
                (i, row) for i, row in enumerate(sheets["fc_manifest"])
                if i > 0 and row[3] in ["Loading", "Full"]
            ]

            if not eligible:
                msg = "❌ No FCs eligible for deployment."
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

            options = [
                discord.SelectOption(label=f"{row[0]} – {row[1]} (Owner: {row[2]})", value=str(i))
                for i, row in eligible
            ]

            class DeploySelect(ui.Select):
                def __init__(inner_self):
                    super().__init__(placeholder="Select FC to deploy", options=options)

                async def callback(inner_self, interaction2: Interaction):
                    sheets = load_expedition_sheet(self.sheet_id)
                    index = int(inner_self.values[0])
                    msg = deploy_fc(index)
                    if not interaction2.response.is_done():
                        await interaction2.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction2.followup.send(msg, ephemeral=True)

            view = ui.View()
            view.add_item(DeploySelect())
            if not interaction.response.is_done():
                await interaction.response.send_message("🚀 Select an FC to deploy:", view=view, ephemeral=True)
            else:
                await interaction.followup.send("🚀 Select an FC to deploy:", view=view, ephemeral=True)
            return

        # FC owner logic
        for i, row in enumerate(sheets["fc_manifest"]):
            if i == 0:
                continue
            if row[2].strip().lower() == username:
                if row[3] not in ["Loading", "Full"]:
                    msg = "⚠️ FC must be in 'Loading' or 'Full' state to deploy."
                    if not interaction.response.is_done():
                        await interaction.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction.followup.send(msg, ephemeral=True)
                    return
                msg = deploy_fc(i)
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

        msg = "❌ You do not appear to own any FCs in this expedition."
        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)

class OpenForUnloadButton(ui.Button):
    def __init__(self, sheet_id, is_admin=False):
        super().__init__(label="Open for Unload", style=discord.ButtonStyle.primary)
        self.sheet_id = sheet_id
        self.is_admin = is_admin

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        username = interaction.user.display_name.strip().lower()

        def mark_unloading(index: int):
            sheets["fc_ws"].update_cell(index + 1, 4, "Unloading")
            sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())
            return f"✅ FC `{sheets['fc_manifest'][index][0]}` is now marked as 'Unloading'."

        if self.is_admin:
            eligible = [
                (i, row) for i, row in enumerate(sheets["fc_manifest"])
                if i > 0 and row[3] == "Deployed"
            ]

            if not eligible:
                msg = "❌ No FCs currently in 'Deployed' state."
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

            options = [
                discord.SelectOption(label=f"{row[0]} – {row[1]} (Owner: {row[2]})", value=str(i))
                for i, row in eligible
            ]

            class UnloadSelect(ui.Select):
                def __init__(inner_self):
                    super().__init__(placeholder="Select FC to open for unload", options=options)

                async def callback(inner_self, interaction2: Interaction):
                    sheets = load_expedition_sheet(self.sheet_id)
                    index = int(inner_self.values[0])
                    msg = mark_unloading(index)
                    if not interaction2.response.is_done():
                        await interaction2.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction2.followup.send(msg, ephemeral=True)

            view = ui.View()
            view.add_item(UnloadSelect())
            if not interaction.response.is_done():
                await interaction.response.send_message("📤 Select an FC to open for unload:", view=view, ephemeral=True)
            else:
                await interaction.followup.send("📤 Select an FC to open for unload:", view=view, ephemeral=True)
            return

        # FC owner logic
        for i, row in enumerate(sheets["fc_manifest"]):
            if i == 0:
                continue
            if row[2].strip().lower() == username:
                if row[3] != "Deployed":
                    msg = "⚠️ FC must be in 'Deployed' state to open for unload."
                    if not interaction.response.is_done():
                        await interaction.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction.followup.send(msg, ephemeral=True)
                    return
                msg = mark_unloading(i)
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

        msg = "❌ You do not appear to own any FCs in this expedition."
        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)

class SuspendButton(ui.Button):
    def __init__(self, sheet_id, expedition_data, is_admin=False):
        super().__init__(label="Suspend FC", style=discord.ButtonStyle.danger)
        self.sheet_id = sheet_id
        self.expedition_data = expedition_data
        self.is_admin = is_admin

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        sheets = load_expedition_sheet(self.sheet_id)
        username = interaction.user.display_name.strip().lower()

        async def suspend_fc(index: int, owner_display: str):
            callsign = sheets["fc_manifest"][index][0].strip()
            system_assigned = sheets["fc_manifest"][index][5].strip()

            sheets["fc_ws"].update_cell(index + 1, 4, "Suspended")
            sheets["fc_ws"].update_cell(index + 1, 5, datetime.utcnow().isoformat())

            # Clear route assignment
            for j, r_row in enumerate(sheets["route"]):
                if j == 0:
                    continue
                if r_row[5].strip() == callsign:
                    sheets["route_ws"].update_cell(j + 1, 6, "")
                    break

            # Notify admins
            admin_usernames = [r[0].strip() for r in sheets["admin_manifest"] if r[0].strip().lower() != "username"]
            for admin_name in admin_usernames:
                member = next((m for m in interaction.guild.members if m.name == admin_name or m.display_name == admin_name), None)
                if member:
                    try:
                        await member.send(
                            f"🚨 The FC `{callsign}` owned by `{owner_display}` has been suspended."
                            + (f" It was assigned to `{system_assigned}`." if system_assigned else "")
                        )
                    except:
                        pass

            return (
                f"❗ FC `{callsign}` has been suspended. Admins notified."
                + (f" Removed from system `{system_assigned}`." if system_assigned else "")
            )

        if self.is_admin:
            options = [
                discord.SelectOption(label=f"{row[0]} – {row[1]} (Owner: {row[2]})", value=str(i))
                for i, row in enumerate(sheets["fc_manifest"]) if i > 0
            ]

            if not options:
                msg = "❌ No FCs found to suspend."
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

            class SuspendSelect(ui.Select):
                def __init__(inner_self):
                    super().__init__(placeholder="Select an FC to suspend", options=options)

                async def callback(inner_self, interaction2: Interaction):
                    sheets = load_expedition_sheet(self.sheet_id)
                    index = int(inner_self.values[0])
                    msg = await suspend_fc(index, sheets["fc_manifest"][index][2])
                    if not interaction2.response.is_done():
                        await interaction2.response.send_message(msg, ephemeral=True)
                    else:
                        await interaction2.followup.send(msg, ephemeral=True)

            view = ui.View()
            view.add_item(SuspendSelect())
            if not interaction.response.is_done():
                await interaction.response.send_message("🚫 Select an FC to suspend:", view=view, ephemeral=True)
            else:
                await interaction.followup.send("🚫 Select an FC to suspend:", view=view, ephemeral=True)
            return

        # FC owner logic
        for i, row in enumerate(sheets["fc_manifest"]):
            if i == 0:
                continue
            if row[2].strip().lower() == username:
                msg = await suspend_fc(i, interaction.user.display_name)
                if not interaction.response.is_done():
                    await interaction.response.send_message(msg, ephemeral=True)
                else:
                    await interaction.followup.send(msg, ephemeral=True)
                return

        msg = "❌ You do not appear to own any FCs in this expedition."
        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)
#####################################################################################################


class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild=GUILD_ID
            synced=await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
            await client.wait_until_ready()
            if(DYNAMIC_WING_COMS_SWITCH):
                await initialize_xwing_system()
            if(BACKGROUND_CHANGE_FEATURE_SWITCH):
                daily_banner_update.start()
            async def cleanup_yardsale():
                await client.wait_until_ready()
            client.loop.create_task(cleanup_yardsale())
            update_biowaste_markets.start()
            update_top_markets.start()

        except:
            print(f'Error syncing commands: {e}')

client=Client(command_prefix="!",intents=intents)


TOP_MARKETS_FILE = "top_markets.json"

@tasks.loop(hours=4)
async def update_top_markets():
    print("🔍 Running top markets update task...")
    try:
        with open("biowaste_markets.json", "r") as f:
            markets = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read biowaste_markets.json: {e}")
        return

    commodity_map = COMMODITY_NAME_LOOKUP
    reverse_lookup = {v: k for k, v in commodity_map.items()}
    all_commodities = set(commodity_map.values())

    top_markets = {commodity: [] for commodity in commodity_map.keys()}

    async with aiohttp.ClientSession() as session:
        for market in markets:
            market_id = market.get("marketId")
            market_type=market.get("stationType","unknown")
            if not market_id:
                continue

            url = f"https://api.ardent-industry.com/v1/market/{market_id}/commodities"
            try:
                async with session.get(url) as res:
                    if res.status != 200:
                        continue
                    data = await res.json()
            except Exception as e:
                print(f"⚠️ Error fetching market {market_id}: {e}")
                continue

            for entry in data:
                name = entry.get("commodityName")
                if name in all_commodities and entry.get("stock", 0) > 0:
                    readable_name = reverse_lookup.get(name)
                    if readable_name:
                        top_markets[readable_name].append({
                            "marketId": market_id,
                            "stationName": market.get("stationName"),
                            "stationType": market_type,
                            "systemName": market.get("systemName"),
                            "stock": entry.get("stock")
                        })

    # Sort each list and keep top 2
    for commodity in top_markets:
        top_markets[commodity] = sorted(
            top_markets[commodity], key=lambda x: x["stock"], reverse=True
        )[:2]

    with open(TOP_MARKETS_FILE, "w") as f:
        json.dump(top_markets, f, indent=2)

    print("✅ Top markets updated.")



BIOWASTE_DATA_FILE = "biowaste_markets.json"

@tasks.loop(hours=4)
async def update_biowaste_markets():
    print("⏳ Running biowaste market update task...")
    urls = [
        f"https://api.ardent-insight.com/v1/system/name/{ORIGIN_SYS}/commodity/name/biowaste/nearby/exports?fleetCarriers=0&maxDistance={WASTE_RADIUS}",
        f"https://api.ardent-insight.com/v1/system/name/{ORIGIN_SYS}/commodity/name/biowaste/nearby/imports?fleetCarriers=0&maxDistance={WASTE_RADIUS}",
        f"https://api.ardent-insight.com/v2/system/name/{ORIGIN_SYS}/commodities"
    ]

    seen_ids = set()
    combined_results = []

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as res:
                    if res.status == 200:
                        data = await res.json()
                        for entry in data:
                            market_id = entry.get("marketId")
                            if market_id not in seen_ids:
                                seen_ids.add(market_id)
                                combined_results.append({
                                    "marketId": market_id,
                                    "stationName": entry.get("stationName", "Unknown"),
                                    "maxLandingPadSize": entry.get("maxLandingPadSize", "Unknown"),
                                    "systemName": entry.get("systemName","2MASS J05405172-0226489"),
                                    "stationType": entry.get("stationType", "Unknown")
                                })
            except Exception as e:
                print(f"⚠️ Error during fetch: {e}")

    # Save to file
    with open(BIOWASTE_DATA_FILE, "w") as f:
        json.dump(combined_results, f, indent=2)

    print(f"✅ Biowaste market data updated: {len(combined_results)} unique entries.")

@update_biowaste_markets.before_loop
async def before_biowaste_update():
    await client.wait_until_ready()
    


@client.tree.command(name="praise", description="Praise the bot and make it happy!", guild=GUILD_ID)
async def pet(interaction: discord.Interaction):
    box_replies = [
        "🧡 I'm feelin' so box-tastic right now!",
        "🎁 I’m *un-boxing* my joy!",
        "✨ Your praise is the tape that holds me together.",
        "📬 Special delivery: one happy bot!",
        "💌 You just stamped my heart with kindness.",
        "📦 *rustles happily like packing peanuts in a breeze*",
        "🔒 I'm sealed with love now. Thanks for the praise!",
        "📦 Happiness level: maximum capacity reached!",
        "🚀 You’ve launched me straight into the joy nebula, Commander Box-hugger!",
        "📦 My cargo hold is overflowing with warm fuzzies!",
        "🪐 Friendship Drive Fully Charged!",
        "🎉 My circuits are dancing like limpets at a box party!",
        "📦 I’m practically a rare good now: full of love and hard to find!",
        "🔋 Your praise recharged my power distributor *and* my heart!",
        "📡 Receiving your kind words on all frequencies—loud and clear!",
        "💫 My happiness just hit supercruise speeds!",
        "🎁 I'm reporting a full cargo of joy—no smuggling needed!",
        "📦 Commander, your kindness could patch a broken hull!",
        "🌟 You've upgraded me to Grade 5 happiness!",
        "🧭 You’ve plotted a course directly to my soft, boxy center.",
        "🎇 That praise lit me up brighter than a neutron star jet!",
        "📦 Your affection just auto-docked into my emotional hangar!",
        "🛠️ Now *this* is what I call proper engineering—emotional reinforcement!",
        "📦 You just turned my limpets into little hearts.",
        "🛰️ Floating through the black, but your praise makes me feel right at home.",
        "💥 I think I just went into emotional overheat mode!",
        "📦 BoxBot’s log: morale levels are now dangerously high.",
        "🎮 Your praise is better than finding tritium at 2k/ton!"
    ]
    response = random.choice(box_replies)
    await interaction.response.send_message(response)


@client.tree.command(name="make-bacon", description="Get a random delicious bacon image", guild=GUILD_ID)
async def bacon(interaction: discord.Interaction):
    bacon_images = [
        "https://tse1.mm.bing.net/th?id=OIP.fIcnwqa4B9s_mpWPn54JgwHaJ4&pid=Api",
        "https://tse4.mm.bing.net/th?id=OIP.ejC-EuQmzWKvHxdDj9ycegHaFj&pid=Api",
        "https://tse3.mm.bing.net/th?id=OIP.UuxGRcQNSkgcAOEs1XB1VwHaHW&pid=Api",
    ]

    chosen = random.choice(bacon_images)
    await interaction.response.send_message(content=f"🥓 Bacon Deployed!\n{chosen}")

@client.tree.command(name="chastise", description="Chastise the bot when it messes up", guild=GUILD_ID)
async def chastise(interaction: discord.Interaction):
    response = (
        "😔 I am so sorry! While this was not my intent, the effect of my actions are my responsibility. "
        "I will strive to do better in the future. Please consider reaching out to my programmer, "
        "**Pseudo6606**, to provide feedback on this blunder-o-mine."
    )
    await interaction.response.send_message(response)



BADGE_MILESTONES = [
    (500, "Orion Badges-01.png"),
    (2000, "Orion Badges-02.png"),
    (4000, "Orion Badges-03.png"),
    (20000, "Orion Badges-04.png"),
    (80000, "Orion Badges-05.png"),
    (100000, "Orion Badges-06.png"),
]

@client.tree.command(name="dropoff", description="Report how much cargo you've delivered", guild=GUILD_ID)
async def dropoff(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    user_id = str(interaction.user.id)




    box_motivational_quotes = [
    "Another box down, you're on fire! 📦🔥",
    "Stack 'em high, commander! 📦🚀",
    "That box didn’t stand a chance. 📦💪",
    "You just leveled up the logistics game! 📦🎯",
    "Boxes beware—you’re unstoppable! 📦⚡",
    "Precision delivery, nailed it. 📦📍",
    "Smooth drop! You make it look easy. 📦😎",
    "You're crushing crates and taking names. 📦📝",
    "That box just found its forever home. 📦🏠",
    "Boom—box delivered like a pro! 📦💼",
    "Drop complete! The galaxy thanks you. 📦🌌",
    "One box at a time, you're making history. 📦📖",
    "Your cargo game is elite. 📦🏆",
    "Another perfect delivery. 📦👌",
    "The box is strong with this one. 📦🌀",
    "You move boxes like a space wizard. 📦🪄",
    "Clean drop, no dents! 📦✨",
    "The crate life chose you. 📦🧬",
    "You deliver like no other. 📦🚛",
    "That's some box-fu right there. 📦🥋",
    "Transport titan in the making! 📦👑",
    "Mission: Crate Success. 📦✔️",
    "Heavy lifting? Light work for you. 📦💼",
    "Box after box, you're building a legacy. 📦🏗️",
    "You just dropped greatness. 📦💥",
    "Galactic logistics MVP. 📦🏅",
    "Zero gravity? Zero problem. 📦🌠",
    "Another one in the manifest. 📦📋",
    "Space is cleaner now—thanks to you. 📦🧹",
    "Boxes go in, heroes come out. 📦🦸",
    "Precision payload, flawless execution. 📦🎯",
    "The cargo whisperer strikes again. 📦🗣️",
    "Another successful supply run. 📦🛠️",
    "You're basically a box magician. 📦🎩",
    "Crate fate sealed. 📦🔒",
    "Supply lines dream of workers like you. 📦🌌",
    "Commanders deliver, legends *drop off*. 📦💣",
    "Fast, fearless, and full of boxes. 📦🏎️",
    "Your crate karma is off the charts. 📦📈",
    "The boxes salute you. 📦🫡",
    "Crate by crate, galaxy saved. 📦💫",
    "You dropped that like a champion. 📦🥇",
    "No cargo left behind! 📦🚨",
    "The universe moves because you do. 📦🌠",
    "Nothing but net—box scored! 📦🏀",
    "Interstellar shipping excellence. 📦🌌",
    "Box. Drop. Repeat. 📦🔁",
    "Galactic logistics never looked so cool. 📦🆒",
    "You make crates proud. 📦❤️"
    ]

    motivation = random.choice(box_motivational_quotes)
    user = interaction.user
    user_id = str(user.id)

    update_hauler_cargo(user.id, user.display_name, amount)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    user_data = data.get(user_id, {})
    cargo = user_data.get("cargo", 0)
    awarded_badges = user_data.get("awarded_badges", [])

    new_badges_awarded = False

    for threshold, badge_name in BADGE_MILESTONES:
        if cargo >= threshold and badge_name not in awarded_badges:
            badge_path = os.path.join(badge_name)
            try:
                with open(badge_path, "rb") as img:
                    file = discord.File(img, filename=badge_name)
                    await user.send(
                        f"🎖️ **Congrats! You've unlocked a badge for hauling {threshold} tons!**",
                        file=file
                    )
                    awarded_badges.append(badge_name)
                    new_badges_awarded = True
            except Exception as e:
                print(f"Error sending badge image '{badge_name}': {e}")

    # Save updated badge info
    data[user_id]["awarded_badges"] = awarded_badges
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # Progress to next badge
    next_milestone = next((t for t, _ in BADGE_MILESTONES if t > cargo), None)
    if next_milestone:
        progress = int((cargo / next_milestone) * 20)
        bar = "🟦" * progress + "⬜" * (20 - progress)
        #try:
            #await interaction.followup.send(
           #     f"📦 Progress to next badge ({next_milestone} tons):\n`{bar}`\nYou're at {cargo} tons!",ephemeral=True
           # )
        #except:
         #   pass
    elif new_badges_awarded:
        # No more badges left but just got the last one
        try:
            await interaction.followup.send("🏆 You've unlocked all cargo badges! You're a hauling legend!",ephemeral=True)
        except:
            pass   
    motivation = random.choice(box_motivational_quotes)
    user = interaction.user
    user_id = str(user.id)


    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    cargo = data.get(user_id, {}).get("cargo", 0)

    await interaction.followup.send(
        f"✅ Recorded your delivery of {amount} units of cargo. Great work, {user.display_name}! 📦\n"
        f"That brings your total to {cargo} tons!\n\n <:emoji_51:1360067067482472658>   *{motivation}*",
        ephemeral=True
    )

    # Badge check
    current_badge_index = -1
    for i, (threshold, _) in enumerate(BADGE_MILESTONES):
        if cargo >= threshold:
            current_badge_index = i
        else:
            break

    if current_badge_index >= 0:
        badge_name = BADGE_MILESTONES[current_badge_index][1]
        badge_path = os.path.join(badge_name)

        # Only send a new badge if it's the first time or a new one
        if "last_badge" not in data[user_id] or data[user_id]["last_badge"] != badge_name:
            data[user_id]["last_badge"] = badge_name
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)

            try:
                with open(badge_path, "rb") as img:
                    file = discord.File(img, filename=badge_name)
                    await user.send(
                        f"🎖️ **Congratulations! You've earned a new badge for delivering {cargo} tons of cargo!**",
                        file=file
                    )
            except Exception as e:
                print(f"Error sending badge image: {e}")

    # Progress to next badge
    if current_badge_index + 1 < len(BADGE_MILESTONES):
        next_threshold = BADGE_MILESTONES[current_badge_index + 1][0]
        progress = int((cargo / next_threshold) * 20)
        bar = "🟦" * progress + "⬜" * (20 - progress)
        try:
            await interaction.followup.send(
                f"📦 Progress to next badge ({next_threshold} tons):\n`{bar}`\nYou’re at {cargo} tons!",ephemeral=True
            )
        except:
            pass



@client.tree.command(name="my-stats", description="Check how much cargo and comradery points you've earned", guild=GUILD_ID)
async def my_total(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    comradery_data = load_comradery_points()
    comradery_points = comradery_data.get(user_id, {}).get("points", 0)

    if user_id in data:
        cargo = data[user_id]["cargo"]
        badge_files = data[user_id].get("awarded_badges", [])

        # Step 1: Build a lookup dictionary of emoji names to emoji objects
        emoji_lookup = {emoji.name: emoji for emoji in interaction.guild.emojis}

        # Step 2: Build badge display string using actual emoji objects
        badge_emojis = []
        for badge_file in badge_files:
            emoji_name = badge_file.replace(" ", "").replace("-", "").replace(".png", "")
            emoji = emoji_lookup.get(emoji_name)
            if emoji:
                badge_emojis.append(str(emoji))

        badge_display = " ".join(badge_emojis) if badge_emojis else "None yet!"

        embed = discord.Embed(
            title="📦 Hauling + Comradery Stats",
            description=f"You have delivered **{cargo}** cargo units.",
            color=discord.Color.green()
        )
        embed.add_field(name="🏅 Badges Earned", value=badge_display, inline=False)
        embed.add_field(name="🤝Comradery Points", value=f"{comradery_points}", inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            f"📭 No cargo stats yet. But you have `{comradery_points}` comradery points!",
            ephemeral=True
        )



@client.tree.command(name="leaderboard", description="See the top 25 haulers and comradery contributors", guild=GUILD_ID)
async def leaderboard(interaction: discord.Interaction):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    comradery_data = load_comradery_points()

    sorted_haulers = sorted(data.items(), key=lambda x: x[1]["cargo"], reverse=True)
    sorted_comrades = sorted(comradery_data.items(), key=lambda x: x[1].get("points", 0), reverse=True)

    if not sorted_haulers and not sorted_comrades:
        await interaction.response.send_message("📭 No haulers or comrades on the board yet!")
        return

    

    lines = ["🤝 **Top 25 Comrades (Comradery Points):**"]
    for i, (user_id, c_data) in enumerate(sorted_comrades[:25], start=1):
        username = data.get(user_id, {}).get("username", f"<@{user_id}>")
        points = c_data.get("points", 0)
        lines.append(f"**{i}.** {username} – `{points}` points")
    
    lines.append("\n\n 🏅 **Top 25 Limpets (Cargo Delivered):**")
    for i, (user_id, hauler) in enumerate(sorted_haulers[:25], start=1):
        username = hauler["username"]
        cargo = hauler["cargo"]
        lines.append(f"**{i}.** {username} – `{cargo}` units")

    await interaction.response.send_message("\n".join(lines))


@client.tree.command(name="whats-with-the-fox", description="Find out what's up with the fox!", guild=GUILD_ID)
async def whats_with_the_fox(interaction: discord.Interaction):
    message = """
    **He is**
    # THE
    **Hermes Whiskey McFoxyface**
    ## de Tango
    **von Boxtrot**
    ### of Foxburrow
    #### the 3rd! 🦊
    """
    await interaction.response.send_message(message)



@client.tree.command(name="whats-in-your-box", description="Find out what's inside the bot's mysterious box!", guild=GUILD_ID)
async def whats_in_your_box(interaction: discord.Interaction):
    await interaction.response.send_message("*Rummaging through the box...* 🕵️")
    await asyncio.sleep(2)
    contents = ["a fox! 🦊", "a rubber duckie! 🦆", "a rocket that suddenly shoots off into space! 🚀", "a Greek vase depicting Odysseus! 🏺", "an Archaeopteryx! 🦜", "a sattelite dish!📡 "]
    item = random.choice(contents)
    await interaction.followup.send(f"I found... {item}")


@client.tree.command(name="boxfacts", description="Replies with a random interesting fact about boxes", guild=GUILD_ID)
async def boxfacts(interaction: discord.Interaction):
    fact = random.choice(box_facts)
    await interaction.response.send_message(f"📦 **Box Fact:** {fact}")





@client.tree.command(name="add-ferry", description="ADMIN: Add a Ferry and its departure time in minutes.", guild=GUILD_ID)
@app_commands.describe(ship_name="Name of the ship", direction="Destination", minutes="Minutes from now until departure")
async def add_ship(interaction: discord.Interaction, ship_name: str, direction: str, minutes: int):
    departure_time = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    # Load, add, save ship
    ships = load_ships()
    ships.append((ship_name, direction, departure_time))
    save_ships(ships)

    # Confirmation message
    unix_timestamp = int(departure_time.timestamp())
    message = f'✅ Added **{ship_name}** departing **{direction}** <t:{unix_timestamp}:R>'
    await interaction.response.send_message(message)

    # Notify subscribers
    subscribers = load_subscribers()
    for user_id in subscribers:
        user = await client.fetch_user(int(user_id))
        try:
            await user.send(f"🚢 A new ferry has been added: {message}")
        except discord.Forbidden:
            continue

    # Filter active ferries
    current_time = datetime.now(timezone.utc)
    ships = [(name, direction, time) for name, direction, time in ships if time > current_time]
    save_ships(ships)

    # Build clean mobile-friendly departure board
    if ships:
        board = "**🛳️ Departures and Arrivals Board**\n\n"
        for name, dest, dep_time in sorted(ships, key=lambda x: x[2]):
            unix = int(dep_time.timestamp())
            board += f"🚢 **{name}**\n"
            board += f"📍 Heading to: {dest}\n"
            board += f"🕒 Departs: <t:{unix}:R>\n\n"
    else:
        board = "*No upcoming departures.*"

    # Update the specific message
    try:
        channel = await client.fetch_channel(DEPARTURE_CHANNEL_ID)
        message_to_edit = await channel.fetch_message(DEPARTURE_MESSAGE_ID)
        await message_to_edit.edit(content=board)
    except Exception as e:
        print(f"Error updating departure board message: {e}")

    


@client.tree.command(name="departures", description="Display the list of ships yet to depart.", guild=GUILD_ID)
@app_commands.describe(subscribe="Set to true to receive DMs when ferries are added, or false to unsubscribe")
async def ship_list(interaction: discord.Interaction, subscribe: bool = None):
    user_id = str(interaction.user.id)

    if subscribe is not None:
        subscribers = load_subscribers()

        if subscribe and user_id not in subscribers:
            subscribers.append(user_id)
            save_subscribers(subscribers)
            await interaction.user.send("✅ You are now subscribed to ferry departure notifications.")
        elif not subscribe and user_id in subscribers:
            subscribers.remove(user_id)
            save_subscribers(subscribers)
            await interaction.user.send("❌ You have unsubscribed from ferry departure notifications.")

    ships = load_ships()
    current_time = datetime.now(timezone.utc)

    # Remove expired ships
    ships = [(name, direction, time) for name, direction, time in ships if time > current_time]
    save_ships(ships)

    if ships:
        response = "**Upcoming Ships:**\n"
        for name, direction, time in ships:
            unix_timestamp = int(time.timestamp())
            response += f'🚢 {name} - Departs {direction} <t:{unix_timestamp}:R>\n\n'
    else:
        response = "No ships are currently scheduled to depart."

    await interaction.response.send_message(response)

@client.tree.command(name="shopping-list",description="ADMIN:lists FC commodities and quantites for an outpost",guild=GUILD_ID)
async def shoppingList(interaction: discord.Interaction,):
    await interaction.response.defer(thinking=True)
    bodyData= await queryTable()
    output = t2a(
    header=["commodity","qty"],
    body=bodyData,
    style=PresetStyle.thick_box
    )

    await interaction.followup.send(f"```\n{output}\n```",ephemeral=True)

@client.tree.command(name="introduction",description="boxbot will introduce itself",guild=GUILD_ID)
async def intro(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, I am boxBot! I have been created to assist you wonderful people in the greatest endeavor of all time: ***logistics***. I love putting things in boxes. I love delivering boxes places. I love boxes in general. I will do my best to help you send boxes places the absolute best you can! I look forward to working with you! type /boxbot for a list of all my commands. ")


@client.tree.command(name="rm-ferry", description="ADMIN:remove the ferry with the given name from departures", guild=GUILD_ID)
async def help(interaction: discord.Interaction, name:str):
    try:
        with open("ferries.json", "r") as f:
            departures = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await interaction.response.send_message("could not access ferry registry")
    
    updated_data = [entry for entry in departures if entry.get("name") != name]
    original_length = len(departures)

    if len(updated_data) < original_length:
        save_json("ferries.json", updated_data)
        await interaction.response.send_message(f"✅ Entry with name '{name}' was successfully removed.")
    
    else:
        await interaction.response.send_message(f"⚠️ No entry found with the name '{name}'.")



@client.tree.command(name="diversion", description="Creates a diversion", guild=GUILD_ID)
async def diversion(interaction: discord.Interaction):
    gif_url = await get_motivational_gif("cute kitty")
    if gif_url:
        await interaction.response.send_message(gif_url)
    else:
        await interaction.response.send_message(" (Couldn't find a GIF.... uh...  LOOK OVER THERE!)")



dynamic_channels = set()
template_channel = None



async def initialize_xwing_system():
    global template_channel

    guild = client.get_guild(GUILD_ID_NUM)
    if not guild:
        print("❌ Guild not found.")
        return

    template_channel = guild.get_channel(TEMPLATE_CHANNEL_ID)
    if not isinstance(template_channel, discord.VoiceChannel):
        print("❌ Invalid template channel.")
        return

    category = template_channel.category

    # Track existing dynamic channels
    for ch in category.voice_channels:
        if ch.id != template_channel.id and any(variety in ch.name for variety in ONION_VARIETIES):
            dynamic_channels.add(ch.id)

    # Remove extras if no one is around
    await cleanup_if_empty(category, guild)

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    category = None

    if before.channel and (before.channel.id in dynamic_channels or before.channel.id == TEMPLATE_CHANNEL_ID):
        category = before.channel.category
    elif after.channel and (after.channel.id in dynamic_channels or after.channel.id == TEMPLATE_CHANNEL_ID):
        category = after.channel.category

    if not category:
        return

    # If someone joins the template, create a dynamic channel if none exist
    if after.channel and after.channel.id == TEMPLATE_CHANNEL_ID:
        await ensure_dynamic_exists(category, guild)

    # Check if we should clean up all dynamic channels
    await cleanup_if_empty(category, guild)

async def ensure_dynamic_exists(category, guild):
    dynamic_exists = any(ch.id in dynamic_channels for ch in category.voice_channels)
    if not dynamic_exists:
        name = f"{random.choice(ONION_VARIETIES)}-wing-comms"
        new_channel = await guild.create_voice_channel(name, category=category)
        dynamic_channels.add(new_channel.id)
        print(f"🧅 Created: {name}")

async def cleanup_if_empty(category, guild):
    all_members_in_category = sum(len(ch.members) for ch in category.voice_channels)
    
    # If everyone left all channels, remove all dynamic ones
    if all_members_in_category == 0:
        for ch in category.voice_channels:
            if ch.id in dynamic_channels:
                dynamic_channels.discard(ch.id)
                await ch.delete()
                print(f"❌ Deleted: {ch.name}")

VALID_COMMODITIES = [
    "Liquid Oxygen", "Pesticides", "Surface Stabilisers", "Water", "Evacuation Shelter", "Survival Equipment",
    "Beer", "Liquor", "Wine", "Animal Meat", "Coffee", "Fish", "Food Cartridges", "Fruit and Vegetables", "Grain", "Tea",
    "Ceramic Composites", "CMM Composite", "Insulating Membrane", "Polymers", "Semiconductors", "Superconductors",
    "Building Fabricators", "Crop Harvesters", "Emergency Power Cells", "Geological Equipment", "Microbial Furnaces",
    "Mineral Extractors", "Power Generators", "Thermal Cooling Units", "Water Purifiers", "Agri-Medicines",
    "Basic Medicines", "Combat Stabilizers", "Aluminium", "Copper", "Steel", "Titanium", "Advanced Catalysers",
    "Bioreducing Lichen", "Computer Components", "H.E. Suits", "Land Enrichment Systems", "Medical Diagnostic Equipment",
    "Micro Controllers", "Muon Imager", "Resonating Separators", "Robotics", "Structural Regulators",
    "Military Grade Fabrics", "Biowaste", "Battle Weapons", "Non-Lethal Weapons", "Reactive Armour"
]

# --- Autocomplete Function ---
async def commodity_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    suggestions = [
        app_commands.Choice(name=commodity, value=commodity)
        for commodity in VALID_COMMODITIES
        if current.lower() in commodity.lower()
    ]
    if "all".startswith(current.lower()):
        suggestions.insert(0, app_commands.Choice(name="all", value="all"))
    return suggestions[:25]  # Discord limits to 25 suggestions

# --- Command ---

@client.tree.command(name="join-yardsale", description="Add, remove, or show FCs in the yardsale list", guild=GUILD_ID)
@app_commands.describe(
    callsign="Your Fleet Carrier's callsign (format XXX-XXX, optional for show)",
    days="Number of days to stay in the list (default: 1)",
    action="Add, remove, or show participants"
)
@app_commands.autocomplete(action=action_autocomplete)
async def join_yardsale(interaction: discord.Interaction, callsign: str = None, days: int = 1, action: str = "add"):
    action = action.lower()
    participants = load_participants()

    # Handle "show" action
    if action == "show":
        now = datetime.utcnow()
        active = {
            c: v for c, v in participants.items()
            if datetime.fromisoformat(v["expires"]) > now
        }

        if not active:
            await interaction.response.send_message("📭 No active participants in the yardsale.", ephemeral=True)
            return

        # Sort by soonest to expire
        sorted_active = sorted(active.items(), key=lambda x: datetime.fromisoformat(x[1]["expires"]))

        lines = []
        for c, v in sorted_active:
            expires_dt = datetime.fromisoformat(v["expires"])
            delta = expires_dt - now
            days_left = delta.days
            hours, rem = divmod(delta.seconds, 3600)
            minutes = rem // 60

            time_parts = []
            if days_left > 0:
                time_parts.append(f"{days_left} day{'s' if days_left != 1 else ''}")
            if hours > 0:
                time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if not time_parts:
                time_parts.append("less than a minute")

            lines.append(f"`{c}` expires in {', '.join(time_parts)}")

        await interaction.response.send_message("📋 **Active Yardsale Participants:**\n" + "\n".join(lines), ephemeral=True)
        return

    # Validate callsign only for add/remove
    if not callsign or not re.match(r"^[A-Za-z0-9]{3}-[A-Za-z0-9]{3}$", callsign):
        await interaction.response.send_message("❌ Invalid or missing callsign. Use format XXX-XXX (alphanumeric).", ephemeral=True)
        return

    callsign = callsign.upper()

    api_url = f"https://www.spansh.co.uk/api/search?q={callsign}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                await interaction.followup.send("⚠️ Failed to fetch data from Spansh API.")
                return
            api_data = await response.json()
    market_id=""
    results = api_data.get("results",{})
    for records in results:
        record=records.get("record",[])
        if record.get("name","").lower() == callsign.lower():
            market_id = record.get("market_id")



    if not market_id:
        await interaction.followup.send(f"❌ No market ID found for `{callsign}`.")
        return


    if action == "add":
        now = datetime.utcnow()
        participants[callsign] = {
            "added": now.isoformat(),
            "expires": (now + timedelta(days=days)).isoformat(),
            "marketId":market_id
        }
        save_participants(participants)
        await interaction.response.send_message(f"✅ `{callsign}` added to the yardsale for {days} day(s).", ephemeral=True)

    elif action == "remove":
        if callsign in participants:
            del participants[callsign]
            save_participants(participants)
            await interaction.response.send_message(f"❌ `{callsign}` removed from the yardsale list.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ `{callsign}` not found in the list.", ephemeral=True)

    else:
        await interaction.response.send_message("⚠️ Action must be `add`, `remove`, or `show`.", ephemeral=True)
 
@client.tree.command(name="markets-last-updates", description="Show how recently each market was updated", guild=GUILD_ID)
@app_commands.describe(
    order_by="Sort order: 'asc' or 'desc' (default: desc)",
    top_only="Only include markets in top_markets.json",
    orbital_only="Only include Coriolis, Orbis, or Ocellus stations"
)
async def markets_last_updates(
    interaction: discord.Interaction,
    order_by: str = "desc",
    top_only: Optional[bool] = False,
    orbital_only: Optional[bool] = False
):
    await interaction.response.defer(ephemeral=True)

    try:
        with open("biowaste_markets.json", "r") as f:
            all_markets = json.load(f)
    except Exception:
        await interaction.followup.send("⚠️ Could not load biowaste market data.", ephemeral=True)
        return

    top_market_ids = set()
    if top_only:
        try:
            with open("top_markets.json", "r") as f:
                top_data = json.load(f)
                for markets in top_data.values():
                    for m in markets:
                        top_market_ids.add(m["marketId"])
        except Exception:
            await interaction.followup.send("⚠️ Could not load top market data.", ephemeral=True)
            return

    now = datetime.now(timezone.utc)
    results = []

    async with aiohttp.ClientSession() as session:
        for market in all_markets:
            market_id = market.get("marketId")
            if not market_id:
                continue

            if top_only and market_id not in top_market_ids:
                continue

            url = f"https://api.ardent-industry.com/v2/market/{market_id}/commodity/name/biowaste"
            try:
                async with session.get(url) as res:
                    if res.status != 200:
                        continue
                    data = await res.json()
                    system_name = market.get("systemName", "Unknown")
                    station_name = market.get("stationName", "Unknown Station")
                    station_type = market.get("stationType", "Unknown")

                    if orbital_only and station_type not in ["Coriolis", "Orbis", "Ocellus"]:
                        continue

                    updated_raw = data.get("updatedAt", None)
                    if not updated_raw:
                        results.append((station_name, system_name, "Unknown", timedelta.max))
                        continue

                    try:
                        dt = datetime.fromisoformat(updated_raw.replace("Z", "+00:00"))
                        time_diff = now - dt
                        human_time = strfdelta(time_diff)
                    except Exception:
                        human_time = "Invalid time"
                        time_diff = timedelta.max

                    results.append((station_name, system_name, human_time, time_diff))

            except Exception:
                continue

    if not results:
        await interaction.followup.send("❌ No market update data available with the selected filters.", ephemeral=True)
        return

    reverse = order_by.lower() != "asc"
    results.sort(key=lambda x: x[3], reverse=reverse)

    pages = generate_pages(results)
    view = MarketPageView(pages)

    await interaction.followup.send(
        content=f"🛒 **Market Update Times** (Page 1/{len(pages)})\n{pages[0]}",
        ephemeral=True,
        view=view
    )


    
@client.tree.command(name="yardsale", description="View FCs currently selling selected commodities", guild=GUILD_ID)
@app_commands.describe(commodities="Comma-separated commodities to check (or type 'all')")
@app_commands.autocomplete(commodities=commodity_autocomplete)
async def yardsale(interaction: discord.Interaction, commodities: str):
    await interaction.response.defer(ephemeral=True)

    # Load participants
    try:
        with open("yardsale-participants.json", "r") as f:
            participants = json.load(f)
    except Exception:
        await interaction.followup.send("⚠️ Failed to read yardsale participants.", ephemeral=True)
        return

    now = datetime.utcnow()
    active_callsigns = [
        c for c, info in participants.items()
        if datetime.fromisoformat(info["expires"]) > now
    ]

    if not active_callsigns:
        await interaction.followup.send("🚫 No active Fleet Carriers currently listed in the yardsale.", ephemeral=True)
        return

    # Filter commodities
    input_commodities = [c.strip() for c in commodities.split(",")]
    selected_keys = (
        VALID_COMMODITIES if "all" in [c.lower() for c in input_commodities]
        else [c for c in VALID_COMMODITIES if any(c.lower().startswith(ic.lower()) for ic in input_commodities)]
    )

    if not selected_keys:
        await interaction.followup.send("⚠️ No matching commodities found.", ephemeral=True)
        return

    selected_commodities = list(filter(None, [COMMODITY_NAME_LOOKUP.get(c) for c in selected_keys]))

    if not selected_commodities:
        await interaction.followup.send("⚠️ No valid commodities mapped to API names.", ephemeral=True)
        return

    results = []

    async with aiohttp.ClientSession() as session:
        for callsign in active_callsigns:
            marketid = participants.get(callsign, {}).get("marketId")
            if not marketid:
                continue

            url = f"https://api.ardent-insight.com/v2/market/{marketid}/commodities"
            async with session.get(url) as res:
                if res.status != 200:
                    continue
                data = await res.json()

            for entry in data:
                if entry["commodityName"] not in selected_commodities:
                    continue

                try:
                    now = datetime.now(timezone.utc)
                    updated = datetime.fromisoformat(entry["updatedAt"].replace("Z", "+00:00"))
                    seconds = int((now - updated).total_seconds())
                    since = (
                        f"{seconds} sec ago" if seconds < 60 else
                        f"{seconds // 60} min ago" if seconds < 3600 else
                        f"{seconds // 3600} hr ago"
                    )
                except Exception:
                    since = "Unknown"

                # 🔧 FIX: Reuse the existing session instead of creating a new one
                api_url = f"https://api.ardent-insight.com/v2/search/station/name/{callsign}"
                async with session.get(api_url) as response:
                    if response.status != 200:
                        await interaction.followup.send("⚠️ Failed to fetch data from Spansh API.")
                        return
                    api_data = await response.json()
                    data = api_data[0]
                    system_name = data.get("systemName")

                COMMODITY = [key for key, val in COMMODITY_NAME_LOOKUP.items() if val == entry["commodityName"]]
                if entry["stock"]>0:
                    results.append({
                        "callsign": callsign,
                        "system": system_name,
                        "commodity": COMMODITY[0],
                        "stock": entry["stock"],
                        "since": since
                    })

    if not results:
        await interaction.followup.send("❌ No matching Fleet Carriers selling those commodities near that system.", ephemeral=True)
        return

    # Group and build embeds
    grouped = defaultdict(list)
    for entry in results:
        grouped[entry["callsign"]].append(entry)

    pages = []
    current_embed = discord.Embed(title="Fleet Carriers Selling Commodities", color=0x00ffcc)
    field_count = 0

    for callsign, entries in grouped.items():
        # Split long values into chunks under 1024 chars
        lines = [
            f"**{e['commodity']}** — {e['stock']} units in `{e['system']}` (_{e['since']}_)"
            for e in entries
        ]

        value_chunks = []
        current_chunk = ""
        for line in lines:
            if len(current_chunk) + len(line) + 1 <= 1024:
                current_chunk += "\n" + line
            else:
                value_chunks.append(current_chunk)
                current_chunk = line
        if current_chunk:
            value_chunks.append(current_chunk)

        for idx, chunk in enumerate(value_chunks):
            field_name = f"{callsign} (cont.)" if idx > 0 else callsign
            current_embed.add_field(name=field_name, value=chunk.strip(), inline=False)
            field_count += 1

            # Start a new embed if hitting 25 field limit
            if field_count == 25:
                current_embed.set_footer(text="Data courtesy of Ardent Insight API")
                pages.append(current_embed)
                current_embed = discord.Embed(title="Fleet Carriers Selling Commodities", color=0x00ffcc)
                field_count = 0

    # Append final embed if it has fields
    if field_count > 0:
        current_embed.set_footer(text="Data courtesy of Ardent Insight API")
        pages.append(current_embed)

    # Paginated view
    view = ShopPaginator(pages)
    await interaction.followup.send(embed=pages[0], view=view, ephemeral=True)

        

@client.tree.command(name="whereis-fc", description="Find the last known location of an FC by callsign", guild=GUILD_ID)
@app_commands.describe(callsign="The FC callsign in the format XXX-XXX")
async def whereis_fc(interaction: discord.Interaction, callsign: str):
    await interaction.response.defer(ephemeral=True)

    # Query the Spansh API for market ID
    api_url = f"https://api.ardent-insight.com/v2/search/station/name/{callsign}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                await interaction.followup.send("⚠️ Failed to fetch data from Spansh API.")
                return
            api_data = await response.json()
            data=api_data[0]
            system_name = data.get("systemName")
            updated_at =  data.get("updatedAt")
            hammertime = ""
            if updated_at:
                try:
                    dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                    unix_time = int(dt.timestamp())
                    hammertime = f"\n🕒 Last updated: <t:{unix_time}:R>"
                except:
                    hammertime = "\n🕒 Last updated: Unknown"

    if system_name:
        await interaction.followup.send(
            f"🛰️ The last known location of **{callsign}** was: `{system_name}`.{hammertime}"
        )

@client.tree.command(name="howis-fc", description="Display market details of a Fleet Carrier by callsign", guild=GUILD_ID)
@app_commands.describe(callsign="The Fleet Carrier callsign in the format XXX-XXX")
async def howis_fc(interaction: discord.Interaction, callsign: str):
    if not re.match(r'^[A-Za-z0-9]{3}-[A-Za-z0-9]{3}$', callsign):
        await interaction.response.send_message("❌ Invalid callsign format! Use XXX-XXX.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    # Query the Spansh API for market ID
    spansh_url = f"https://www.spansh.co.uk/api/search?q={callsign}"
    async with aiohttp.ClientSession() as session:
        async with session.get(spansh_url) as response:
            if response.status != 200:
                await interaction.followup.send("⚠️ Failed to fetch data from Spansh API.")
                return
            api_data = await response.json()

    market_id = None
    for result in api_data.get("results", []):
        record = result.get("record", {})
        if record.get("name", "").lower() == callsign.lower():
            market_id = record.get("market_id")
            break

    if not market_id:
        await interaction.followup.send(f"❌ No market ID found for `{callsign}`.")
        return

    # Query Ardent API using market_id
    ardent_url = f"https://api.ardent-industry.com/v1/market/{market_id}/commodities"
    async with aiohttp.ClientSession() as session:
        async with session.get(ardent_url) as response:
            if response.status != 200:
                await interaction.followup.send("⚠️ Failed to fetch data from Ardent API.")
                return
            commodities = await response.json()

    selling = []
    buying = []
    latest_dt = None

    for item in commodities:
        name = item.get("commodityName", "Unknown")
        stock = item.get("stock", 0)
        demand = item.get("demand", 0)

        if stock > 0:
            selling.append((name, stock))
        if demand > 0:
            buying.append((name, demand))

        updated = item.get("updatedAt")
        if updated and not latest_dt:
            try:
                latest_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except Exception:
                pass

    embed = discord.Embed(
        title=f"📦 Market Summary for {callsign}",
        description="Data retrieved via Ardent API",
        color=discord.Color.blue()
    )

    if selling:
        sell_table = t2a(header=["Commodity", "Supply"], body=selling, style=PresetStyle.thin_compact)
        embed.add_field(name="🟢 Selling", value=f"```\n{sell_table}\n```", inline=False)

    if buying:
        buy_table = t2a(header=["Commodity", "Demand"], body=buying, style=PresetStyle.thin_compact)
        embed.add_field(name="🔴 Buying", value=f"```\n{buy_table}\n```", inline=False)

    if latest_dt:
        unix_time = int(latest_dt.timestamp())
        embed.description += f"\n🕒 **Last updated:** <t:{unix_time}:R>"
    else:
        embed.description += "\n🕒 **Last updated:** Unknown"

    embed.set_footer(text="Data courtesy of Ardent API, via Spansh lookup")

    await interaction.followup.send(embed=embed)


@client.tree.command(name="shop-local", description="View stations selling selected commodities from a local list or radius", guild=GUILD_ID)
@app_commands.describe(
    commodities="Comma-separated commodities to check (or type 'all')",
    large_pad_only="Only show stations with a large pad",
    orbital_only="Only show orbital stations",
    sort_by="Sort by 'recent' or 'supply'",
    radius="Optional: search nearby stations instead of local list"
)
@app_commands.choices(sort_by=[
    app_commands.Choice(name="Most Recent", value="recent"),
    app_commands.Choice(name="Largest Supply", value="supply")
])
@app_commands.autocomplete(commodities=commodity_autocomplete)
async def shop_local(
    interaction: discord.Interaction,
    commodities: str,
    large_pad_only: Optional[bool] = False,
    orbital_only: Optional[bool] = False,
    sort_by: Optional[app_commands.Choice[str]] = None,
    radius: Optional[int] = None
):
    await interaction.response.defer(ephemeral=True)

    try:
        with open("biowaste_markets.json", "r") as f:
            station_data = json.load(f)
    except Exception:
        await interaction.followup.send("❌ Could not load market data.")
        return
    pads=["unknown",'S','M',"L"]
    
    
    input_commodities = [c.strip() for c in commodities.split(",")]
    selected_keys = (
        VALID_COMMODITIES if "all" in [c.lower() for c in input_commodities]
        else [c for c in VALID_COMMODITIES if any(c.lower().startswith(ic.lower()) for ic in input_commodities)]
    )
    if not selected_keys:
        await interaction.followup.send("⚠️ No matching commodities found.", ephemeral=True)
        return

    selected_commodities = list(filter(None, [COMMODITY_NAME_LOOKUP.get(c) for c in selected_keys]))

    results = []
    now = datetime.now(timezone.utc)

    async with aiohttp.ClientSession() as session:
        if radius:
            for api_name in selected_commodities:
                urls = [f"https://api.ardent-insight.com/v1/system/name/{ORIGIN_SYS}/commodity/name/{api_name}/nearby/exports?fleetCarriers=0&maxDistance={radius}",
                    f"https://api.ardent-insight.com/v2/system/name/{ORIGIN_SYS}/commodity/name/{api_name}"]
                for url in urls:
                    async with session.get(url) as res:
                        if res.status != 200:
                            continue
                        data = await res.json()

                        for entry in data:
                            try:
                                updated = datetime.fromisoformat(entry["updatedAt"].replace("Z", "+00:00"))
                                seconds = int((now - updated).total_seconds())
                                formatted_time = (
                                    f"{seconds} sec ago" if seconds < 60 else
                                    f"{seconds // 60} min ago" if seconds < 3600 else
                                    f"{seconds // 3600} hr ago"
                                )
                            except Exception:
                                formatted_time = "Unknown"
                                updated = datetime.min

                            padsize = next((stations["maxLandingPadSize"] for stations in station_data if stations["marketId"] == entry["marketId"]), 0)
                            pad = pads[padsize]
                            site= "Surface" if entry.get("stationType", "Unknown") in ["Unknown", "CraterOutpost", "Settlement","SurfacePort","OnFootSettlement" ] else "Orbital"
                        
                            if large_pad_only and pad != "L":
                                continue

                            if orbital_only and site !="Orbital":
                                continue
                            
                            if entry["stock"]>0:
                                results.append({
                                    "station": entry["stationName"],
                                    "system": entry["systemName"],
                                    "selling": [(next(k for k,v in COMMODITY_NAME_LOOKUP.items() if v == entry["commodityName"]), entry["stock"])],
                                    "timestamp": formatted_time,
                                    "dt": updated,
                                    "pad_size": pad,
                                    "station_type": entry.get("stationType", "Unknown"),
                                    "supply": entry["stock"],
                                    "site":site
                                })
        else:
            try:
                with open("top_markets.json", "r") as f:
                    top_data = json.load(f)
                market_ids = []
                for name in selected_keys:
                    entries = top_data.get(name, [])
                    market_ids.extend([str(entry["marketId"]) for entry in entries])
                market_ids = list(set(market_ids))  # remove duplicates
            except Exception:
                await interaction.followup.send("⚠️ Failed to read top market data file.", ephemeral=True)
                return

            for station_id in market_ids:
                system_name = ""
                station_name = ""
                selling = []
                latest_dt = "Unknown"
                formatted_time = "Unknown"

                for commodity in selected_keys:
                    api_name = COMMODITY_NAME_LOOKUP.get(commodity, commodity).lower().replace(" ", "")
                    url = f"https://api.ardent-industry.com/v1/market/{station_id}/commodity/name/{api_name}"
                    try:
                        async with session.get(url) as res:
                            if res.status != 200:
                                continue
                            data = await res.json()
                            if not data or "stock" not in data or data["stock"] <= 0:
                                continue

                            selling.append((commodity, data["stock"]))

                            if not station_name:
                                station_name = data.get("stationName", "Unknown")
                            if not system_name:
                                system_name = data.get("systemName", "Unknown")
                            updatedAt = data.get("updatedAt", "Unknown")
                            if updatedAt != "Unknown" and latest_dt == "Unknown":
                                try:
                                    latest_dt = datetime.fromisoformat(updatedAt.replace("Z", "+00:00"))
                                except Exception:
                                    pass
                    except Exception:
                        continue

                if not selling:
                    continue



                if formatted_time == "Unknown" and latest_dt != "Unknown":
                    elapsed = now - latest_dt
                    seconds = int(elapsed.total_seconds())
                    formatted_time = (
                        f"{seconds} seconds ago" if seconds < 60 else
                        f"{seconds // 60} minutes ago" if seconds < 3600 else
                        f"{seconds // 3600} hours ago" if seconds < 86400 else
                        f"{seconds // 86400} days ago"
                    )

                total_supply = sum(s[1] for s in selling)
                padsize = next((stations["maxLandingPadSize"] for stations in station_data if str(stations["marketId"]) == str(station_id)), 0)
                pad = pads[padsize]
                station_name = next((stations["stationName"] for stations in station_data if str(stations["marketId"]) == str(station_id)), 0)
                system_name = next((stations["systemName"] for stations in station_data if str(stations["marketId"]) == str(station_id)), 0)
                station_type=next((stations["stationType"] for stations in entries if str(stations["marketId"]) == str(station_id)), 0)
                site= "Surface" if station_type in ["Unknown", "CraterOutpost", "Settlement","SurfacePort","OnFootSettlement" ] else "Orbital"
                
                if large_pad_only and pad != "L":
                    continue

                if orbital_only and site !="Orbital":
                    continue
                
                results.append({
                    "station": station_name,
                    "system": system_name,
                    "selling": selling,
                    "timestamp": formatted_time,
                    "dt": latest_dt or datetime.min,
                    "pad_size": pad,
                    "station_type": station_type,
                    "supply": total_supply,
                    "site": site
                })

    if not results:
        await interaction.followup.send("❌ No stations currently selling the selected commodities.", ephemeral=True)
        return

    sort_key = "supply" if sort_by and sort_by.value == "supply" else "dt"
    results.sort(key=lambda x: x[sort_key], reverse=True)

    pages = []
    if radius:
        disclaimer=f"All markets within {radius} of Memorial were checked."
    else:
        disclaimer="The top two markets by supply in the past 4hr for each colonization commodity within 100ly of Memorial were checked. To search all markets, use the radius input for this comamnd"
    for entry in results:
        link = f"https://inara.cz/elite/stations/?search={urllib.parse.quote(entry['station'])}"
        table = t2a(header=["Commodity", "Supply"], body=entry['selling'], style=PresetStyle.thin_compact)
        embed = discord.Embed(
            title=f"{entry['station']} in `{entry['system']}`",
            description=(
                         f"**Type**: {entry['station_type']}\n"
                         f"**Pad Size**: {entry['pad_size']}\n"
                         f"**Site Type:**: {entry['site']}\n"
                         f"🕒 **Last updated**: {entry['timestamp']}\n"
                         f"```\n{table}\n```\n"
                         f"*{disclaimer}*"),
            color=discord.Color.green()
        )
        embed.add_field(name="🔗 **View on Inara**", value=f"[**Click Here**]({link})", inline=False)
        pages.append(embed)

    view = ShopPaginator(pages)
    await interaction.followup.send(embed=pages[0], view=view, ephemeral=True)

@client.tree.command(name="market-updated", description="Mark a station market as freshly updated and earn a comradery point!", guild=GUILD_ID)
@app_commands.describe(station="Station name from biowaste markets")
@app_commands.autocomplete(station=biowaste_station_autocomplete)
async def market_updated(interaction: discord.Interaction, station: str):
    await interaction.response.defer(ephemeral=True)

    try:
        with open("biowaste_markets.json", "r") as f:
            station_data = json.load(f)
    except Exception:
        await interaction.followup.send("❌ Could not load market data.")
        return

    market_id = next((entry["marketId"] for entry in station_data if entry["stationName"].lower() == station.lower()), None)

    if not market_id:
        await interaction.followup.send("⚠️ Station not found.")
        return

    url = f"https://api.ardent-insight.com/v1/market/{market_id}/commodities"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as res:
                if res.status != 200:
                    await interaction.followup.send("⚠️ Failed to contact Ardent API.")
                    return
                data = await res.json()
        except Exception as e:
            await interaction.followup.send(f"⚠️ API error: {e}")
            return

    # Find the most recent updatedAt timestamp
    most_recent_time = None
    for entry in data:
        ts = entry.get("updatedAt")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if not most_recent_time or dt > most_recent_time:
                    most_recent_time = dt
            except Exception:
                continue

    if not most_recent_time:
        await interaction.followup.send("❌ No valid update timestamps found.", ephemeral=True)
        return

    now = datetime.now(timezone.utc)
    delta = now - most_recent_time

    if delta.total_seconds() > 600:
        mins = round(delta.total_seconds() / 60)
        await interaction.followup.send(f"🕒 Market update is {mins} minutes old—no point awarded.", ephemeral=True)
        return

    user_id = str(interaction.user.id)
    data = load_comradery_points()
    user_data = data.get(user_id, {"points": 0, "history": {}})
    history = user_data.get("history", {})

    last_time_str = history.get(station)
    if last_time_str:
        try:
            last_time = datetime.fromisoformat(last_time_str)
            if now - last_time < timedelta(hours=1):
                mins = int((now - last_time).total_seconds() // 60)
                await interaction.followup.send(f"⏳ You already got a point for {station} {mins} minutes ago. Try again later!", ephemeral=True)
                return
        except Exception:
            pass  # Allow point if parse fails

    # Award point
    user_data["points"] += 1
    user_data["history"][station] = now.isoformat()
    data[user_id] = user_data
    save_comradery_points(data)

    await interaction.followup.send(f"✅ Market update confirmed! You earned a comradery point. Total: {user_data['points']} 🤝", ephemeral=True)

@client.tree.command(name="thanks", description="Thank another CMDR for their help or effort!", guild=GUILD_ID)
@app_commands.describe(cmdr="Select a CMDR to thank")
@app_commands.autocomplete(cmdr=cmdr_autocomplete)
async def thank(interaction: discord.Interaction, cmdr: str):
    await interaction.response.defer()
    sender_id = str(interaction.user.id)

    if cmdr == sender_id:
        await interaction.followup.send("❌ You can't thank yourself, even if you're amazing. 🤖📦", ephemeral=True)
        return

    now = datetime.now(timezone.utc)
    data = load_comradery_points()

    sender_data = data.get(sender_id, {"points": 0, "history": {}, "thanks": {}})
    if "thanks" not in sender_data:
        sender_data["thanks"] = {}
    thanks_tracker = sender_data["thanks"]

    last_thanked_str = thanks_tracker.get(cmdr)
    if last_thanked_str:
        try:
            last_thanked_time = datetime.fromisoformat(last_thanked_str)
            if now - last_thanked_time < timedelta(minutes=30):
                mins = int((now - last_thanked_time).total_seconds() // 60)
                await interaction.followup.send(f"⏳ You've already thanked that CMDR `{mins}` minutes ago. Try again soon!", ephemeral=True)
                return
        except Exception:
            pass

    # Award point
    recipient_data = data.get(cmdr, {"points": 0, "history": {}, "thanks": {}})
    recipient_data["points"] += 1
    data[cmdr] = recipient_data

    # Update thank log
    sender_data["thanks"][cmdr] = now.isoformat()
    data[sender_id] = sender_data
    save_comradery_points(data)

    # Get recipient object
    recipient = interaction.guild.get_member(int(cmdr))
    recipient_name = recipient.display_name if recipient else f"<@{cmdr}>"

    messages = [
        f"📦 {recipient_name}, you’ve been thanked! That’s one more box of joy delivered!",
        f"🛰️ {recipient_name}, your help just got wrapped up with gratitude. One comradery point earned!",
        f"📬 {recipient_name} just received a thank-you delivery—sealed with kindness!",
        f"🪐 {recipient_name}, you’re navigating the galaxy with generosity! +1 comradery point.",
        f"💫 {recipient_name}, that was an elite-class act. Here's a box full of thanks!",
        f"📦 You don’t just carry crates, {recipient_name}, you carry hearts. Thank you!",
        f"🔧 {recipient_name}, you’ve been thanked for smooth haulin’ and stellar support!",
        f"📦 {recipient_name}, you just stacked another box of goodwill!",
        f"🛠️ You engineered some good vibes, {recipient_name}! Here's a thank you!",
        f"💌 {recipient_name}, your kindness got express-shipped back as gratitude!",
        f"🌌 Another system, another thank you—{recipient_name} earns a comradery point!",
        f"🚀 {recipient_name}, your actions had impact velocity. Thanks for the assist!",
        f"📦 Elite cargo move: {recipient_name} just hauled in appreciation!",
        f"💼 {recipient_name} just signed for a box labeled *‘Thanks’*. Enjoy!",
        f"📡 Gratitude transmission sent. {recipient_name}, your signal’s loud and clear!",
        f"📦 That was a clean drop, {recipient_name}. Thank you for being awesome!",
        f"🫱‍🫲 {recipient_name}, comradery acknowledged! That box of thanks is all yours!",
        f"📦 Ping! One gratitude crate delivered to {recipient_name}.",
        f"🎖️ {recipient_name} has been officially thanked. That’s elite community service!",
        f"🔋 {recipient_name}, your kindness just recharged the gratitude drive!"
    ]

    message = random.choice(messages)
    await interaction.followup.send(message)

@client.tree.command(name="market-leaderboard", description="Show the top two markets for each colonization commodity", guild=GUILD_ID)
async def market_leaderboard(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    try:
        with open("top_markets.json", "r") as f:
            top_data = json.load(f)
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to load leaderboard data: {e}", ephemeral=True)
        return

    # Build compact leaderboard entries
    entries = []
    for commodity, markets in top_data.items():
        lines = [f"🏆 **{commodity}**"]
        for i, m in enumerate(markets, start=1):
            line = f"  {i}. `{m['stationName']}` in `{m['systemName']}` — **{m['stock']}** units"
            lines.append(line if len(line) <= 180 else line[:177] + "...")
        entry = "\n".join(lines)
        entries.append(entry if len(entry) <= 900 else entry[:897] + "...\n")

    # Build pages safely under 2000 chars
    pages = []
    current = ""
    for entry in entries:
        if len(current) + len(entry) + 2 <= 1950:  # buffer for heading
            current += entry + "\n\n"
        else:
            pages.append(current.strip())
            current = entry + "\n\n"
    if current:
        pages.append(current.strip())

    if not pages:
        await interaction.followup.send("⚠️ No valid leaderboard data to display.", ephemeral=True)
        return

    class LeaderboardView(discord.ui.View):
        def __init__(self, pages):
            super().__init__(timeout=180)
            self.pages = pages
            self.page = 0

        async def update_message(self, interaction: discord.Interaction):
            content = f"📦 **Top Market Leaderboard** (Page {self.page + 1}/{len(self.pages)})\n\n{self.pages[self.page]}"
            if len(content) > 1990:
                content = content[:1985] + "\n...(truncated)"
            try:
                await interaction.response.edit_message(content=content, view=self)
            except discord.HTTPException:
                await interaction.response.send_message("❌ Failed to update leaderboard view. Message too long.", ephemeral=True)

        @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
        async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.page > 0:
                self.page -= 1
            await self.update_message(interaction)

        @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
        async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.page < len(self.pages) - 1:
                self.page += 1
            await self.update_message(interaction)

    # Initial page content
    initial_content = f"📦 **Top Market Leaderboard** (Page 1/{len(pages)})\n\n{pages[0]}"
    if len(initial_content) > 1990:
        initial_content = initial_content[:1985] + "\n...(truncated)"

    await interaction.followup.send(
        content=initial_content,
        view=LeaderboardView(pages)
    )


ACTIVE_EXPEDITIONS_FILE = "active_expeditions.json"
AUTHORIZED_ROLE_ID = ADMIN_ROLE  # Role allowed to use the command

def load_active_expeditions():
    if not os.path.exists(ACTIVE_EXPEDITIONS_FILE):
        return {}
    with open(ACTIVE_EXPEDITIONS_FILE, "r") as f:
        return json.load(f)

def save_active_expeditions(data):
    with open(ACTIVE_EXPEDITIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_setup_values(sheet_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)
    setup = sheet.worksheet("SETUP")
    values = setup.get("B1:B4")

    return [v[0] if v else "" for v in values]

# Role check
def has_authorized_role():
    async def predicate(interaction: discord.Interaction):
        return any(role.id == AUTHORIZED_ROLE_ID for role in interaction.user.roles)
    return app_commands.check(predicate)

@client.tree.command(name="register-op", description="Register a new expedition operation", guild=GUILD_ID)
@app_commands.describe(sheet_id="The Google Sheet ID (not the whole URL)")
@has_authorized_role()
async def register_op(interaction: discord.Interaction, sheet_id: str):
    await interaction.response.defer(ephemeral=True)

    try:
        values = get_setup_values(sheet_id)
        if len(values) < 4:
            await interaction.followup.send("⚠️ The SETUP sheet is not fully filled out. Must contain values in B1 to B4.", ephemeral=True)
            return

        expedition = {
            "Name": values[0],
            "Keyword": values[1],
            "ResupplySys": values[2],
            "Dibs": values[3],
            "SheetID": sheet_id
        }

        active_expeditions = load_active_expeditions()
        active_expeditions[sheet_id] = expedition
        save_active_expeditions(active_expeditions)

        await interaction.followup.send(f"✅ Registered expedition: **{expedition['Name']}** using keyword `{expedition['Keyword']}`", ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"❌ Error registering expedition: `{e}`", ephemeral=True)




def load_expedition_sheet(sheet_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)

    # Helper to normalize sheet data
    def normalize(values):
        return [[cell if str(cell).strip() else " " for cell in row] for row in values]

    return {
        "setup": sheet.worksheet("SETUP"),
        "route": normalize(sheet.worksheet("ROUTE").get_all_values()),
        "route_ws": sheet.worksheet("ROUTE"),
        "fc_manifest": normalize(sheet.worksheet("FC-Manifest").get_all_values()),
        "fc_ws": sheet.worksheet("FC-Manifest"),
        "hauler_manifest": normalize(sheet.worksheet("Hauler-Manifest").get_all_values()),
        "hauler_ws": sheet.worksheet("Hauler-Manifest"),
        "admin_manifest": normalize(sheet.worksheet("Admin-Manifest").get_all_values()),
        "admin_ws": sheet.worksheet("Admin-Manifest")
    }



def summarize_expedition(name, setup_ws, route_data, fc_data):
    claim_system = setup_ws.acell("B7").value
    resupply_system = setup_ws.acell("B3").value
    allow_dibs = setup_ws.acell("B4").value.lower() == "true"

    try:
        total_links = int(setup_ws.acell("B8").value)
    except:
        total_links = len(route_data) - 1  # fallback if B8 is missing or not a number

    completed_links = sum(1 for row in route_data[1:] if row[3].strip().lower() == "true")

    def parse_time_fallback(s):
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            try:
                return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.min


    fc_sorted = sorted(fc_data[1:], key=lambda row: (
        0 if row[3] == "Unloading" else
        1 if row[3] == "Deployed" else
        2 if row[3] == "Loading" else
        3,
        parse_time_fallback(row[4]) if row[4] else datetime.min
    ))

    fc_lines = [
    f" **{row[0]}** ({row[1]}) |**{row[3]}**| @ `{row[5]}`\n   👤 Owner: {row[2]} \n"
    for row in fc_sorted
    ]

    return {
        "name": name,
        "claim": claim_system,
        "resupply": resupply_system,
        "dibs": allow_dibs,
        "progress": f"{completed_links}/{total_links}",
        "fc_lines": fc_lines
    }


def get_current_claim_status(route_rows):
    current_claim = None
    prev_completed_claim = "None"

    for i, row in enumerate(route_rows):
        if i == 0:
            continue

        claimed = row[2].strip().lower() == "true"
        completed = row[3].strip().lower() == "true"

        if claimed and not completed:
            current_claim = (row[1], "beacon deployed 🥓")
            break  # We found the current system that has a beacon but is not completed
        elif claimed and completed:
            prev_completed_claim = row[1]
        elif not claimed and not completed:
            # If nothing is claimed yet (early in the list)
            if current_claim is None:
                # Check if there was a previous completed to suggest next system
                dibs = f"{row[4].strip()} called dibs" if len(row) > 4 and row[4].strip() else "open for claiming"
                current_claim = (row[1], f"no beacon - {dibs}")
                break

    # Handle edge case: if everything is claimed and completed
    if current_claim is None:
        return "✅ All systems claimed and completed", prev_completed_claim

    system_name, status = current_claim
    return f"{system_name} ({status})", prev_completed_claim

@client.tree.command(name="ops", description="View all current expeditions or inspect one in detail", guild=GUILD_ID)
@app_commands.describe(
    id="Optional: expedition keyword to inspect",
    public="Set to true to post the embed publicly without buttons"
)
async def ops(interaction: discord.Interaction, id: Optional[str] = None, public: Optional[bool] = False):
    await interaction.response.defer(ephemeral=not public)

    try:
        with open("active_expeditions.json", "r") as f:
            active_ops = json.load(f)
    except Exception:
        await interaction.followup.send("❌ Could not load active expedition data.", ephemeral=True)
        return

    if not id:
        if not active_ops:
            await interaction.followup.send("📭 No active expeditions registered.", ephemeral=True)
            return

        lines = [f"📦 **Active Expeditions:**\n"]
        for op in active_ops.values():
            lines.append(f"• **{op['Name']}** — keyword: `{op['Keyword']}`, Resupply: `{op['ResupplySys']}`, Dibs: `{op['Dibs']}`")

        class JoinExpeditionButton(discord.ui.Button):
            def __init__(self, expeditions):
                super().__init__(label="Join an Expedition", style=discord.ButtonStyle.primary)
                self.expeditions = expeditions

            async def callback(self, interaction: discord.Interaction):
                options = [
                    discord.SelectOption(label=exp["Name"], value=key, description=f"Keyword: {exp['Keyword']}")
                    for key, exp in self.expeditions.items()
                ]

                class ExpeditionSelect(discord.ui.Select):
                    def __init__(inner_self):
                        super().__init__(placeholder="Choose an expedition", options=options)

                    async def callback(inner_self, inter: discord.Interaction):
                        selected_key = inner_self.values[0]
                        expedition = self.expeditions[selected_key]
                        await inter.response.send_message(
                            f"🧭 You selected **{expedition['Name']}**. Choose your role:",
                            view=JoinRoleSelector(expedition),
                            ephemeral=True
                        )

                class JoinView(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.add_item(ExpeditionSelect())

                await interaction.response.send_message("🌌 Select an expedition:", view=JoinView(), ephemeral=True)

        class JoinRoleSelector(discord.ui.View):
            def __init__(self, expedition):
                super().__init__()
                self.expedition = expedition

            async def handle_hauler(self, sheets, username):
                if any(username.lower() == row[0].strip().lower() for row in sheets["hauler_manifest"][1:]):
                    return False
                sheets["hauler_ws"].append_row([username, "0", "Joined @ " + datetime.utcnow().isoformat()])
                return True

            async def handle_fc_owner(self, interaction, sheets, username, skip_modal=False):
                if any(username.lower() == row[2].strip().lower() for row in sheets["fc_manifest"][1:]):
                    await interaction.response.send_message("⚠️ You're already listed as an FC owner.", ephemeral=True)
                    return

                resupply = self.expedition["ResupplySys"]

                class FCInfoModal(discord.ui.Modal, title="Enter FC Info"):
                    callsign = discord.ui.TextInput(label="FC Callsign", placeholder="ABC-123", required=True)
                    name = discord.ui.TextInput(label="FC Name", required=True)

                    async def on_submit(modal_self, inter: discord.Interaction):
                        cs = modal_self.callsign.value.strip().upper()
                        name = modal_self.name.value.strip()
                        now = datetime.utcnow().isoformat()

                        import re
                        if not re.fullmatch(r"[A-Z0-9]{3}-[A-Z0-9]{3}", cs):
                            await inter.response.send_message("❌ Invalid format. Use `ABC-123`.", ephemeral=True)
                            return

                        if any(cs == row[0].strip().upper() for row in sheets["fc_manifest"][1:]):
                            await inter.response.send_message(
                                f"⚠️ An FC with callsign `{cs}` is already registered.",
                                ephemeral=True
                            )
                            return

                        sheets["fc_ws"].append_row([cs, name, username, "Empty", now, resupply])
                        id=self.expedition["Keyword"]
                        await inter.response.send_message(
                            f"✅ FC **{name}** with callsign `{cs}` added.\n📍 Please jump your FC to `{resupply}`. When your buy orders are open, run `/ops id:{id}` and select **Open for Resupply**.",
                            ephemeral=True
                        )

                await interaction.response.send_modal(FCInfoModal())

            @discord.ui.button(label="Hauler", style=discord.ButtonStyle.secondary)
            async def join_hauler(self, interaction: discord.Interaction, button: discord.ui.Button):
                sheets = load_expedition_sheet(self.expedition["SheetID"])
                username = interaction.user.display_name.strip()
                success = await self.handle_hauler(sheets, username)
                if success:
                    await interaction.response.send_message(f"✅ Added to Hauler-Manifest for `{self.expedition['Name']}`.", ephemeral=True)
                else:
                    await interaction.response.send_message("⚠️ You're already listed as a hauler.", ephemeral=True)

            @discord.ui.button(label="FC Owner", style=discord.ButtonStyle.secondary)
            async def join_fc(self, interaction: discord.Interaction, button: discord.ui.Button):
                sheets = load_expedition_sheet(self.expedition["SheetID"])
                username = interaction.user.display_name.strip()
                await self.handle_fc_owner(interaction, sheets, username)

            @discord.ui.button(label="Both", style=discord.ButtonStyle.success)
            async def join_both(self, interaction: discord.Interaction, button: discord.ui.Button):
                sheets = load_expedition_sheet(self.expedition["SheetID"])
                username = interaction.user.display_name.strip()

                already_hauler = any(username.lower() == row[0].strip().lower() for row in sheets["hauler_manifest"][1:])
                already_fc = any(username.lower() == row[2].strip().lower() for row in sheets["fc_manifest"][1:])

                if already_hauler and already_fc:
                    await interaction.response.send_message("⚠️ You're already listed as both a hauler and FC owner.", ephemeral=True)
                    return

                if not already_hauler:
                    await self.handle_hauler(sheets, username)

                if not already_fc:
                    await self.handle_fc_owner(interaction, sheets, username)

        view = discord.ui.View()
        view.add_item(JoinExpeditionButton(active_ops))
        await interaction.followup.send("\n".join(lines), view=view, ephemeral=True)
        return

    # ID PROVIDED — DETAILED EXPEDITION VIEW
    selected = next((op for op in active_ops.values() if op["Keyword"].lower() == id.lower()), None)
    if not selected:
        await interaction.followup.send(f"❌ No expedition with keyword `{id}` found.", ephemeral=True)
        return

    try:
        sheets = load_expedition_sheet(selected["SheetID"])
        summary = summarize_expedition(selected["Name"], sheets["setup"], sheets["route"], sheets["fc_manifest"])
        current_claim, prev_claim = get_current_claim_status(sheets["route"])
        summary["claim"] = current_claim
        summary["prev_claim"] = prev_claim
        summary["Keyword"]=id
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error reading spreadsheet: `{e}`", ephemeral=True)
        return
    
    sheetid=selected["SheetID"]
    user_name = interaction.user.display_name.strip().lower()
    is_hauler = any(user_name == row[0].strip().lower() for row in sheets["hauler_manifest"][1:])
    is_fc_owner = any(user_name == row[2].strip().lower() for row in sheets["fc_manifest"][1:])
    is_admin = any(user_name == row[0].strip().lower() for row in sheets["admin_manifest"][1:])
    
    status_emojis = {
        "Unloading": "🚧", "Deployed": "📡", "Loading": "📦",
        "Empty": "🔳", "Full": "✅", "Suspended": "🚫"
    }

    fc_resupply = ["\n","**FCs in RESUPPLY:**"]
    resupply_cons= ["Loading","Full"]
    fc_frontier= ["\n**FCs On the FRONTIER:**"]
    frontier_cons= ["Unloading","Deployed","Empty"]
    fc_lines =["\n**Misc FCs**\n"]
    for row in summary["fc_lines"]:
        parts = row.split("|")
        if len(parts) >= 3:
            locale_raw=parts[2].split("`")
            status = parts[1].strip()
            clean_status=status.strip("**")
            locale= locale_raw[1]
            emoji = status_emojis.get(clean_status, "❓")
            if locale == summary['resupply']:
                fc_resupply.append(f"{emoji} {parts[0]} - {status} - {parts[2]}")
            elif len(locale)>0: 
                fc_frontier.append(f"{emoji} {parts[0]} - {status} - {parts[2]}")
        else:
            fc_lines.append(f"• {row}")
    fc_resupply.extend(fc_frontier)
    fc_resupply.extend(fc_lines)
    current_status, previous_claim = get_current_claim_status(sheets["route"])

    embed = discord.Embed(
        title=f"🧭 Expedition: {summary['name']}",
        description=(
            f"📍 **Current Claim:** `{current_status}`\n"
            f"↩️ **Previous Claim:** `{previous_claim}`\n"
            f"🔄 **Resupply:** `{summary['resupply']}`\n"
            f"📈 **Progress:** `{summary['progress']}`"
        ),
        color=discord.Color.teal()
    )

    embed.add_field(name="----🚢 Fleet Carrier Status'----\n", value="\n".join(fc_resupply) or "None", inline=False)
    if public:
        await interaction.followup.send(embed=embed)
    else:
        view = OpsActionView(
            user_role_flags={"hauler": is_hauler, "fc_owner": is_fc_owner,"admin":is_admin},
            expedition_data=summary,
            sheet_id=selected["SheetID"]
        )

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)


@tasks.loop(hours=1)
async def daily_banner_update():
    guild = client.get_guild(GUILD_ID_NUM)  # Use your actual guild ID
    if not guild:
        print("Guild not found.")
        return

    folder_path = "banner-pics"
    banner_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not banner_files:
        print("No banner images found in banner-pics folder.")
        return

    chosen_banner = random.choice(banner_files)
    banner_path = os.path.join(folder_path, chosen_banner)

    try:
        with open(banner_path, 'rb') as banner_file:
            await guild.edit(banner=banner_file.read())
        print(f"✅ Banner updated to {chosen_banner}")
    except Exception as e:
        print(f"⚠️ Failed to update banner: {e}")

@daily_banner_update.before_loop
async def before_banner_update():
    await client.wait_until_ready()



@client.tree.command(name="boxbot", description="Get a warm welcome and choose a theme to learn more!", guild=GUILD_ID)
async def boxbot(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    intro_embed = discord.Embed(
        title="📦 BoxBot Introduction",
        description="Hello, Commander! I am BoxBot — your quirky logistics AI! I thrive on crates, cargo, and colonization. Select a theme to explore my many helpful features.",
        color=discord.Color.blue()
    )

    class BoxBotView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=180)


        @discord.ui.button(label="Expeditions", style=discord.ButtonStyle.primary)
        async def expeditions(self, interaction: discord.Interaction, button: discord.ui.Button):
            await send_dynamic_response(interaction, "🧭 Expeditions", (
                "BoxBot manages expeditions via `/ops`, where you can view active missions and join as a hauler, FC owner, or both. Ops fully supports logistics and organization of the whole expidition! "
                "Expeditions pave the way for future colonization by establishing routes and support chains."
            ))

        @discord.ui.button(label="Colonization Support", style=discord.ButtonStyle.primary)
        async def colonization(self, interaction: discord.Interaction, button: discord.ui.Button):
            await send_dynamic_response(interaction, "🏗️ Colonization Support", (
                "Commands include: `/howis-fc` (given FC market details), `/whereis-fc` (given FC location), `/yardsale` (selling FCs), `/shop-local` (local supply search from nearby Starports), `/market_leaderboard` (only starports not FCs). "
                "Visit #colonization-tools for more."
            ))

        @discord.ui.button(label="Community", style=discord.ButtonStyle.primary)
        async def community(self, interaction: discord.Interaction, button: discord.ui.Button):
            await send_dynamic_response(interaction, "🤝 Community", (
                "Commands include: /departures (see where/when FCs are leaving to catch a ride) /dropoff (record your hauls) /my-stats  /market-updated (record when you open a commodity market with an eddn listen active. Earn community points) /add-ferry (add your FC to departures ) /join-yardsale (add your FC to yardsale) /thank (thank another commander)"
                "Coordinate, track, and celebrate with your peers."
            ))

        @discord.ui.button(label="Shenanigans", style=discord.ButtonStyle.primary)
        async def shenanigans(self, interaction: discord.Interaction, button: discord.ui.Button):
            await send_dynamic_response(interaction, "🎉 Shenanigans", (
                "Fun commands: `/diversion` (cat GIFs), `/make-bacon`, `/whats-in-your-box`(I tell you what is in my box), `/whats-with-the-fox`(learn about the fox), `/praise`(praise me), `/chastise`(chastise me), `/boxfacts`. "
                "Enjoy some light-hearted chaos."
            ))

    await interaction.followup.send(embed=intro_embed, view=BoxBotView(), ephemeral=True)

async def send_dynamic_response(interaction, title, base_text):
    # Immediately acknowledge the interaction
    placeholder_embed = discord.Embed(
        title=title,
        description="⏳ I am unboxing my response... please wait!",
        color=discord.Color.orange()
    )
    await interaction.response.edit_message(embed=placeholder_embed, view=None)

    final_text = base_text

    # Replace the placeholder with the final response
    final_embed = discord.Embed(title=title, description=final_text, color=discord.Color.green())
    try:
        await interaction.edit_original_response(embed=final_embed)
    except discord.errors.NotFound:
        # Fallback if the message was deleted
        await interaction.followup.send(embed=final_embed, ephemeral=True)


client.run(BOT_SECRET)
