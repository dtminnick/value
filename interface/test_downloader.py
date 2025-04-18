
from downloader import Downloader
from messenger import Messenger

msg_handler = Messenger()

downloader = Downloader(msg_handler)

# Generate test list of dict to simulate query result.

sample_data = [
    {
        "user_id": 101,
        "username": "jdoe",
        "email": "jdoe@example.com",
        "action": "login",
        "timestamp": "2025-04-17 08:15:23"
    },
    {
        "user_id": 102,
        "username": "asmith",
        "email": "asmith@example.com",
        "action": "file_upload",
        "timestamp": "2025-04-17 08:17:01"
    },
    {
        "user_id": 103,
        "username": "mjohnson",
        "email": "mjohnson@example.com",
        "action": "logout",
        "timestamp": "2025-04-17 08:18:55"
    },
    {
        "user_id": 101,
        "username": "jdoe",
        "email": "jdoe@example.com",
        "action": "download",
        "timestamp": "2025-04-17 08:20:10"
    },
    {
        "user_id": 104,
        "username": "kwilliams",
        "email": "kwilliams@example.com",
        "action": "password_change",
        "timestamp": "2025-04-17 08:21:42"
    }
]

downloader.download(sample_data, "Test Download Sample Data")
