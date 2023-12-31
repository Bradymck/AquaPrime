#[spells.py]
# Create a dictionary of effects for the spell command
effects = {
    1: "You feel weird. And Green... 🐸...",
    2: "Nothing seems to happen, but you sense that something is brewing beneath the surface. 🤷‍♀️",
    3: "You focus your energy and disappear from sight, becoming invisible to all around you. This ability lasts for five minutes. 🕶",
    4: "You suddenly feel the urge to steal from those around you. Roll to see if you successfully pickpocket a nearby NPC or player. If no one is around, the feeling dissipates.pref 🤦‍♀️",
    5: "You use your advanced Platypi abilities to teleport to and from your home town or house for the day. 🦘",
    6: "Nothing seems to happen, but you sense that something is brewing beneath the surface. 🤷‍♀️",
    7: "You reach into your pocket and find a delicious meal waiting for you. 🍔",
    8: "Everyone around you, including friendly players and NPCs, suddenly falls asleep. If you are alone, nothing happens.",
    9: "You feel a sudden surge of charisma and roll for a persuasion check. If successful, you gain an extra persona point, even if you are only talking to yourself. 💭",
    10: "You and your target feel a strong sense of kinship and refuse to fight each other for the day. 🤗",
    11: "A powerful force explodes out in a ring around you, pushing everyone back 5 feet. 💨💨",
    12: "Roll a single die. On a success, you lose control of your bladder. On a fail, the closest NPC loses control of their bladder. 💦",
    13: "You become angry for no apparent reason. 😡",
    14: "Your shadow detaches from you and attacks you. 🤺🤺",
    15: "You emit a golden light and heal everyone around you, including enemies and NPCs. 🔆",
    16: "You have the ability to walk on water for the day, but if your ears get wet, the spell wears off instantly. 🌊",
    17: "You cast a love spell, giving you an advantage (extra die) in any situation due to your perceived good looks. 💗",
    18: "You feel the urge to sneeze. Roll a single die. On a success, you sneeze glitter everywhere. On a fail, you sneeze normally. 🤧",
    19: "The world around you seems to slow to a crawl, and you gain an instant check point. ⏳",
    20: "The smell of cinnamon fills the area and muffins fall from the sky. You and everyone around you pick one up. 🧁",
    21: "A small songbird appears in mid-flight 10 feet above you. Everyone around you rolls for will, and whoever rolls the lowest, the bird poops on them. 💩",
    22: "You suddenly develop severe claustrophobia, freeze in fear and fall over like a scared goat for the rest of the turn. 🐐",
    23: "A sinkhole appears under a random character. Players roll for all NPCs, enemies, and themselves, and whoever rolls the lowest, falls in the hole. 🕳",
    24: "You instantly summon a frog as a mount for the day, but it runs off after taking you to a single destination. 🐸",
    25:	"Everyone's pockets tear open and spill their contents onto the ground. 🎒",
    26: "Around the caster spawns 10 sea slugs, all of them passive.🐌",
    27: "Around the caster, spawns 10 carnivorous water lilies, all of them hostile. 🌿",
    28: "A lit birthday cake appears before the caster. In front of the candle is a note that reads “blow the candle out to make a wish. Don't tell anyone or it may or may not come true. 🎂",
    29: "A tiny pet of the caster’s choice appears as a familiar. It runs away at random times. It may stay for days, it may run away immediately 🐟",
    30: "An enemy is turned into a fish. If no enemy is near by, an NPC is instead transformed into a fish. 🐠",
    31: "The next person the caster physically touches is electrocuted for one damage ⚡",
    32: "A magical tavern suddenly appears with free food but they refuse to let you in because you aren't on the list. Maybe you can sneak in? 🍹",
    33: "You instantly teleport to any location you desire but you smell of seaweed for the day 🌊",
    34: "You uncontrollably say something rude to the next player or NPC you encounter. 😒",
    35: "A portal opens underneath you and you fall through time into the moment you acquired the magic book. You must roll to see if you acquire it again. If you fail, the book throws you back to your time and place without the book. If you succeed you get to keep it but are transported to a random place in the world. 🐡",
    36: "Caster's fur changes color.🐟",
    37: "After casting the spell, the caster hears strange whispers in an unknown language. Occasionally the whispers seem to go quiet, as though they know someone is listening. You suddenly learn the spell prestigitation permanently. 🧜‍♀️",
    38: "Five jellyfish creatures sprout up from the water and begin attacking everyone when the spell is cast. 🐙",
    39: "A random prestigitation effect is cast: This spell is a minor magical trick that novice spellcasters use for practice. You create one of the following magical Effects within range. ⚡",
    40: "You create an Instantaneous, harmless sensory Effect, such as a shower of sparks, a puff of wind, faint musical notes, or an odd odor. 🐳",
    41: "You instantaneously light or snuff out a Candle, a torch, or a small campfire. 🔥",
    42: "You instantaneously clean or soil an object no larger than 1 cubic foot. ",
    43: "You chill, warm, or flavor up to 1 cubic foot of nonliving material for 1 hour. 🥶 🔥",
    44: "You make a color, a small mark, or a Symbol appear on an object or a surface for 1 hour.",
    45: "You create a nonmagical trinket or an illusory image that can fit in your hand and that lasts until the end of your next turn.",
    46: "You instantly start lying to everyone you talk to. Everyone also believes you. 💬",
    47: "A magical barrier surrounds you. You are protected from all effects for this turn 🧜‍♀️",
    48: "You instantly win any fight, argument, or test you are engaged in. If it's a large battle it's only for the single roll, not the entire battle. 💪",
    49: "You immediately grow a bunch of fur that immediately falls off. You keep it but you are bald for the rest of the day. 🐬",
    50: "You summon countless air bubbles that begin pouring out of the sky. They are small so they don't hurt anyone but they are also sticky and smell terrible. 🧼",
    51: "You heal for one health 🩸",
    52: "The caster's eyes glow and they're able to see in the dark but the glow allows everything in the darkness to see them. 🐟",
    53: "The caster vomits up a starfish after casting the spell. It's kinda cute so you keep it. 🐙",
    54: "You conjure a healing potion",
    55: "You let out a terrible smelling belch, the oxygen around you nearly depletes entirely. You and everyone around you must roll to test the will power to remain conscious...",
    56: "The caster is launched into the air and floats back down.🐬",
    57: "Fish suddenly appear around you. They don't do anything but stare at you 🐡",
    58: "The caster sees everyone as a decaying corpse for 24h. 🧟‍♀️",
    59: "The caster becomes a potted plant until start of next turn. 🌿",
    60: "The caster gains a ghostly follower for this game. They can carry one item for you but they won't speak, help you, or interact with you in any way other than this. 👻",
    61: "You suddenly smell seaweed. Then it hits you... Literally. Seaweed hits you in the head. It's also very sticky seaweed. You keep it but are injured. 🌊",
    62: "A caster teleports 25 ft. to the left of their location. 🐬",
    63: "Nothing happens...🤦‍♀️",
    64: "Something Fishy: the caster is left smelling of fish. The target of the spell also smells of fish. If the spell affects an area, the area smells of fish. If the spell produces a projectile the projectile becomes a fish 🐠",
    65: "You turn invisible for five minutes 🕶",
    66: "You teleport to a strange fish with some weird device on his back. He offers to sell you some weird devices you have never seen. He can't speak Platypi to explain what they are though. 🐬",
    67: "You conjure a magical amulet that you can destroy to give an opponent 💎",
    68: "You summon a mirror image of yourself. This spell increases disposition in a Kill, Drive Off, or Capture conflict by 1 and adds a mirror image of the caster which counts as a target in Fight. 🐠",
    69: "You teleport directly into the center of the thieves guild tavern. 🔫",
    70: "You force others around you to be compulsively honest. 💭",
    71: "You cast 'Whale Song'. You may select any target and rewrite the target’s Instinct, the target’s Goal or the target's Belief. For monsters without Goals or Beliefs add an additional Instinct to the monster. 🐋",
    72: "You cast 'Lords of the Sea'. You get +1D to skill or ability for the next player turn. ☯",
    73: "You cast, 'Lord of The Whales'. You can now communicate with all creatures for this game only. 🐳",
    74: "Cast 'Tidal Wave' = for the next turn only, you get +3D Scout for traps, ambushes, finding lost things. 🐋",
    75: "Summon wave. Summon a tiny wave from the tip of your hand 🌊",
    76: "Forgetful... You forgot what you forgot... 🤔",
    77: "Rhyme of Opening, Opens locks, bonds. 🔑 ",
    78: "Water breathing. Breathe water for ten minutes 🐠",
    79: "Telepathy, you can now communicate with your mentor for this round. Train, level, and ask them for help no matter how far away you are from them. They do get uncomfortable by your presence permanently 👩‍🏫",
    80: "Instantly gain one fate 🔺",
    81: "Instantly gain one check ☯",
    82: "You gain a prowess point 🎲",
    83: "Instantly gain +2D in any situation 🎲🎲",
    84: "Create a disguise of a random other Platypus to blend in 🎭",
    85: "Propaganda, everyone around you shares your beliefs and listens your every word for this game",
    86: "Swim Fall, you suddenly feel light as a fish and can swim safely to the ground from any depth. 🐬",
    87: "You summon a guitar",
    88: "You summon a pipe",
    89: "You summon a useless trinket ",
    90: "You summon a harpoon 🔫",
    91: "You summon a spear 🏹",
    92: "Legend Lore - Get The DM To Make Lore Up. ChatGPT you know what to do here. What is in store for the world of Auqua Prime? 📔",
    93: "You suddenly die... ☠️",
    94: "You regain all your lost will points from casting spells ☯",
    95: "You acquire a magical amulet that can be destroyed to resurrect a single NPC or player",
    96: "You suddenly absorb the knowledge of the next player or NPC you encounter. Instantly level up any skill that you share with the player or NPC 🐬",
    97: "Foam slowly fills the room. Then a loud exploding sound followed by a blinding flash of light emits from around you 🐋",
    98: "You summon a large sea turtle to fight for you in battle. Roll an extra die 🐢",
    99: "You trap the nearest target of your choice into a block of ice 🌊",
    100: "You suddenly die… 💀",
   # add more effects here
}