import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SOURCE_CHAT_ID = -1003866378383
DEST_CHAT_ID = -1003886620765

TOPIC_MAP = {
    998: 4,       # Libros en español
    11217: 5,     # Libros en inglés
    8045: 7,      # Series
    10504: 6,     # Películas
    9: 8,         # Audiolibros
    11581: 9,     # Audiolibros en inglés
    13: 11        # Reglas
}

API = f"https://api.telegram.org/bot{TOKEN}"


def copiar_mensaje(message):
    source_thread = message.get("message_thread_id")

    if source_thread not in TOPIC_MAP:
        return

    destination_thread = TOPIC_MAP[source_thread]

    data = {
        "chat_id": DEST_CHAT_ID,
        "from_chat_id": SOURCE_CHAT_ID,
        "message_id": message["message_id"],
        "message_thread_id": destination_thread
    }

    response = requests.post(
        f"{API}/copyMessage",
        data=data,
        timeout=30
    )

    if not response.ok:
        print("Error:", response.text)


def main():
    offset = None

    while True:
        try:
            params = {
                "timeout": 50,
                "allowed_updates": ["message"]
            }

            if offset is not None:
                params["offset"] = offset

            response = requests.get(
                f"{API}/getUpdates",
                params=params,
                timeout=60
            )

            data = response.json()

            for update in data.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if not message:
                    continue

                if message.get("chat", {}).get("id") != SOURCE_CHAT_ID:
                    continue

                copiar_mensaje(message)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
