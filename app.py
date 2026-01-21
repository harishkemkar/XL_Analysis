import os
from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from analysis_utils.analyzer import analyze_file, analyze_selected_columns

# Flask app setup
app = Flask(__name__)
app.secret_key = "supersecretkey"   # Needed for flash messages

# Config: always use absolute path for uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"xlsx"}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in request.")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Read Excel file into DataFrame
            df = pd.read_excel(filepath)

            # Run analysis
            summary = analyze_file(df)

            return render_template(
                "report.html",
                summary=summary,
                columns=df.columns,
                filename=file.filename
            )
        else:
            flash("Invalid file type. Please upload an .xlsx file.")
            return redirect(request.url)

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_columns():
    """Analyze specific columns selected by user."""
    selected_columns = request.form.getlist("columns")
    filename = request.form.get("filename")
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(filepath):
        flash("Uploaded file not found.")
        return redirect(url_for("index"))

    df = pd.read_excel(filepath)

    # Base summary
    summary = analyze_file(df)

    # Add detailed analysis of selected columns
    summary["selected_columns"] = analyze_selected_columns(df, selected_columns)

    return render_template(
        "report.html",
        summary=summary,
        columns=df.columns,
        filename=filename
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)