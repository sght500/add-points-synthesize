# Add Points and Synthesize

## Introduction

**Add Points and Synthesize** is a Python-based tool designed to help language learners improve their pronunciation and comprehension by listening to texts in various voices. It ensures natural speech flow by automatically formatting text to match the optimal input format for text-to-speech (TTS) engines. The project utilizes **Microsoft Speech Services** to generate high-quality audio with diverse voices across multiple languages.

## Motivation

When learning a new language, it can be challenging to hear how a text should be read naturally. Many text-to-speech (TTS) services, including Google Translate, often produce monotonous, robotic voices, making listening practice less engaging.

Through exploration, we discovered a TTS service that required each sentence to end with a **period and a space** to ensure proper pausing. To automate this formatting, a spreadsheet was initially created, but copying large amounts of text became a challenge due to mobile security restrictions. This led to the development of this Python tool, which:

- **Formats text** by adding necessary punctuation and spacing.
- **Uses Microsoft Speech Services** to generate natural speech.
- **Provides randomized voices** for a more dynamic listening experience.

## Features

- **Automatic Text Formatting:** Ensures each sentence ends with a period and a space.
- **Multi-language Support:** Works with multiple languages including English, Portuguese, Spanish, French, German, and more.
- **Microsoft Speech Integration:** Fetches high-quality voices from Microsoft's AI-powered speech synthesis service.
- **Randomized Voice Selection:** Makes listening more engaging by selecting a different voice each time.
- **MPV Integration for Audio Playback:** Plays the generated speech automatically on supported platforms.

## Supported Languages

The tool currently supports the following languages (with at least 4 voice variations available):

- Arabic
- Chinese
- Dutch
- English
- French
- German
- Indonesian
- Italian
- Japanese
- Korean
- Polish
- Portuguese
- Russian
- Spanish
- Thai
- Turkish
- Vietnamese

## Installation

### Prerequisites

Before using this tool, ensure you have the following installed:

- **Python 3.x**
- **[Termux (for Android users)](TERMUX_SETUP.md)** (Optional, if running on a mobile device)
- **MPV media player** (Required for audio playback)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/sght500/add-points-synthesize.git
   cd add-points-synthesize
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Microsoft Speech API credentials:

   - Sign up for **[Microsoft Azure Speech Services](AZURE_SETUP.md)**.
   - Retrieve your **Subscription Key** and **Region**.
   - Export them as environment variables:
     ```bash
     export SPEECH_KEY="your_subscription_key"
     export SPEECH_REGION="your_region"
     ```

4. Run the script:

   ```bash
   python add-points-tts.py
   ```

## How to Use

1. **Enter your text line by line.** Each sentence should be on a separate line.
2. **End input by entering an integer.** This number specifies how many lines to delete from the end before processing.
3. **The tool automatically adds punctuation.** It ensures that each sentence ends with a period and a space.
4. **Audio is generated using a random voice.** The tool selects a voice from Microsoft Speech Services.
5. **MPV plays the generated audio file.**

### Commands

- **Enter `0` on the first line** → Change language.
- **Enter `9` on the first line** → Exit the program.

## Configuration

Modify `add-points.json` to customize settings:

- `mpv_path`: Path to MPV media player.
- `target_languages`: List of supported languages.
- `min_voice_count`: Minimum number of voices required for a language to be selectable.
- `instructions`: Language-specific prompts displayed in the program.

## Future Improvements

- **GUI version** for easier text input and playback.
- **Offline TTS support** to reduce reliance on Microsoft servers.
- **Customization options** for voice selection and speed adjustments.

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the project.

## License

This project is licensed under the **AGPL-3.0 License**. See [LICENSE](LICENSE) for details.

---

Developed with ❤️ to make language learning more engaging!
