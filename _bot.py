import pyautogui
import pyperclip
import time
from google import genai


import pyautogui
import pyperclip
import time
import re
from google import genai


CHAT_AREA_START = (484, 125)
CHAT_AREA_END = (691, 922)
MESSAGE_BOX = (743, 981)
OPEN_CHAT_CLICK = (1221, 1038)

MY_NAME = "Pranay Kadam"
client = genai.Client(api_key="your_actual_api_key_here")

pyautogui.PAUSE = 0.3


def get_last_sender_name(chat_log):
    chat_log = chat_log.strip()

    if not chat_log:
        return ""

    matches = re.findall(
        r"\[\d{1,2}:\d{2}\s*(?:am|pm),\s*\d{2}/\d{2}/\d{4}\]\s*(.*?):",
        chat_log,
        flags=re.IGNORECASE
    )

    if matches:
        return matches[-1].strip()

    return ""


def get_latest_message(chat_log):
    chat_log = chat_log.strip()

    if not chat_log:
        return ""

    parts = re.split(
        r"\[\d{1,2}:\d{2}\s*(?:am|pm),\s*\d{2}/\d{2}/\d{4}\]",
        chat_log,
        flags=re.IGNORECASE
    )

    if len(parts) > 1:
        return parts[-1].strip()

    return ""


def copy_whatsapp_chat():
    pyautogui.moveTo(
        CHAT_AREA_START[0],
        CHAT_AREA_START[1],
        duration=0.3
    )

    pyautogui.dragTo(
        CHAT_AREA_END[0],
        CHAT_AREA_END[1],
        duration=1.0,
        button="left"
    )

    time.sleep(0.5)

    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.8)

    chat_history = pyperclip.paste().strip()

    pyautogui.click(
        MESSAGE_BOX[0],
        MESSAGE_BOX[1]
    )

    time.sleep(0.3)

    return chat_history


def generate_reply(chat_history):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": (
                "You are Pranay Kadam. "
                "You speak Marathi, Hindi, and English naturally. "
                "You are from India and you are a coder. "
                "Read the WhatsApp chat history and reply like Pranay. "
                "Keep the reply short and natural. "
                "Return only the WhatsApp reply text. "
                "Do not add explanations, headings, quotes, or extra text."
            )
        },
        contents=chat_history
    )

    return response.text.strip()


def send_whatsapp_message(message):
    pyperclip.copy(message)

    pyautogui.click(
        MESSAGE_BOX[0],
        MESSAGE_BOX[1]
    )

    time.sleep(0.5)

    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)

    pyautogui.press("enter")


last_processed_message = ""

print("WhatsApp auto reply bot started.")
print("It replies to everyone except messages sent by you.")
print("Press Ctrl + C in terminal to stop the bot.")

pyautogui.click(
    OPEN_CHAT_CLICK[0],
    OPEN_CHAT_CLICK[1]
)

time.sleep(2)

while True:
    try:
        chat_history = copy_whatsapp_chat()

        if not chat_history:
            print("No chat history copied.")
            time.sleep(3)
            continue

        print("\n---------------- CHAT HISTORY ----------------")
        print(chat_history)
        print("------------------------------------------------")

        last_sender = get_last_sender_name(chat_history)
        latest_message = get_latest_message(chat_history)

        if last_sender and last_sender.lower() != MY_NAME.lower():
            if latest_message != last_processed_message:
                print("\nNew message from:", last_sender)
                print("Message:", latest_message)

                reply = generate_reply(chat_history)

                print("\nPranay reply:", reply)

                if reply:
                    send_whatsapp_message(reply)
                    last_processed_message = latest_message
        else:
            print("Last message is from you, so bot will not reply.")

        time.sleep(3)

    except KeyboardInterrupt:
        print("\nBot stopped manually.")
        break

    except Exception as error:
        print("\nError:", error)
        time.sleep(3)