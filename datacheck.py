import pyrebase

config = {
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain",
    "databaseURL": "https://fir-ologi-default-rtdb.firebaseio.com/",
    "storageBucket": "your-storage-bucket"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Example: Pushing data to the database
data = {"name": "John Doe", "age": 30}
db.child("users").push(data)

# Example: Retrieving data from the database
user = db.child("users").get()
if user.val() is None:
    print("No data found at this path")
else:
    print(user.val())
