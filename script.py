import gradio as gr
import requests
import re
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY', '')

def parse_arguments():
    parser = argparse.ArgumentParser(description='E-Z Host File Management Tool')
    parser.add_argument('action', choices=['upload', 'delete', 'info', 'shorten', 'paste'],
                       help='Action to perform: upload, delete, info, shorten URL, or create paste')
    parser.add_argument('--file', '-f', help='File path for upload')
    parser.add_argument('--url', '-u', help='URL for shortening or deletion')
    parser.add_argument('--text', '-t', help='Text content for paste')
    parser.add_argument('--title', help='Title for paste')
    parser.add_argument('--description', '-d', help='Description for paste')
    parser.add_argument('--language', '-l', help='Language for paste')
    return parser.parse_args()

def upload_file(file_path):
    url = 'https://api.e-z.host/files'
    headers = {
        'key': API_KEY
    }
    files = {
        'file': open(file_path, 'rb')
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_file_info(file_id):
    url = f'https://api.e-z.host/files/get/{file_id}'
    headers = {
        'key': API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def extract_file_id(url):
    pattern = r'r2\.e-z\.host/[^/]+/([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def delete_file(deletion_url):
    try:
        response = requests.delete(deletion_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during deletion: {e}")
        return None

def save_file_info(result):
    """Save file info to a local JSON file for future reference"""
    history_file = Path.home() / '.ezhost_history.json'
    history = []
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    
    history.append({
        'timestamp': import_time.strftime('%Y-%m-%d %H:%M:%S'),
        'imageUrl': result.get('imageUrl'),
        'rawUrl': result.get('rawUrl'),
        'deletionUrl': result.get('deletionUrl')
    })
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def shorten_url(url: str) -> Optional[Dict[str, Any]]:
    """Shorten a URL using the E-Z.host API"""
    api_url = 'https://api.e-z.host/shortener'
    headers = {
        'key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {'url': url}

    try:
        response = requests.post(api_url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print("API Response:", response.text)
        
        if response.status_code == 429:
            return {'error': 'Rate limit exceeded. Please try again later.'}
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            return {
                'shortenedUrl': result.get('shortendUrl'),
                'deletionUrl': result.get('deletionUrl'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            print(f"API Error: {result.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def create_paste(text: str, title: str = '', description: str = '', language: str = '') -> Optional[Dict[str, Any]]:
    """Create a paste using the E-Z.host API"""
    api_url = 'https://api.e-z.host/paste'
    headers = {
        'key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'title': title,
        'description': description,
        'language': language
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

class EZHostInterface:
    def __init__(self):
        self.history_file = Path.home() / '.ezhost_history.json'
        self.url_validity_cache = {}
        self.load_history()
        
        with gr.Blocks(
            title="E-Z Host Tool",
            css="""
                footer {display: none !important;}
                ::-webkit-scrollbar {
                    width: 10px;
                    height: 10px;
                    background-color: var(--background-fill-primary);
                }
                ::-webkit-scrollbar-thumb {
                    background-color: var(--background-fill-secondary);
                    border-radius: 5px;
                }
                ::-webkit-scrollbar-track {
                    background-color: var(--background-fill-primary);
                }
            """
        ) as self.interface:
            with gr.Tabs():
                with gr.Tab("Upload"):
                    file_input = gr.File(label="Select file to upload")
                    upload_button = gr.Button("Upload")
                    upload_output = gr.Textbox(label="Status")
                    upload_button.click(
                        fn=self.handle_upload,
                        inputs=[file_input],
                        outputs=[upload_output]
                    )
                with gr.Tab("URL Shortener"):
                    url_input = gr.Textbox(label="URL to Shorten")
                    shorten_button = gr.Button("Shorten")
                    url_output = gr.Textbox(label="Shortened URL")
                    shorten_button.click(
                        fn=self.handle_shorten,
                        inputs=[url_input],
                        outputs=[url_output]
                    )
                with gr.Tab("Paste"):
                    with gr.Row():
                        paste_title = gr.Textbox(label="Title")
                        paste_lang = gr.Textbox(label="Language")
                    paste_desc = gr.Textbox(label="Description")
                    paste_content = gr.TextArea(label="Content", lines=10)
                    paste_button = gr.Button("Create Paste")
                    paste_output = gr.Textbox(label="Paste URL")
                    paste_button.click(
                        fn=self.handle_paste,
                        inputs=[paste_content, paste_title, paste_desc, paste_lang],
                        outputs=[paste_output]
                    )
                with gr.Tab("History"):
                    history_output = gr.Dataframe(
                        headers=["Time", "Type", "URL", "Deletion URL", "Status"],
                        label="Upload History"
                    )
                    with gr.Row():
                        refresh_button = gr.Button("Refresh History")
                        loading_indicator = gr.Textbox(
                            label="Status",
                            value="",
                            interactive=False
                        )
                    refresh_button.click(
                        fn=self.get_history_data,
                        inputs=[],
                        outputs=[history_output, loading_indicator]
                    )
                with gr.Tab("Purge"):
                    gr.Markdown("""
                    # 🚨 WORK IN PROGRESS 🚨
                    ## This feature is currently NOT FUNCTIONAL
                    The purge functionality is still under development and may not work as expected.
                    Please do not rely on this feature for deleting files at this time.

                    ---

                    # ⚠️ Warning
                    This will permanently delete all your uploads that have valid deletion URLs.
                    This action cannot be undone.
                    """)
                    with gr.Row():
                        confirmation = gr.Textbox(
                            label="Type 'CONFIRM' to proceed",
                            placeholder="CONFIRM"
                        )
                        purge_button = gr.Button("Purge All", variant="stop")
                    purge_status = gr.Textbox(label="Status")
                    
                    purge_button.click(
                        fn=self.purge_all,
                        inputs=[confirmation],
                        outputs=[purge_status]
                    )

    def check_deletion_url(self, url):
        """Check if a deletion URL is still valid with caching"""
        if url in self.url_validity_cache:
            return self.url_validity_cache[url]

        try:
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            deletion_key = params.get('key', [''])[0]
            
            if not deletion_key:
                self.url_validity_cache[url] = False
                return False

            check_url = f"https://api.e-z.host/files/exists?key={deletion_key}"
            response = requests.get(check_url, headers={
                'key': API_KEY
            })
            
            result = False
            if response.status_code == 200:
                data = response.json()
                result = data.get('exists', False)
            self.url_validity_cache[url] = result
            return result
        except Exception as e:
            print(f"Error checking URL validity: {e}")
            self.url_validity_cache[url] = False
            return False

    def get_history_data(self):
        """Get history data with validity check and progress indication"""
        try:
            self.load_history()
            validated_history = []
            total_items = len(self.history)
            
            for index, item in enumerate(self.history, 1):
                deletion_url = item.get('deletionUrl', '')
                status = "Valid" if deletion_url and self.check_deletion_url(deletion_url) else "Invalid/Expired"
                
                validated_history.append([
                    item.get('timestamp', ''),
                    self.get_item_type(item),
                    item.get('imageUrl') or item.get('shortenedUrl') or item.get('pasteUrl', ''),
                    deletion_url,
                    status
                ])
                if index % 5 == 0:
                    yield validated_history, f"Processing... {index}/{total_items}"
            
            return validated_history, "Complete!"
        except Exception as e:
            return [], f"Error: {str(e)}"

    def purge_all(self, confirmation):
        """Purge all valid items from history"""
        if confirmation != "CONFIRM":
            return "Please type 'CONFIRM' to proceed with purge"
        self.load_history()
        initial_count = len(self.history)
        deleted_count = 0
        failed_count = 0
        new_history = []
        for item in self.history:
            deletion_url = item.get('deletionUrl')
            if deletion_url and self.check_deletion_url(deletion_url):
                try:
                    result = delete_file(deletion_url)
                    if result and result.get('success', False):
                        deleted_count += 1
                        continue
                    failed_count += 1
                except:
                    failed_count += 1
            new_history.append(item)
        
        self.history = new_history
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        
        return f"""Purge completed:
- Initial items: {initial_count}
- Successfully deleted: {deleted_count}
- Failed to delete: {failed_count}
- Remaining items: {len(new_history)}"""

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def save_history(self, result):
        result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append(result)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_item_type(self, item):
        if 'imageUrl' in item:
            return 'File'
        elif 'shortenedUrl' in item:
            return 'URL'
        elif 'pasteUrl' in item:
            return 'Paste'
        return 'Unknown'

    def handle_upload(self, file):
        if not file:
            return "No file selected!"
        try:
            result = upload_file(file.name)
            if result:
                self.save_history(result)
                return f"Upload successful!\nURL: {result.get('imageUrl', '')}"
            return "Upload failed!"
        except Exception as e:
            return f"Error: {str(e)}"

    def handle_shorten(self, url):
        if not url:
            return "Please enter a URL!"
        if not url.startswith(('http://', 'https://')):
            return "Invalid URL! Please include http:// or https://"
        result = shorten_url(url)
        if not result:
            return "Shortening failed! Please check the console for details."
        if 'error' in result:
            return f"Error: {result['error']}"
            
        shortened = result.get('shortenedUrl')
        if shortened:
            self.save_history(result)
            return shortened
        return "Shortening failed! Could not get shortened URL from response."

    def handle_paste(self, content, title, desc, lang):
        if not content:
            return "Please enter content!"
        result = create_paste(
            text=content,
            title=title,
            description=desc,
            language=lang
        )
        if result:
            self.save_history(result)
            return result.get('pasteUrl', '')
        return "Paste creation failed!"

    def run(self, share=False):
        self.interface.launch(
            share=share,
            show_api=False,
            show_error=True,
            favicon_path=None
        )

if __name__ == "__main__":
    interface = EZHostInterface()
    interface.run()
