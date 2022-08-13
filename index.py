# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
A bot that indexes your messages and save them to elastic
"""

#import logging
import json
import re
from functools import partial


import emoji
from elasticsearch import Elasticsearch
from telegram.ext import Updater, CommandHandler  # , MessageHandler, Filters

from config import config

TELEGRAM_API_TOKEN = config.TELEGRAM_API_TOKEN  # env.get("TELEGRAM_API_TOKEN")
ELASTICSEARCH_HOST = config.ELASTICSEARCH_HOST  # env.get("ELASTICSEARCH_HOST")
ELASTIC_USER = config.ELASTICSEARCH_HOST  # env.get("ELASTIC_USER")
ELASTIC_PASSWORD = config.ELASTIC_PASSWORD  # env.get("ELASTIC_PASSWORD")

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)


def message_data_to_es_object(message_test):
    """Verify message data structure and return an ES compatible JSON object"""
    trimmed_text = message_test.replace(
        "/update\n", "").replace("/update", "").replace("\n", ",\n")
    quoted_text = re.sub(r'(\w+)', r'"\1"', trimmed_text)
    braced = f"{{ {quoted_text} }}"
    json_text = json.loads(braced)
    return json_text


def update_index(update, context, elastic):
    """Send a message when the command /help is issued."""
    message = message_data_to_es_object(update.message.text)
    print(elastic.info())
    update.message.reply_text(f"got message {message}")
    elastic_response = elastic.index(index='test-index', document=message)
    print(elastic_response)
    update.message.reply_text(
        f"Great! successfuly indexed your update {emoji.emojize(':thumbs_up:')}")


# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    print(
        f"Connecting to elasticsearch... with creds user is {ELASTIC_USER} and pass is {ELASTIC_PASSWORD} and {ELASTICSEARCH_HOST}")
    elastic = Elasticsearch(
        hosts=ELASTICSEARCH_HOST,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
    )

    if not elastic.ping():
        raise ValueError(
            f"Connection to elasticsearch in {ELASTICSEARCH_HOST} had failed")

    print("Connected to elasticsearh")
    updater = Updater(
        TELEGRAM_API_TOKEN, use_context=True)
    print("started listenning...")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(
        "update", partial(update_index, elastic=elastic)))
#    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
