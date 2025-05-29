"""Entry point for src folder"""
from app.app import create_app

def main():
    """Run the Flask application"""
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()