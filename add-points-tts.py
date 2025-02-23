"""
Add Points and Synthesize - A text-to-speech formatting and synthesis tool.

Script Name:    add-points-tts.py
Description:    A Python tool that enhances text-to-speech by formatting sentences
                for natural pauses and synthesizing high-quality speech using
                Microsoft AI voices.
Author:         Mario Montoya <mariosght500@gmail.com>
Date:           2025-02-23

Version History:
- v0.1 (2025-02-23): Get Voices by Locale and Country and save preferences.

Copyright (C) 2025 Mario Montoya

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU Affero General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more 
details.

For a copy of the license, see <https://www.gnu.org/licenses/>.
"""
import json
from collections import defaultdict
import random
import os
import requests
import html
import platform
import subprocess

class VoiceList:
    "Get the Locale, LocaleName, Voice, Gender and WordPerMinute. Get the token to get the list."

    def __init__(self, target_languages, min_voice_count):
        """Initialize the VoiceList with the target languages and the minimum voice count"""
        self.target_languages = target_languages
        self.min_voice_count = min_voice_count

    def get_token(self):
        """Authenticate and get an access token from Azure Speech Service."""
        url = f"https://{os.getenv('SPEECH_REGION')}.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            "Ocp-Apim-Subscription-Key": os.getenv("SPEECH_KEY")
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        self.token = response.text

    def get_voices(self):
        """Retrieve the list of available voices from Azure Speech Service."""
        url = f"https://{os.getenv('SPEECH_REGION')}.tts.speech.microsoft.com/cognitiveservices/voices/list"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.voices = response.json()

    def save_voices_to_json(self, filename="all_voices.json", rawname="raw_voices.json"):
        """Save voices to 2 JSON files. One with some of the keys. Another with raw information."""
        keys = ["Locale", "LocaleName", "ShortName", "Gender", "WordsPerMinute"]
        voice_data = [{key: v[key] for key in keys if key in v} for v in self.voices]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(voice_data, f, indent=4, ensure_ascii=False)
        with open(rawname, "w", encoding="utf-8") as f:
            json.dump(self.voices, f, indent=4, ensure_ascii=False)

    def load_voices_from_json(self, filename="all_voices.json"):
        """Load voices from a JSON file and create a list of locales with their voice count."""
        with open(filename, "r", encoding="utf-8") as f:
            self.voices = json.load(f)
        locale_counts = defaultdict(lambda: {"LocaleName": "", "VoiceCount": 0})
        for voice in self.voices:
            locale = voice["Locale"]
            locale_counts[locale]["LocaleName"] = voice["LocaleName"]
            locale_counts[locale]["VoiceCount"] += 1
        self.locales = [{"Locale": locale, **data} for locale, data in locale_counts.items()]

    def filter_and_display_locales(self):
        """Filter locales by target languages, and display in a 3-column format."""
        # Filter locales where LocaleName contains any of the target languages
        # AND VoiceCount is greater than or equal to min_voice_count
        filtered_locales = [
            (locale["Locale"], locale["LocaleName"], locale["VoiceCount"])
            for locale in self.locales
            if any(lang in locale["LocaleName"] for lang in self.target_languages)
            and locale["VoiceCount"] >= self.min_voice_count
        ]

        # Determine column width based on longest string
        max_locale_len = max(len(l[0]) for l in filtered_locales)
        max_name_len = max(len(l[1]) for l in filtered_locales)
        max_count_len = max(len(str(l[2])) for l in filtered_locales)
        
        col_widths = [max_locale_len, max_name_len, max_count_len]
        
        # Print header
        header = f"{'Locale'.ljust(col_widths[0])} {'LocaleName'.ljust(col_widths[1])} {'VoiceCount'.rjust(col_widths[2])}"
        print(header)
        print("=" * len(header))

        # Print data in a 3-column format
        for locale, name, count in filtered_locales:
            print(f"{locale.ljust(col_widths[0])}  {name.ljust(col_widths[1])} {str(count).rjust(col_widths[2])}")

    def filter_and_display_languages(self):
        """Filter locales, count voices by language, and display in a 2-column format."""
        # Lambda function to extract the first word (language) from LocaleName
        get_first_word = lambda s: s.split()[0]

        # Group by language and sum VoiceCount
        language_voice_count = {}
        for locale in self.locales:
            language = get_first_word(locale["LocaleName"])
            language_voice_count[language] = language_voice_count.get(language, 0) + locale["VoiceCount"]
        
        # Filter by minimum voice count and target languages
        filtered_languages = {
            lang: count for lang, count in language_voice_count.items()
            if count >= self.min_voice_count and lang in self.target_languages
        }

        # Determine column width based on longest string
        max_lang_len = max(len(lang) for lang in filtered_languages.keys())
        max_count_len = max(len(str(count)) for count in filtered_languages.values())
        col_widths = [max_lang_len, max_count_len]
        
        # Print header
        header = f"{'Language'.ljust(col_widths[0])} {'Voices'.rjust(col_widths[1])}"
        print(header)
        print("=" * len(header))
        
        # Print data in a 2-column format
        for language, count in sorted(filtered_languages.items()):
            print(f"{language.ljust(col_widths[0])} {str(count).rjust(col_widths[1])}")


