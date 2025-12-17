from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the application on localhost port 5000
    app.run(debug=True)
