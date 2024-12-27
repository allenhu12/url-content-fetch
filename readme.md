# Link Extractor

A GUI application for extracting links from HTML files and fetching their content using the Jina API.
For CLI version, please use
```
- install the python virtual env
- pip install requests
- pip install beautifulsoup4
```
`python link_extractor.py "Gemini (12_26_2024 6：03：40 PM).html" "output_links.txt" --api-key "jina_" --fetch-content`

## Features

- Extract URLs from HTML files
- Save URLs to text files
- Load existing URL files
- Fetch content for URLs using Jina API
- User-friendly GUI interface
- Preview URLs from loaded files
- Separate or combined operations

## Requirements

- Python 3.6+
- beautifulsoup4
- requests
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/link-extractor.git
cd link-extractor
2. Install dependencies:
pip install -r requirements.txt

## Usage

### Starting the Application

Run the application using:
python standalone_link_extractor.py


### GUI Components

1. **Input HTML File**
   - Click "Browse" to select an HTML file
   - Required only for URL extraction
   - Automatically suggests names for URL and content files

2. **URL File**
   - Two options available:
     - "Load": Load an existing URL file
     - "Save As": Choose where to save extracted URLs
   - When loading a URL file:
     - Displays preview of first 3 URLs
     - Shows total URL count
     - Automatically switches to content fetching mode

3. **Content File**
   - Specify where to save fetched content
   - Automatically suggested based on URL file name
   - Content is saved with clear separators between URLs

4. **API Key**
   - Enter your Jina API key
   - Required only for content fetching
   - Securely used for API authentication

5. **Operations**
   - Extract URLs: Extract links from HTML file
   - Fetch Content: Fetch content for URLs in file
   - Can select one or both operations

### Workflows

#### Extracting URLs from HTML

1. Click "Browse" next to "Input HTML File"
2. Select your HTML file
3. URL and content file names will be auto-suggested
4. Ensure "Extract URLs" is checked
5. Click "Run"
6. URLs will be saved to the specified file

#### Loading Existing URLs

1. Click "Load" next to "URL File"
2. Select your URL file
3. Preview of URLs will be shown in log area
4. Program automatically switches to content fetching mode

#### Fetching Content

1. Ensure you have a URL file (either extracted or loaded)
2. Enter your Jina API key
3. Specify content file location
4. Check "Fetch Content"
5. Click "Run"
6. Content will be saved with URL separators

### Tips

- You can modify the URL file between operations
- Content fetching has a 1-second delay between requests
- Log area shows real-time progress
- Status bar shows current operation
- Error messages provide specific guidance
- Files can be renamed before saving

### Common Operations

1. **Extract and Fetch**
   - Select HTML file
   - Check both operations
   - Enter API key
   - Click Run

2. **Fetch from Existing URLs**
   - Load URL file
   - Enter API key
   - Specify content file
   - Click Run

3. **Extract Only**
   - Select HTML file
   - Check "Extract URLs" only
   - Click Run

### Error Handling

The program will show error messages for:
- Missing input files
- Invalid API key
- Network issues
- File access problems
- Empty URL files

## Building Executable

To create a standalone executable:
pyinstaller standalone_link_extractor.spec


The executable will be created in the `dist` directory.

### Running the Executable

- Windows: Double-click `LinkExtractor.exe`
- macOS: Double-click `LinkExtractor.app`
- Linux: Run `LinkExtractor` executable

## Troubleshooting

1. **Program won't start**
   - Check Python installation
   - Verify dependencies are installed
   - Check file permissions

2. **Can't extract URLs**
   - Verify HTML file is readable
   - Check file encoding
   - Ensure proper file permissions

3. **Content fetching fails**
   - Verify API key is correct
   - Check internet connection
   - Verify URL format in file
   
## Source code structure
link-extractor/
├── standalone_link_extractor.py
├── standalone_link_extractor.spec
├── requirements.txt
├── README.md
└── .gitignore

## License
## Author

