## Mp3-Download-Bot
A python based bot for mass locating and downloading mp3 files locally

This project was created to help a DJ friend automate the process of downloading hundreds of songs for his mixtape. What started as a simple script to batch-download songs using `yt-dlp` evolved into a full-fledged Python bot that can search for songs based on a provided list, gather shareable URLs, and handle downloading efficiently.

## How I Built This

The idea for this project came when my DJ friend needed to download hundreds of songs for a new mixtape. Manually searching and downloading these songs would have been a time-consuming task, so I decided to create a solution that could automate this process.

### The Beginning: `run.sh` for Batch Downloads

Initially, I started by writing a shell script (`run.sh`) that used `yt-dlp` (a YouTube video downloader) to batch download songs. The script was designed to take a list of YouTube share links, download the audio, and save the files. It worked well for the task at hand but was limited in flexibility and scalability.

### Expanding to a Python Bot

After seeing the limitations of the shell script, I realized I needed something more dynamic and scalable. That's when I decided to expand the project into a Python bot using Selenium and other Python libraries.

The bot would:

- Parse through an exported list of song names.
- Automatically search for each song on YouTube Music.
- Extract the shareable URLs.
- Download each song using `yt-dlp`.

This change allowed me to automate the entire process and handle thousands of songs in a fraction of the time it would have taken manually.

### Key Features:

- **Automated Song Search**: The bot searches for each song on YouTube Music using the provided list of song names.
- **Share URL Extraction**: It interacts with the YouTube Music interface, clicks on the share button, and extracts the shareable URL.
- **Batch Downloading**: The bot generates a list of URLs that can be used for bulk downloads via `yt-dlp`.
- **Error Handling**: If a song cannot be found, it is logged into an `unlinked.txt` file, allowing you to address missing tracks later.

### How It Works

1. **Input**: The bot takes an input file (`list.txt`) that contains a list of song names.
2. **Processing**: It searches for each song on YouTube Music, grabs the shareable URL, and logs it.
3. **Output**: Successfully found URLs are saved to `url_list.txt`, while any songs that couldn't be found are recorded in `unlinked.txt`.

Once the bot finishes processing the entire list, it runs the "run.sh" script which uses `yt-dlp` with the generated URL list for a fast, bulk download of all the songs.

## Getting Started

### Requirements:

- Python 3.x
- Selenium
- Firefox WebDriver (or other drivers depending on your browser)
- `yt-dlp` (for downloading the songs)

### Installation:

4. Clone this repository:
    
    bash
    
    Copy
    
    `git clone https://github.com/owxneby/Mp3-Download-Bot.git cd Mp3-Download-Bot`
    
5. Install the required Python dependencies:
    
    bash
    
    Copy
    
    `python 3 -m pip install -r requirements.txt`
    
6. Install yt-dlp: Follow the official installation instructions available on their GitHub page:
https://github.com/yt-dlp/yt-dlp/wiki/Installation

You can also install it via pip directly:
    
    bash
    
    Copy
    
    `python3 -m pip install -U "yt-dlp[default]"`
    
7. Set up the Firefox WebDriver (or use a different browser of your choice. I plan on building for alternate webdrivers).

    

### Usage:

8. Place your list of song names in the `list.txt` file. Each line should contain a song name.
    
9. Run the bot:
    
    bash
    
    Copy
    
    `python main.py`
    
10. The bot will start processing the list and will output the results to `url_list.txt` (for successful finds) and `unlinked.txt` (for failed searches).
    

### Running the Batch Download

Once the bot finishes, it wil initiate the run.shyou can run the following command to download all songs using `yt-dlp`:

bash

Copy

`yt-dlp -a url_list.txt`

## Project Structure

bash

Copy

`song-downloader-bot/ │ 
├── main.py              # Python bot that handles song search and URL extraction 
├── run.sh              # Shell script for batch downloading via yt-dlp (automatically executed by the bot)
├── list.txt            # Input file containing the list of song names 
├── url_list.txt        # Output file containing the successfully found song URLs 
├── unlinked.txt        # Output file for songs that couldn't be found 
└── requirements.txt     # Python dependencies

## Conclusion

This project started as a simple solution to automate song downloading for a mixtape, but it grew into a more robust Python bot that can handle large lists of songs, search for them, and download them automatically. Whether you're a DJ, a music enthusiast, a person trying to build a local music library or anyone who needs to collect music in bulk, this tool can save you a lot of time!

## Future Plans

I plan on expanding the support for additional WebDrivers, such as Safari and Chrome, and providing improved compatibility for different operating systems, including Windows and macOS. This will make the bot more versatile and easier to run on various platforms.

Additionally, I’m considering transforming the bot into a web server in the future, so it can be accessed and controlled via a web interface. This would make it even easier to manage and automate the song downloading process without needing to interact with the code directly.

Feel free to contribute to the project by submitting issues or pull requests. You’re welcome to use and modify the code for your own needs, and I appreciate any improvements or optimizations you might suggest. Let’s build something great together!

