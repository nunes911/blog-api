from app import create_app


new_app = create_app()
new_app.run(host="0.0.0.0", port=5000)
