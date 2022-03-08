import asyncio


#this is the function that will run all the time

# 1. Get all of the clubs from clubs table
# 2. Using the clubID find the name of the club on the presence api
# 3. Get the latest event of that club
# 4. Using event's data, create the event in ICheck-in
# 5. Generate a code and write that to the codes table with the name of the eventID and start and date of the event like this [code, eventID, startTime, endTime]
# 6. Do steps 2-4 until you have done it for all of the clubs in the clubs table.
# 7. Have an event listener function that watches for any changes in the clubs table, and if there's change, run steps 2-4.


#this is the another function that will run all the time, this function is for refreshing the latest event of the club in the codes table

# 1. Get all codes from codes table sorted through the most recent to latest.
# 2. 