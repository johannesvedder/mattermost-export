# Mattermost Export Tool with Viewer

A simple Python script to export chat data from Mattermost and generate a basic HTML chat view.
This tool allows you to select and view chats exported from Mattermost in an organized and user-friendly way.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [License](#license)

## Introduction

Mattermost is a popular team messaging platform. When you export chat data from Mattermost, it is stored in JSON format,
which may not be very user-friendly for reading. This tool takes exported Mattermost chat data in JSON format and
generates an HTML viewer to make it more accessible and readable.

## Prerequisites

Before using this tool, ensure you have the following installed on your system:
- Python (Python 3.x recommended)

## Getting Started

1. Clone this repository to your local machine or download the script directly.

2. Ensure you have a folder containing your exported Mattermost chat data in JSON format.

3. Open a terminal or command prompt and navigate to the directory containing the script.

4. Install and run the download script using Python:

   ```shell
   pip install -r requirements.txt
   python mattermost-dl.py
   ```

5. Backup as much of your data as you need. And let the script finish downloading.

6. Run the export script using Python:

   ```shell
   python mattermost-dl-viewer.py
   ```

7. The script will prompt you to enter the path of the folder containing your exported chat data. If you press Enter
without specifying a custom path, it will use the default 'results' folder with the current date.

8. The script will generate an HTML file (mattermost-dl-viewer.html) in the specified folder.

## Usage

- After running the script and generating the HTML file, open it in your web browser.
- You will see a chat selector that allows you to choose from the available chats.
- Once you select a chat, the chat messages will be displayed in an organized and readable format.

## Sample Output

Here's an example of how the generated HTML output looks:

![tba](sample_output.png)

## License

This tool is provided under the [MIT License](LICENSE). You are free to use, modify, and distribute it as needed.

`mattermost-dl.py` has been adapted from [this Gist](https://gist.github.com/RobertKrajewski/5847ce49333062ea4be1a08f2913288c).

---

**Note**: This tool was created to download and improve the readability of exported Mattermost chat data. It's not
officially affiliated with or endorsed by Mattermost.