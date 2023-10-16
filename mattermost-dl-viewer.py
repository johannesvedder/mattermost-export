import json
import html
import os
import glob
from datetime import datetime


# Function to load chat data from a JSON file
def load_chat_data(chat_dir):
    json_files = glob.glob(os.path.join(chat_dir, "*.json"))
    if json_files:
        with open(json_files[0], "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    return None


# Get the current date in the format 'YYYYMMDD'
current_date = datetime.now().strftime('%Y%m%d')

# Construct the default export folder path
default_export_folder = os.path.join('results', current_date)

# Ask the user to provide a path to the chat folder
export_folder = input(f"Please enter the path of the folder containing the downloaded chats (default: {default_export_folder}): ")

# If the user didn't provide a custom path, use the default
if not export_folder:
    export_folder = default_export_folder

# Find subdirectories containing JSON files
chat_directories = [directory for directory in os.listdir(export_folder) if
                    os.path.isdir(os.path.join(export_folder, directory)) and glob.glob(os.path.join(export_folder, directory, "*.json"))]

# Create an HTML chat template with a link to an external CSS file
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Mattermost Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }}
        h1 {{
            background-color: #0084ff;
            color: white;
            text-align: center;
            padding: 10px;
            margin: 0;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 5px;
            padding: 10px;
            box-shadow: 3px 3px 5px #888888;
        }}
        li p {{
            margin: 0;
        }}
        select {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <h1>Mattermost Viewer</h1>
    <label for="chatSelector">Select a Chat:</label>
    <select id="chatSelector" onchange="showChat()">
        {chat_options}
    </select>
    <div id="chatDisplay"></div>
    <script>
        var chatData = '{chat_data}'.split("\\\\").join('\\\\\\\\');
        function htmlDecode(input) {{
  var doc = new DOMParser().parseFromString(input, "text/html");
  return doc.documentElement.textContent;
}}    
    function showChat() {{
        var selector = document.getElementById("chatSelector");
        var selectedChat = selector.value;
        var chatDisplay = document.getElementById("chatDisplay");
        var chatDataObject = JSON.parse(chatData);
        
        var channelInfo = chatDataObject[selectedChat]["channel"];
        var posts = chatDataObject[selectedChat]["posts"];
        
        var displayHTML = "<h2>Channel Information</h2>";
        displayHTML += "<p><strong>Name:</strong> " + channelInfo.name + "</p>";
        displayHTML += "<p><strong>Display Name:</strong> " + channelInfo.display_name + "</p>";
        displayHTML += "<p><strong>ID:</strong> " + channelInfo.id + "</p>";
        displayHTML += "<p><strong>Exported At:</strong> " + channelInfo.exported_at + "</p>";
        
        displayHTML += "<h2>Posts</h2>";
        displayHTML += "<ul>";
        for (var i = 0; i < posts.length; i++) {{
            var post = posts[i];
            displayHTML += "<li>";
            displayHTML += "<p><strong>idx:</strong> " + post.idx + "</p>";
            displayHTML += "<p><strong>id:</strong> " + post.id + "</p>";
            displayHTML += "<p><strong>Username:</strong> " + post.username + "</p>";
            displayHTML += "<p><strong>Created:</strong> " + post.created + "</p>";
            displayHTML += "<p><strong>Message:</strong> " + htmlDecode(post.message) + "</p>";
            if ('files' in post) {{
                var files = post.files;
                displayHTML += "<p><strong>Files:</strong>";
                for (var j = 0; j < files.length; j++) {{
                    var file = files[j];
                    var path = selectedChat + "/" + post.idx.toString().padStart(3, '0') + "_" + j + "_" + file;
                    path = encodeURI(path);
                    displayHTML += "<p>" + "<a href=" + path + " target=_blank>" + file + "</a></p>";
                }}
                displayHTML += "</p>";
            }}
            displayHTML += "</li>";
        }}
        displayHTML += "</ul>";
        chatDisplay.innerHTML = displayHTML;
    }}
        showChat()
    </script>
</body>
</html>
"""

# Create chat data dictionary
chat_data = {}
chat_options = ""
for chat_directory in chat_directories:
    chat_directory = os.path.join(export_folder, chat_directory)
    chat_name = os.path.basename(chat_directory)
    chat_data_json = load_chat_data(chat_directory)
    if chat_data_json:
        chat_data_json["channel"]["header"] = html.escape(
            chat_data_json["channel"]["header"].replace("\n", r"<br>").replace("\t", r"<br>"),
            quote=True)
        for post in chat_data_json["posts"]:
            post["message"] = post["message"]
            post["message"] = html.escape(post["message"].replace("\n", r"<br>").replace("\t", r"<br>"), quote=True)
        chat_data[chat_name] = chat_data_json
        chat_options += f'<option value="{chat_name}">{chat_name}</option>'
# Insert the chat selector and chat messages into the HTML template
html_output = html_template.format(chat_options=chat_options, chat_data=json.dumps(chat_data, ensure_ascii=False))

file_path = os.path.join(export_folder, "mattermost_dl_viewer.html")

# Save the HTML to a file
with open(file_path, "w", encoding="utf-8") as html_file:
    html_file.write(html_output)

print(f"HTML view saved to {file_path}")
