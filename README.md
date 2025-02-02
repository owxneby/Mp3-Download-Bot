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

