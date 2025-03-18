import openai
import requests
import config

from flask import Flask, render_template, request, session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = "replace_with_a_random_secret_key"  # Required for session usage

# -----------------------------------------
# Determine Active Model & Key
# -----------------------------------------
ACTIVE_MODEL = config.ACTIVE_MODEL.lower()

if ACTIVE_MODEL == "openai":
    openai.api_key = config.GPT4O_API_KEY
    MODEL_NAME = "gpt-4"  # or "gpt-3.5-turbo" if desired
elif ACTIVE_MODEL == "gemini":
    # If using Gemini, ensure GEMINI_API_KEY is uncommented in config.py
    GEMINI_API_KEY = config.GEMINI_API_KEY
    MODEL_NAME = "gemini-2"
elif ACTIVE_MODEL == "claude":
    # If using Claude, ensure CLAUDE_API_KEY is uncommented in config.py
    CLAUDE_API_KEY = config.CLAUDE_API_KEY
    MODEL_NAME = "claude-3.5"
else:
    raise ValueError("Invalid model selection in config.py. Use 'openai', 'gemini', or 'claude'.")


def query_ai_model(user_input):
    """
    Sends user_input to the chosen AI model and returns the response text.
    """
    # Common parameters
    max_tokens = config.MAX_TOKENS
    temperature = config.TEMPERATURE

    # ------------- OpenAI GPT-4o -------------
    if ACTIVE_MODEL == "openai":
        if not openai.api_key:
            return "Error: OpenAI API key not found in config."
        try:
            # We'll send the entire conversation (stored in session) to preserve context
            conversation_history = session.get("conversation", [])
            # Append current user query
            conversation_history.append({"role": "user", "content": user_input})

            completion = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=conversation_history,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            response_text = completion.choices[0].message.content
            # Add assistant message to conversation
            conversation_history.append({"role": "assistant", "content": response_text})
            # Save back to session
            session["conversation"] = conversation_history

            return response_text
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"

    # ------------- Google Gemini 2.0 -------------
    elif ACTIVE_MODEL == "gemini":
        try:
            # Example endpoint (subject to change)
            url = "https://generativelanguage.googleapis.com/v1/models/gemini-2:generateText"
            headers = {"Content-Type": "application/json"}
            params = {"key": GEMINI_API_KEY}
            data = {
                "prompt": {"text": user_input},
                "maxTokens": max_tokens,
                "temperature": temperature,
            }
            response = requests.post(url, headers=headers, params=params, json=data)
            response.raise_for_status()
            response_json = response.json()
            candidates = response_json.get("candidates", [])
            if not candidates:
                return "No response from Gemini."
            return candidates[0].get("content", "No text from Gemini response.")
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

    # ------------- Anthropic Claude 3.5/3.7 -------------
    elif ACTIVE_MODEL == "claude":
        try:
            # Example Anthropic endpoint (subject to change)
            url = "https://api.anthropic.com/v1/complete"
            headers = {
                "x-api-key": CLAUDE_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "model": MODEL_NAME,
                "max_tokens_to_sample": max_tokens,
                "prompt": f"\n\nHuman: {user_input}\n\nAssistant:",
                "temperature": temperature,
            }
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("completion", "No completion text from Claude.")
        except Exception as e:
            return f"Error calling Claude API: {str(e)}"

    return "No valid AI model selected or no response."


@app.route("/", methods=["GET", "POST"])
def chat():
    """
    Route for RAMbo's AI chat interface with conversation memory.
    """
    # Ensure conversation is initialized
    if "conversation" not in session:
        session["conversation"] = []

    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            response_text = query_ai_model(user_input)

    # We'll display the entire conversation in index.html
    conversation_history = session["conversation"]
    return render_template(
        "index.html",
        conversation=conversation_history,
        response=response_text,
    )


@app.route("/browse", methods=["GET", "POST"])
def browse():
    """
    Route for browsing a webpage using Selenium and summarizing its content with the AI model.
    """
    page_summary = ""
    url = ""
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=chrome_options)

            try:
                driver.get(url)
                page_source = driver.page_source
            except Exception as e:
                page_source = f"Error loading URL: {str(e)}"
            finally:
                driver.quit()

            snippet = page_source[:1000]  # Limit how much we send to the AI
            summary_prompt = f"Summarize this webpage snippet:\n\n{snippet}"

            page_summary = query_ai_model(summary_prompt)

    return render_template("browse.html", url=url, page_summary=page_summary)


if __name__ == "__main__":
    app.run(debug=True)
