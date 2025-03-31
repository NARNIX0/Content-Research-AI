# Instagram Research Tool MVP

This tool automates the process of searching Instagram for videos with 1M+ views based on provided keywords.

## Prerequisites

- Python 3.x
- Chrome browser installed
- Instagram account credentials

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Instagram credentials:
   - Open the `.env` file
   - Replace `your_username` with your Instagram username
   - Replace `your_password` with your Instagram password

3. Run the environment check to make sure everything is configured correctly:
```bash
python check_setup.py
```

## Usage

1. Run the script:
```bash
python instagram_research.py
```

2. The script will:
   - Log in to Instagram
   - Search for each keyword
   - Find videos with 1M+ views
   - Log the results to `instagram_research.log`

## Features

- Automated Instagram login
- Keyword-based search
- Reels tab navigation
- View count filtering (1M+ views)
- Progress logging
- Error handling

## Troubleshooting

If you encounter errors related to ChromeDriver:

1. **Driver not found**: The script will now attempt to use the Chrome browser directly without needing a separate ChromeDriver installation.

2. **Win32 application error**: This usually happens when there's a mismatch between your Chrome version and the ChromeDriver. The updated script handles this automatically.

3. **Browser crashes**: If the browser crashes, try running the check_setup.py script to verify your environment.

## Notes

- The script includes basic error handling and logging
- Results are logged to `instagram_research.log`
- The script will collect at least 5 videos per keyword
- Instagram's interface may change, requiring updates to the selectors 