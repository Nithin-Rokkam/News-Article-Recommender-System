from app import app, load_model

if __name__ == "__main__":
    print("Loading model...")
    load_model()
    print("Model loaded successfully!")
    app.run() 