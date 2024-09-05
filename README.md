# Discord Bots

Learning to create professional discord bots using python from FreeCodeCamp
This repository will store the code that I will write for practice!

# About Bots: 
=> **main.py** file contains a simple bot. This bot contains some simple commands to engage with users and motivate them. It also shares motivational quotes from https://api.api-ninjas.com/v1/quotes?category=inspirational

=> **polling-bot.py** file contains the code for a bot that can help users in conducting polls in the discord server.


# Execution Details:
1. Install the required dependencies using `pip install -r requirements.txt`
2. Than you can simply use python to start the bot `python main.py` for the 1st one and `python polling-bot.py` for the 2nd one

-------------------------------

# Polling Bot User Guide

The Polling Bot allows you to create polls in your Discord server, collect votes, and see the results automatically after a set time period.

## Commands

### 1. `/poll <question> <duration in hours> <choice1> <choice2> ... <choiceN>`
Create a poll with up to 10 choices. The bot will track votes and announce the result after the poll ends.

**Command Structure:**
/poll <question> <duration_in_hours> <choice1> <choice2> ... <choiceN>

**Example:**
/poll "What's your favorite color?" 2 "Red" "Blue" "Green"

This creates a poll with the question "What's your favorite color?" that lasts for 2 hours, and offers the choices: "Red," "Blue," and "Green."

## Poll Creation
After you run the command, the bot will:
- Delete the original command message to keep the chat clean.
- Post the poll with numbered emoji reactions (1️⃣, 2️⃣, etc.) for each choice.
- Send a DM to the poll creator to confirm the poll was created successfully.

## Poll Duration
- The poll will remain open for the specified number of hours (e.g., 2 hours in the example above).
- You can create polls lasting from a few minutes to several hours.

## Poll Limitations
- You need to provide at least **2 choices** and no more than **10 choices** for the poll.
- If you try to provide fewer than 2 choices or more than 10 choices, the bot will notify you.

## Voting
- Users can vote by reacting to the poll message with the corresponding numbered emoji (e.g., 1️⃣ for the first choice, 2️⃣ for the second, etc.).
- Each user can vote once per poll.

## Poll Results
When the poll time ends, the bot will automatically:
- Calculate the votes for each option.
- Announce the winning choice in the same channel where the poll was created.
- Send the poll creator a DM with the results, including the votes for each option.

**Tie Result:** If there is a tie between two or more options, the bot will declare a tie in the poll results.

**No Winner:** If all options have the same number of votes, the bot will announce that the poll ended in a tie between all options.

## DM Settings
Make sure your **Direct Messages (DMs)** are enabled if you want to receive notifications from the bot regarding poll creation and results.

# Images:

![image](https://github.com/user-attachments/assets/e4449b4c-17d8-4487-a7c9-ffd51aafec53)
![image](https://github.com/user-attachments/assets/07747a01-ed41-4e6a-998e-423be5b74cf4)


