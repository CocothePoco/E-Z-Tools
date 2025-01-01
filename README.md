# 🚀 E-Z DASH MANAGER

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-3.50+-F08080?style=for-the-badge&logo=python&logoColor=white)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/cocothepoco/E-Z-Tools/graphs/commit-activity)
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/ezhost)

<div align="center">
  
  ![GitHub repo size](https://img.shields.io/github/repo-size/cocothepoco/E-Z-Tools?style=flat-square)
  ![GitHub last commit](https://img.shields.io/github/last-commit/cocothepoco/E-Z-Tools?style=flat-square)
  ![GitHub issues](https://img.shields.io/github/issues/cocothepoco/E-Z-Tools?style=flat-square)
  ![GitHub pull requests](https://img.shields.io/github/issues-pr/cocothepoco/E-Z-Tools?style=flat-square)
  
</div>

A modern interface for E-Z.host file hosting service, featuring file uploads, URL shortening, and paste creation.

![E-Z Tools Interface BETA](screenshot.png)

## ✨ Features

- 📤 **File Upload**: Upload files to E-Z.host with ease
- 🔗 **URL Shortener**: Create shortened URLs
- 📝 **Paste Creation**: Share text with syntax highlighting
- 📊 **History Tracking**: Keep track of all your uploads
- 🗑️ **Bulk Purge**: Remove multiple files at once

## 🚀 Getting Started

### Prerequisites

```bash
pip install gradio requests
```

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/cocothepoco/E-Z-Tools.git
cd E-Z-Tools
```

2. Run the script:
```bash
python script.py
```

3. Open your browser to the displayed URL (usually http://127.0.0.1:7860)

## 💡 Usage

### File Upload
1. Go to the "Upload" tab
2. Click "Select file to upload" or drag & drop your file
3. Click "Upload"
4. Copy the provided URL

### URL Shortening
1. Navigate to the "URL Shortener" tab
2. Paste your long URL
3. Click "Shorten"
4. Use the shortened URL

### Creating Pastes
1. Go to the "Paste" tab
2. (Optional) Set a title and language for syntax highlighting
3. Enter your text content
4. Click "Create Paste"
5. Share the generated URL

### Managing History
- View all uploads in the "History" tab
- Click "Refresh History" to update the list
- Use the "Purge" tab to delete multiple files (use with caution)

## 🔑 API Configuration

The tool uses the E-Z.host API. To use your own API key:

1. Replace the API key in the enviroment file:
```python
API_KEY=
```

## 🛠️ Installation

### Automatic Setup (Windows)

1. Download or clone this repository
2. Double-click `Setup.bat`
3. Follow the on-screen instructions

### Manual Setup

1. Install Python 3.8 or newer
2. Clone the repository:
```bash
git clone https://github.com/cocothepoco/E-Z-Tools.git
cd E-Z-Tools
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the script:
```bash
python script.py
```

5. Open your browser to the displayed URL (usually http://127.0.0.1:7860)

## 🛟 Support

For support, please visit [E-Z.host Discord](https://discord.gg/ez) or open an issue in this repository.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [E-Z.host](https://e-z.host) for providing the file hosting service
- [Gradio](https://gradio.app) for the web interface framework
