import streamlit as st
import google.generativeai as genai
import tempfile
import os
import subprocess
import time

# Page configuration
st.set_page_config(layout="wide")
st.title("AI Web App Generator")

def generate_prompt(description):
    return f"""Create a complete web application based on this description: {description}

Requirements:
- Create a single HTML file that includes all CSS and JavaScript
- Use vanilla JavaScript (no frameworks/libraries needed)
- Store data in localStorage if persistence is needed
- Add clear comments explaining the code
- Make the code complete and ready to run in a browser
- Include responsive design for mobile/desktop
- Use modern HTML5 and CSS3 features
- Ensure good user experience and error handling

Return only the HTML code (with embedded CSS and JavaScript) without any explanations."""

def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-pro')

def find_free_port(start_port=5000, max_tries=100):
    """Find a free port starting from start_port."""
    import socket
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError("Could not find a free port")

def save_and_run_app(code):
    # Kill any existing Python HTTP servers (skip on Windows)
    if os.name != "nt":
        subprocess.run(["pkill", "-f", "python -m http.server"], stderr=subprocess.DEVNULL)
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    app_path = os.path.join(temp_dir, "index.html")
    
    # Clean up the code by removing markdown code fence if present
    code = code.strip()
    if code.startswith("```html"):
        code = code[len("```html"):].strip()
    if code.startswith("```"):
        code = code[3:].strip()
    if code.endswith("```"):
        code = code[:-3].strip()
    
    # Save the generated code
    with open(app_path, "w", encoding="utf-8") as f:
      f.write(code)
    
    # Find a free port and start the server
    port = find_free_port()
    process = subprocess.Popen(
        ["python", "-m", "http.server", str(port)],
        cwd=temp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start and verify it's running
    time.sleep(1)
    if process.poll() is not None:
        # Server failed to start, get the error
        _, stderr = process.communicate()
        raise RuntimeError(f"Server failed to start: {stderr.decode()}")
    
    return process, f"http://localhost:{port}"

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("Generate Your Web App")
    
    # User inputs
    st.info("This app generates simple web applications using HTML, CSS, and vanilla JavaScript (no frameworks/libraries needed). Perfect for creating interactive single-page applications!")
    
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    app_description = st.text_area(
        "Describe your web app:",
        "Create a simple todo list app where users can add and remove tasks.",
        height=150
    )
    
    if st.button("Generate & Run App"):
        if not api_key or not app_description:
            st.error("Please enter both API key and app description.")
        else:
            try:
                # Setup Gemini and generate code
                model = setup_gemini(api_key)
                prompt = generate_prompt(app_description)
                
                with st.spinner("Generating your web app..."):
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        # Display generated code
                        st.subheader("Generated Code")
                        st.code(response.text, language="python")
                        
                        # Run the app
                        with col2:
                            st.header("Live Preview")
                            try:
                                with st.spinner("Starting the server..."):
                                    process, url = save_and_run_app(response.text)
                                    
                                # Check if the process is still running
                                if process.poll() is None:
                                    st.success(f"App is running at {url}")
                                    st.info("⚠️ For the best experience, please open the app in a new tab to test all features properly.")
                                    st.markdown(
                                        f'<iframe src="{url}" width="100%" height="600px" sandbox="allow-scripts allow-forms"></iframe>',
                                        unsafe_allow_html=True
                                    )
                                    st.markdown(f'[Open in new tab]({url})', unsafe_allow_html=True)
                                else:
                                    st.error("Failed to start the web server. Please try again.")
                            except Exception as e:
                                st.error(f"Error running the app: {str(e)}")
                    else:
                        st.error("No code was generated. Please try again.")
                        
            except Exception as e:
                st.error(f"Error generating code: {str(e)}")

with col2:
    st.header("Preview")
    st.info("Generate an app to see the preview here!")
