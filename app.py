from flask import Flask, render_template, request

app = Flask(__name__)

import re

def clean_text(text, phrase1, phrase2):

    if not text:
        return text

    # Remove between start and end markers
    if phrase1 and phrase2:
        start = re.escape(phrase1)
        end = re.escape(phrase2)

        pattern = start + r".*?" + end

        cleaned = re.sub(pattern, "", text, flags=re.DOTALL)
    elif phrase1 and phrase2 is None:
        pattern = re.escape(phrase1)
        cleaned = re.sub(pattern, "", text)

    else:
        cleaned = text

    cleaned = re.sub(r'\n\s*\n', '\n', cleaned).strip()

    return cleaned


@app.route("/", methods=["GET", "POST"])
def index():
    cleaned_text = ""
    original_text = ""

    if request.method == "POST":
        original_text = request.form.get("text", "")
        removal_type = request.form.get("removal_type")

        phrase1 = request.form.get("phrase1") or None
        phrase2 = request.form.get("phrase2") or None
        single_phrase = request.form.get("single_phrase") or None

        if removal_type == "markers":
            cleaned_text = clean_text(original_text, phrase1, phrase2)

        elif removal_type == "phrase":
            cleaned_text = clean_text(original_text, single_phrase, None)

    return render_template("index.html",
                           cleaned_text=cleaned_text,
                           original_text=original_text)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
