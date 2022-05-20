# See readme.md for instructions on running this code.

from typing import Any, Dict

from zulip_bots.lib import BotHandler
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webbrowser import Chrome
import time
import schedule


class HelloWorldHandler:
    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        self.content = message["content"]
        self.sender_email = message["sender_email"]
        self.ttype = message["type"]
        self.stream_name = message["display_recipient"]
        self.stream_topic = message["subject"]

        self.restaurants = ["smarthouse", "garden", "galaxi"]

        if self.stream_topic == "ruokaketju":
            if self.content.lower() in self.restaurants: 
                bot_handler.send_message(bot_handler, self.get_lunch_data(self.content.lower()))
            else:
                comma = ", "
                bot_handler.send_message(bot_handler, f"Ei onnistu :cry: Validit komennot atm: {comma.join(f'{r.upper()}' for r in restaurants)}")
        else:
            bot_handler.send_message(bot_handler, "Väärä topic :sunglasses:")

        schedule.every().day.at("13:00").do(self.recurring_message, bot_handler)
        schedule.run_pending()
        time.sleep(60)

        return

    def recurring_message(self, bot_handler):
        message = ":food: Päivän ruokalistat :food:"
        for restaurant in self.restaurants:
            message += f"\n\n:food: {restaurant.upper()} :food: \n\n {self.get_lunch_data(restaurant)}"

        bot_handler.send_message(bot_handler, message)

    def get_lunch_data(self, restaurant):
        message = ""
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if restaurant == "smarthouse":
            driver.get("https://www.foodandco.fi/ravintolat/Ravintolat-kaupungeittain/oulu/smarthouse/")
            smarthouse_data = driver.find_elements_by_class_name("menu-container-set-menu-content")
            for data in smarthouse_data:
                message += f"{data.text}\n\n"
        elif restaurant == "garden":
            driver.get("https://www.foodandco.fi/ravintolat/Ravintolat-kaupungeittain/oulu/garden/")
            garden_data = driver.find_elements_by_class_name("menu-container-set-menu-content")
            for data in garden_data:
                message += f"{data.text}\n\n"
        elif restaurant == "galaxi":
            driver.get("https://www.sodexo.fi/ravintolat/ravintola-galaksi")
            garden_data = driver.find_elements_by_class_name("meal-name")
            for data in garden_data:
                message += f"{data.text}\n\n"
        
        return message


handler_class = HelloWorldHandler
