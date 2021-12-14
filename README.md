# meepybot
Discord bot that reimplements Discord's built-in features in an alternative way!

How to use:
1. Run python utilities/dbgen.py to generate a database with table and indexes
2. Keep main.py running

# Features
* Custom pin system to bypass the 50-pin limit in Discord
  - `?meep pin [message ID]` pins the specified (or referenced/replied) message
  - `?meep unpin [message ID]` unpins the specified (or referenced/replied) message
  - `?meep random` retrieves a random pinned message from the channel
  - `?meep showpins` generates a URL that displays all of your pins (use in conjunction with [meepybot-webserver](https://github.com/lilbillybiscuit/meepybot-webserver))
  - `?meep refresh` refreses the cache of all of the messages in a channel (might change to last 14 days only)
  - Messages are refreshed once every hour anyway
* Democracy moderation system
  - `?meep mute [ping someone]` starts a vote that lasts for `vote_timeout` seconds and requires `vote_threshold` reactions to pass
  - `?meep unmute [ping someone]` is the same thing but unmuted
  - `?meep slowmode [ping someone]` is the same thing but adds a 'slowmoded' role to the user
  - The bot has a slowmode feature that will automatically delete a user's message if they have the 'slowmoded' role and they haven't waited `slowmodetime` seconds before sending another message
* Settings
  - `?meep options` gives a list of all the settings you can figure (including parameters for voting)
  - `?meep set [option name] [value]` sets `option name` to the specificed `value`
* Misc
  - `?meep oeis` picks a random number sequence from OEIS and prints it
  - `?meep zipavatars` creates a zip file of all of the profile pictures in the server for use in tier lists
  - `?meep version` displays the version
  - `?meep fmute` or `?meep forcemute` can only be used by mods and you can mute multiple users at a time
  - `?meep funmute` or `?meep forceunmute` is the same thing but for unmuting
