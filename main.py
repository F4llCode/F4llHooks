import requests
import time
from termcolor import colored
import os
import subprocess
from config import WEBHOOKS_FILE


def display_ascii_art():
    banner = """
    ███████ ██   ██ ██      ██      ██   ██  ██████   ██████  ██   ██ ███████ 
    ██      ██   ██ ██      ██      ██   ██ ██    ██ ██    ██ ██  ██  ██      
    █████   ███████ ██      ██      ███████ ██    ██ ██    ██ █████   ███████ 
    ██           ██ ██      ██      ██   ██ ██    ██ ██    ██ ██  ██       ██ 
    ██           ██ ███████ ███████ ██   ██  ██████   ██████  ██   ██ ███████ 

    """

    print(colored(banner, "green"))


def send_webhook_message(webhook_url, message_content, num_times, delay_seconds):
    for _ in range(num_times):
        response = requests.post(
            webhook_url,
            json={"content": message_content},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 204:
            print(colored("Message sent successfully!", "green"))

        else:
            print(
                colored(
                    f"Failed to send message. Status code: {response.status_code}",
                    "red",
                )
            )

        time.sleep(delay_seconds)


def save_webhook_to_file(webhook_url):
    with open(WEBHOOKS_FILE, "a") as file:
        file.write(webhook_url + "\n")

    print(colored(f"Webhook saved to {WEBHOOKS_FILE}!", "yellow"))


def load_webhook_from_file():
    webhooks = []

    if os.path.exists(WEBHOOKS_FILE):
        with open(WEBHOOKS_FILE, "r") as file:
            webhooks = file.read().splitlines()
    return webhooks


def remove_webhook_from_file(webhook_url):
    webhooks = load_webhook_from_file()

    if webhook_url in webhooks:
        webhooks.remove(webhook_url)

        with open(WEBHOOKS_FILE, "w") as file:
            file.write("\n".join(webhooks))
        print(colored(f"Webhook removed from {WEBHOOKS_FILE}!", "yellow"))
    else:
        print(colored("Webhook not found in the file.", "red"))


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def get_user_input(prompt, input_type=str):
    while True:
        try:
            user_input = input(f"{prompt}: ")
            if user_input.lower() == "exit":
                print(colored("Exiting the tool. Goodbye!", "yellow"))
                exit()
            return input_type(user_input)
        except ValueError:
            print(colored("Invalid input. Please enter a valid value.", "yellow"))


def main():
    while True:
        display_ascii_art()
        webhooks = load_webhook_from_file()
        print("\nOptions:")
        print("1. Send webhook message")
        print("2. Save webhook to file")
        print("3. Remove webhook from file")
        print("4. Exit")
        choice = get_user_input("Enter your choice", int)
        if choice == 1:
            print("\nLoaded webhooks:")
            for i, webhook in enumerate(webhooks, start=1):
                print(f"{i}. {webhook}")
            webhook_choice = get_user_input("Choose a webhook (number)", int)
            selected_webhook = webhooks[webhook_choice - 1]
            message = get_user_input("Message")
            num_times = get_user_input("Number of times to send the message", int)
            delay_seconds = get_user_input(
                "Delay in seconds between each request", float
            )
            send_webhook_message(selected_webhook, message, num_times, delay_seconds)
        elif choice == 2:
            new_webhook = get_user_input("Enter the webhook URL")
            save_webhook_to_file(new_webhook)
        elif choice == 3:
            print("\nLoaded webhooks:")
            for i, webhook in enumerate(webhooks, start=1):
                print(f"{i}. {webhook}")
            webhook_choice = get_user_input("Choose a webhook to remove (number)", int)
            selected_webhook = webhooks[webhook_choice - 1]
            remove_webhook_from_file(selected_webhook)

        elif choice == 4:
            print(colored("Exiting the tool. Goodbye!", "yellow"))
            exit()

        clear_console()


if __name__ == "__main__":
    main()
