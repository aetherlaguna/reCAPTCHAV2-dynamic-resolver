# Advanced Selenium reCAPTCHA v2 Solver

This Python script is an advanced attempt to programmatically solve Google's reCAPTCHA v2 using Selenium. It employs several techniques to mimic human behavior and bypass common anti-bot detections.

The primary goal is to authenticate on a target website and acquire a session cookie, demonstrating a complete login/authentication cycle.

### Disclaimer

⚠️ **This script is for educational and experimental purposes only.** Automating interactions with websites may be against their Terms of Service. The user assumes all responsibility for using this script. reCAPTCHA is an evolving technology designed specifically to block bots; therefore, **this script is not guaranteed to work** and may fail if the website's security measures are updated.

## Features

-   **Stealth Mode:** Uses `selenium-stealth` to modify the WebDriver's properties, making it harder to detect as a bot.
-   **Human-like Delays:** Incorporates randomized delays to simulate human thinking and interaction time.
-   **Overlay Removal:** Automatically detects and removes invisible overlay `div` elements that are designed to block automated clicks.
-   **Audio Challenge Solver:** Utilizes `pypasser` to attempt solving the reCAPTCHA via the audio challenge.
-   **Cookie Verification:** Actively monitors browser cookies to confirm a successful solution by checking for the presence of a specific session cookie.

## Requirements

-   Python 3.7+
-   Google Chrome browser installed on your system.
-   `ffmpeg`: The `pypasser` library requires `ffmpeg` for audio processing. You must install it on your system and ensure it's available in your system's PATH.
    -   **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your Environment Variables.
    -   **macOS (Homebrew):** `brew install ffmpeg`
    -   **Linux (apt):** `sudo apt-get install ffmpeg`

## Installation

1.  Clone this repository or download the `recaptcha_scrapper.py` file.

2.  It is highly recommended to create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  Create a `requirements.txt` file with the following content:
    ```
    selenium
    webdriver-manager
    selenium-stealth
    pypasser
    SpeechRecognition
    pydub
    ```

4.  Install all the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Configure the Target:** The script is currently hardcoded to target `https://portalbnmp.cnj.jus.br/#/captcha/`. You can change this URL by modifying the `driver.get(...)` line in the script.

2.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python recaptcha_scrapper.py
    ```

### Debugging

To see what the browser is doing in real-time, you can run it in "headed" (non-headless) mode. This is **essential for diagnosing issues**.

To do this, comment out the headless option in the script:
```python
# Find this line
options.add_argument('--headless=new')

# And comment it out
# options.add_argument('--headless=new') 
```

## How It Works

The script follows a logical sequence of steps to bypass the reCAPTCHA:
1.  **Initialization:** Launches a Selenium Chrome WebDriver with `selenium-stealth` options enabled.
2.  **Navigation:** Opens the target URL.
3.  **Checkbox Click:** Locates the reCAPTCHA `iframe` and clicks the "I'm not a robot" checkbox.
4.  **Overlay Handling:** After the click, it switches back to the main page content and actively searches for and removes any invisible `div` overlays that would intercept clicks meant for the challenge `iframe`.
5.  **Challenge Attempt:** It calls `pypasser` to find and solve the audio version of the reCAPTCHA challenge.
6.  **Verification:** After the attempt, it enters a loop to check for the presence of the `portalbnmp` session cookie, which signals a successful login.

## Troubleshooting & Known Limitations

This script can fail for several reasons. Here are the most common errors and their meanings:

#### Error: `Pypasser failed with error: list index out of range`

-   **Cause:** This is the most likely failure mode. It means that Google's anti-bot detection was successful. Instead of presenting an audio challenge (which `pypasser` can solve), it presented an **image challenge** (e.g., "select all squares with traffic lights"). `pypasser` cannot find the "get an audio challenge" button, resulting in an empty list and this error.
-   **Solution:** Run the script in non-headless mode to visually confirm you are being served an image challenge. If so, **this script cannot solve it.**

#### Error: `ElementClickInterceptedException`

-   **Cause:** An element (usually an invisible overlay) is covering the element the script is trying to click.
-   **Solution:** The script already contains a mechanism to remove a common type of overlay. If this error still occurs, the site may have implemented a new or different overlay. You would need to inspect the page source to identify and remove the new blocking element.

### The Ultimate Solution: When This Script Fails

If you consistently receive an image challenge, it means the target website's security is too strong for this method. The industry-standard solution for robust CAPTCHA solving is to integrate a **third-party CAPTCHA-solving service** (e.g., 2Captcha, Anti-Captcha). These services use human workers to solve CAPTCHAs via an API and are far more reliable, though they are paid services.