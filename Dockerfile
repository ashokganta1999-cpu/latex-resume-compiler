FROM texlive/texlive:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 10000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:10000", "app:app"]