def read_preference_file(filename="preference.json"):
    """Read the user-preferred Locale or Language."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("filter_by"), data.get("filter_value")
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None    

def prompt_and_save_user_preference(voiceList, filename="preference.json"):
    """Prompts if the user prefers to filter by Locale (Country) or by Language.
    Display the options depending on user input. Prompts for the filter itself.
    Save the selections."""
    
    while True:
        filter_by = input("Would you like to filter by Country or Language? (C/L): ").strip().upper()
        if filter_by in ["C", "L"]:
            break
        print("Invalid input. Please enter 'C' or 'L'.")
    
    if filter_by == "C":
        filter_by = "Locale"
        voiceList.filter_and_display_locales()
    else:
        filter_by = "Language"
        voiceList.filter_and_display_languages()
    
    filter_value = input(f"Enter your preferred {filter_by}: ").strip()
    
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({"filter_by": filter_by, "filter_value": filter_value}, file, indent=4)
    return filter_by, filter_value

def process_text(filter_by, filter_value):
    """Enter the text you want to hear. Add a period and a space to every sentence for proper pausing.
    Enter a zero on the first line to change Language. Or enter a nine on the first line to exit."""
    
    if filter_by == "Locale":
        lang_code = filter_value.split("-")[0]  # Extract the first two letters of locale
        message = next((inst["Message"] for inst in instructions if inst["Lan"] == lang_code), None)
    elif filter_by == "Language":
        message = next((inst["Message"] for inst in instructions if inst["Language"] == filter_value), None)
    else:
        message = None
    
    # Fallback to English
    if message is None:
        message = next((inst["Message"] for inst in instructions if inst["Lan"] == "en"), "Instruction message not found.")
    
    print(message)
    sentences = []

    # Capture the first line separately
    first_line = input().strip()
    
    # If the first line is a digit (0-9), return it immediately
    if first_line.isdigit():
        return first_line, ""

    # Otherwise, process the text
    if first_line.endswith("."):
        sentences.append(first_line + " ")
    else:
        sentences.append(first_line + ". ")

    while True:
        line = input().strip()
        if line.isdigit():  # If the line is a number, break the loop
            break
        if line.endswith("."):
            sentences.append(line + " ")
        else:
            sentences.append(line + ". ")

    # Delete the last n lines
    n = int(line)
    sentences = sentences[:-n or None]

    result = "\n".join(sentences)
    
    return first_line, result


def select_voice(filter_by, filter_value, filename="all_voices.json"):
    """Randomly select a voice from the filtered voices."""
    # Lambda function to extract the first word (language) from LocaleName
    first_word = lambda s: s.split()[0]

    # Load voices from file
    with open(filename, "r", encoding="utf-8") as f:
        voices = json.load(f)

    # Filter voices based on user preference
    if filter_by == "Locale":
        filtered_voices = [v for v in voices if v["Locale"] == filter_value]
    else:  # filter_by == "Language"
        filtered_voices = [v for v in voices if first_word(v["LocaleName"]) == filter_value]

    # If no voices match, return an error message
    if not filtered_voices:
        print("No matching voices found.")
        return None

    # Randomly select a voice
    voice = random.choice(filtered_voices)['ShortName']
    print(f"Selected voice: {voice}")
    return voice

def text_to_mp3(text, voice, filename="output.mp3"):
    key = os.getenv('SPEECH_KEY')
    region = os.getenv('SPEECH_REGION')

    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3"
    }
    
    # Escape special XML characters (& -> &amp;, < -> &lt;, > -> &gt;)
    safe_text = html.escape(text)

    data = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='pt-BR' name='{voice}'>{safe_text}</voice></speak>"

    if os.path.exists(filename):
        os.remove(filename)

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print("Error:", response.text)  # Print error details

def play_mp3(filename="output.mp3"):
    # MPV arguments to not use GUI
    args = ['--terminal=no', '--force-window=no', filename]
    # Play the MP3 file with MPV
    if platform.system() == "Windows":
        subprocess.run([mpv_path] + args)
    elif platform.system() == "Darwin" or platform.system() == "Linux":  # macOS or Linux
        subprocess.run(["mpv"] + args)
    else:
        raise OSError("Unsupported operating system")

def show_license_notice():
    print("=" * 60)
    print(" Add Points and Synthesize - Open Source Speech Tool")
    print(" Licensed under AGPL-3.0 - See https://www.gnu.org/licenses/")
    print("=" * 60)
    print()

def read_config():
    # Load JSON configuration file
    with open('add-points.json', 'r', encoding="utf-8") as file:
        config = json.load(file)
    global mpv_path, target_languages, min_voice_count, instructions
    mpv_path, target_languages, min_voice_count = config['mpv_path'], config['target_languages'], config['min_voice_count']
    instructions = config['instructions']

def main():
    voiceList = VoiceList(target_languages, min_voice_count)
    filter_by, filter_value = read_preference_file()
    if not filter_by:
        voiceList.get_token()
        voiceList.get_voices()
        voiceList.save_voices_to_json()
        voiceList.load_voices_from_json()
        filter_by, filter_value = prompt_and_save_user_preference(voiceList)

    # Main loop
    while True:
        first_line, result = process_text(filter_by, filter_value)
        
        if first_line == "0":
            # Change language preference
            voiceList.load_voices_from_json()
            filter_by, filter_value = prompt_and_save_user_preference(voiceList)
            continue  # Restart the loop with the new language
        
        elif first_line == "9":
            # Exit the program
            break

        elif result == "":
            print("You deleted all the lines. Try a lower number.")
            continue

        voice = select_voice(filter_by, filter_value)
        if voice:
            text_to_mp3(result, voice)
            play_mp3()

if __name__ == "__main__":
    show_license_notice()  # Display the license notice at startup
    read_config()
    main()
