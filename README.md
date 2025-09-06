# AI Web App Generator

A Streamlit app that generates complete, self-contained web applications using HTML, CSS, and JavaScript. Simply describe what you want, and get a working web app instantly!

## Features

- Generate complete web apps from natural language descriptions
- Pure HTML/CSS/JavaScript - no frameworks or dependencies needed
- Instant preview in the browser
- Client-side storage using localStorage
- Responsive design for all devices
- Modern HTML5 and CSS3 features

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```
3. Enter your Gemini API key and describe your web app
4. Click 'Generate & Run App' to see it in action

## Example Prompts

- "Create a todo list app where users can add and remove tasks"
- "Create a calculator with a clean modern design"
- "Create a notes app that saves to localStorage"
- "Create a simple drawing app with different colors"

## Technical Details

- Uses Gemini API for code generation
- Generates single-file applications (HTML/CSS/JS)
- Preview served using Python's built-in HTTP server
- All data stored in the browser's localStorage

## Limitations
- Client-side only (no server-side features)
- Storage limited to browser's localStorage
- Gemini API key required for generation

## Future Plans
- Add example templates gallery
- Adding backend and db support
- Adding support for enhancing the web app dynamically with succesive user prompts
- Export functionality for downloading apps
- More interactive preview features
