from random import choice

messages = [
    f"🏹  Prepare to be amazed by **{{player_name}}**'s sword skills... or not!",
    f"🏹  **{{player_name}}** has entered the game and immediately forgot how to craft.",
    f"🏹  **{{player_name}}** just joined the server. The Berserker will probably be dead in 5 minutes.",
    f"🏹  **{{player_name}}** has entered the world of Valheim. We’re doomed.",
    f"🏹  Looks like **{{player_name}}** finally found the server... after 30 minutes of trying.",
    f"🏹  **{{player_name}}** has arrived! Time to test if the Viking can survive without a map.",
    f"🏹  **{{player_name}}** just logged in, let's hope the Berserker doesn't confuse the workbench for an altar.",
    f"🏹  **{{player_name}}** has entered Valheim, bringing chaos and confusion as usual.",
    f"🏹  **{{player_name}}** just joined and is already asking how to tame a boar... classic.",
    f"🏹  **{{player_name}}** has entered the game. Someone remind the Berserker that berries are not weapons.",
    f"🏹  The legendary **{{player_name}}** has joined. Now who’s going to mess up the firepit?",
    f"🏹  **{{player_name}}** has entered Valheim. Let’s hope the Viking doesn’t confuse the workbench for an altar.",
    f"🏹  **{{player_name}}** has logged in. Time to see if the Berserker can survive more than 10 minutes.",
    f"🏹  **{{player_name}}** is here, and we all know what that means… time for a new grave.",
    f"🏹  Welcome, **{{player_name}}**. We hope the Viking remembers how to run away from enemies.",
    f"🏹  **{{player_name}}** has joined. Someone grab the pitchforks, we're going hunting!",
    f"🏹  **{{player_name}}** is in! Hope the Berserker brought some wood this time... or at least some food.",
    f"🏹  **{{player_name}}** just entered the server, and chaos is about to ensue.",
    f"🏹  **{{player_name}}** has arrived! The Viking has been practicing running skills... away from enemies.",
    f"🏹  **{{player_name}}** just entered. The server was quiet until the Berserker arrived.",
    f"🏹  Look out! **{{player_name}}** has joined, and the Berserker’s already trying to build a roof… inside out.",
    f"🏹  **{{player_name}}** is here! Time for an unintentional friendly fire incident.",
    f"🏹  **{{player_name}}** has joined the game. Are we sure the Viking can build a shelter?",
    f"🏹  **{{player_name}}** has entered the world of Valheim... and forgotten how to use a hammer.",
    f"🏹  **{{player_name}}** has joined the server. Here’s hoping the Berserker doesn’t accidentally destroy the portal.",
    f"🏹  **{{player_name}}** is in the game. We’re all one accidental bonfire away from chaos.",
    f"🏹  **{{player_name}}** has joined. Will the Viking stay alive long enough to make a shield?",
    f"🏹  **{{player_name}}** just logged in... and immediately asked where to find the chickens.",
    f"🏹  **{{player_name}}** is back, and the Berserker’s probably going to break something again.",
    f"🏹  **{{player_name}}** has entered the server... let’s hope the Viking remembers which direction to run in.",
    f"🏹  **{{player_name}}** is here, and the Berserker's ready to make questionable decisions.",
    f"🏹  Welcome **{{player_name}}**! The good news: The Viking is here. The bad news: The Berserker is unprepared.",
    f"🏹  **{{player_name}}** has joined! Get ready for the next unintentional boat disaster.",
    f"🏹  **{{player_name}}** has arrived! Can the Berserker survive without getting lost for an hour?",
    f"🏹  **{{player_name}}** has entered the world of Valheim. Let’s see how long the Viking lasts.",
    f"🏹  **{{player_name}}** just joined. Time to see if the Berserker remembers where they put their axe.",
    f"🏹  **{{player_name}}** has logged in, and yes, the Viking's still the one who forgets the food.",
    f"🏹  **{{player_name}}** has arrived! Let the unorganized chaos begin!",
    f"🏹  Guess who’s back? **{{player_name}}**, the Berserker who can’t craft anything without help.",
    f"🏹  **{{player_name}}** just joined, and the Viking’s already asking where the nearest swamp is.",
    f"🏹  **{{player_name}}** has entered Valheim. Time to see how many times the Berserker will accidentally hit the wrong thing.",
    f"🏹  **{{player_name}}** is in! Someone give the Viking a map… they’re going to need it.",
    f"🏹  **{{player_name}}** just logged in. Time to find out if the Berserker remembers what the workbench is.",
    f"🏹  **{{player_name}}** has joined the game, probably with no idea how to survive the first night.",
    f"🏹  Look who’s here! **{{player_name}}** has entered Valheim… we’re all doomed now.",
    f"🏹  **{{player_name}}** is here! Everyone, hide your resources.",
    f"🏹  **{{player_name}}** has entered the game! Watch as the Berserker panics when the first boar shows up.",
    f"🏹  **{{player_name}}** has logged in. Now we just need them to stop dying every 5 minutes.",
    f"🏹  Welcome, **{{player_name}}**! Time to see how long the Viking can survive before calling for help."
]


def random_join_message(player_name: str) -> str:
    message = choice(messages)
    return message.format(player_name=player_name)
