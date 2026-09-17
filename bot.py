import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SOURCE_CHAT_ID = -1003866378383
DEST_CHAT_ID = -1003886620765

TOPIC_MAP = {
    998: 4,
    11217: 5,
    8045: 7,
    10504: 6,
    9: 8,
    11581: 9,
    13: 11
}

API = f"https://api.telegram.org/bot{TOKEN}"


def copiar_mensaje(message):
    chat = message.get("chat", {})
    thread = message.get("message_thread_id")

    print(
        f"Mensaje recibido: chat={chat.get('id')} "
        f"thread={thread} "
        f"message_id={message.get('message_id')}",
        flush=True
    )

    if chat.get("id") != SOURCE_CHAT_ID:
        return

    if thread not in TOPIC_MAP:
        print("Tema ignorado", flush=True)
        return

    destino = TOPIC_MAP[thread]

    respuesta = requests.post(
        f"{API}/copyMessage",
        data={
            "chat_id": DEST_CHAT_ID,
            "from_chat_id": SOURCE_CHAT_ID,
            "message_id": message["message_id"],
            "message_thread_id": destino
        },
        timeout=30
    )

    print(
        f"Copia a tema {destino}: "
        f"{respuesta.status_code} {respuesta.text}",
        flush=True
    )


def main():
    offset = None

    print("BOT INICIADO", flush=True)

    while True:
        try:
            parametros = {
                "timeout": 50,
                "allowed_updates": ["message"]
            }

            if offset is not None:
                parametros["offset"] = offset

            respuesta = requests.get(
                f"{API}/getUpdates",
                params=parametros,
                timeout=60
            )

            datos = respuesta.json()

            print(
                f"getUpdates: ok={datos.get('ok')} "
                f"mensajes={len(datos.get('result', []))}",
                flush=True
            )

            for update in datos.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if message:
                    copiar_mensaje(message)

        except Exception as error:
            print(f"ERROR: {error}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
