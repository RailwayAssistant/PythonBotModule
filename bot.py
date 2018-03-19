# -*- coding: utf-8 -*-
from chatterbot import ChatBot


# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot

is_set_to_read_only = True

bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
#    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
#    input_adapter="chatterbot.input.TerminalAdapter",
#    output_adapter="chatterbot.output.TerminalAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.BestMatch",
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand this yet. Please let me train some more'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me!',
            'output_text': 'Ask the creater! The one true GOD!'
        }
    ],
    database="./db.sqlite3",
    preprocessors=[
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    read_only = is_set_to_read_only,
)

#bot.train('chatterbot.corpus.english')

if __name__ == '__main__':
    # The following loop will execute each time the user enters input
    print("Type something to begin...")
    while True:
        try:
            # We pass None to this method because the parameter
            # is not used by the TerminalAdapter
#            bot_input = bot.get_response()
            print(bot.get_response(input()))
        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

