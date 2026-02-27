from flask import Flask, request, send_file, jsonify
import subprocess, tempfile, pathlib

app = Flask(__name__)

@app.post("/compile")
def compile():
    data = request.get_json(force=True)
    latex = data.get("latex", "")
    if not latex.strip():
        return jsonify({"error": "Missing latex"}), 400

    work = pathlib.Path(tempfile.mkdtemp())
    (work / "resume.tex").write_text(latex, encoding="utf-8")

    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "resume.tex"]
    p = subprocess.run(cmd, cwd=str(work), capture_output=True, text=True)

    pdf_path = work / "resume.pdf"
    if p.returncode != 0 or not pdf_path.exists():
        err = (p.stdout + "\n" + p.stderr)[-4000:]
        return jsonify({"error": "LaTeX compile failed", "log_tail": err}), 400

    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="resume.pdf")
