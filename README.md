# boxbot

This code should allow for a localized instance of the Boxbot Discord bot as seen on the FleetCom server during Shoulder of Orion event as well as on the OASIS server. To set it up, complete the following:

1) Download the code from this repository.  Due to file size, only one of the 30 brewer gifs is in this repo. The rest can be found here:
2) Open the boxbotMain.py file in your preferred IDE, I can confirm compatability with Visual Studio Code. Edit lines 38 and 41-47 for your discord and systems.
3) Create an account if you dont already have one with http://discord.com/developers and create a new bot. Be sure to give it permissions for all the priviledge gateway intents. This is where you will get the client secret.
4) Next, make an account to access the giphy API here: https://developers.giphy.com/     this is where you will get your giphy api key
5) finally, create a new Google Sheets API project here: https://console.cloud.google.com/    use the info to fill in the service_account.json file.
6) That should be all of the prep needed!


# Commands and Content

Below are all of the available commands and what they do:

**/market-leaderboard** This command returns the top two largest supply markets for every colonization commodity within the WASTE_RADIUS distance of ORIGIN_SYSTEM in a pagified embeded message. It updates this list every 4 hours by finding every market that buys or sells biowaste within that radius and then checks each for every colonization commodity. 

**/shop-local** This command searches either the markets found in the market leaderboard for a user supplied commodity or all markets within a user supplied radius of ORIGIN_SYSTEM. Has filters for pad size and orbital vs planetary and provides inara link for markets. 

**/ops**  This is a complete ecosystem for automatically maintaining and coordinating colonization chain/expidition opporations. First, fill out a copy of this google sheet template:     Next, get its document id from the url and a user with the AUTHORIZED_ROLE_ID role runs /register-op and provides the doc id as well as some basic info for the operation. Once this is done, the expidition will appear when /ops is called and users can sign up for the opperation and do things like mark FCs as empty or full (will DM the fc owners of the change), mark current systems as complete or that the beacon is deployed, etc. 

**howis-fc and whereis-fc** uses ardent-industries and spansh api to find the location and market conditions of any FC given its callsign and returns the info and when the info was last updated. 

**praise and chastise** lets users praise and or chastise the bot

**dropoff my-stats and leaderboard** lets users record cargo they have hauled. has a badge system based on tons delivered and replies with affirming motivational sayings. users can see badges and progress using my-stats and how they compare with leaderboard. Also tracks community points

**market-updated and thanks** market updated lets users record when they have flown to a market and updated eddb with its market state. has 5min grace period. thanks lets users thank other commanders. both awards community points. 

****


