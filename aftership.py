# -*- coding: utf8 -*-
"""
aftership.py - Willie aftership tracking module
"""
import requests
import json

API_URL = "https://api.aftership.com/v4"
HEADERS = {"Content-Type": "application/json", "aftership-api-key": bot.config.apikeys.aftership_api_key}

def track(bot, trigger):
    tracking_number = trigger.group(2)
    nick = trigger.nick.lower()
    
    message = ".track TRACKING_NUMBER"
    if tracking_number:
        message = create_tracking(tracking_number, nick)
    else:
        if bot.db.get_nick_value(nick, 'last_tracking_id'):
            message = get_tracking(bot.db.get_nick_value(nick, 'last_tracking_id'))            
    bot.say(message)


def create_tracking(tracking_number, nick):
    post_data = {
        "tracking": {
            "tracking_number": tracking_number
        }
    }
    r = requests.post(u"{}/{}/".format(API_URL, 'trackings'), data=json.dumps(post_data), headers=HEADERS).json()
    if "id "in r["data"]["tracking"]:
        tracking_id = r["data"]["tracking"]["id"]
        if bot.db:
            bot.db.set_nick_value(nick, 'last_tracking_id', tracking_id)
        return get_tracking(tracking_id)

    else:
        return "Your tracking number sucks. Go blame bob."


def get_tracking(tracking_id):
    r = requests.get(u"{}/{}/{}".format(API_URL, 'trackings', tracking_id), headers=HEADERS).json()
    tracking_data = r["data"]["tracking"]
    message = u"Expected: {}, Latest Status: {}: {}".format(tracking_data["expected_delivery"], tracking_data["checkpoints"][-1]["message"], tracking_data["checkpoints"][-1]["checkpoint_time"] )
    return message