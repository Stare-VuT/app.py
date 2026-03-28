cd /storage/emulated/0/Android/data/ru.iiec.pydroid3/files/login-system

cat > app.py << 'EOF'
from flask import Flask

print(">>> APP STARTING...")

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask local OK"

if __name__ == "__main__":
    print(">>> RUNNING FLASK...")
    app.run(host="0.0.0.0", port=5000, debug=True)
EOF
