# Global Entry Notifier

This is an azure function written in Python to check for available global entry interview appointments at a specific location and send an sms message via twilio when they become available.

## Setup
Ensure that all environment variables for twilio use are setup in the azure function configuration settings and ensure that the location code variable is set for your desired location from here: https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry

Inspiration came from this project: https://github.com/Drewster727/goes-notify
