# [News Ceeper Bot](https://t.me/NewsCkeeperBot)

This is a Python script for a Telegram bot. The bot forwards all incoming messages from users to a designated chat ID. The bot also has admin commands to ban users, unban users, and clear all messages from a specific user.

Here is a description of the script's main functions:

```/start```: This function responds to the /start command and sends a welcome message to the user.

```/ban_user```: This function bans the user who is the sender of the message that was answered with the command /ban_user (only with admin rights).

```/unban_user```: This function unbans the user who is the sender of the message that was answered with the command /unban_user (only with admin rights).

```/admin_commands```: This function sends a list of available admin commands to the admin user (only with admin rights).
