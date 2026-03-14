import os
from vu_sports import create_app

app = create_app()
host = os.environ.get("HOST")
port = os.environ.get("PORT", 5000)

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
