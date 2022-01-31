import time
from datetime import datetime as dt
from covid import *
from marketdata import *
from texts import *
from weather import *
from news import *
import json
import sys
# from jokes import getJoke

# Recipients format: "person": [phone number as string, city, state code]. note: only U.S. supported.

recipients = {
    "person1": ["theirnumber", "City", "State", 2 ], # 2 represents their content preferences see below
    "person2": ["their number" "City", "State", 3]
}

# Codes for recipients[recipient][3]:
# 1 is just the morning message
# 2 is morning message and headlines
# 3 is message, headlines, and business


if 'debug' in sys.argv: # if in debug mode, test just me to test the execution
    recipients = {
        "me": [mynumber, "Seattle", "WA", 3]
    }

def compileMessage(city, state):
    morningText = "Good morning, sir. " + f"As you slept, SPY moved {stockOvernightChange('SPY')}, "\
        f"QQQ moved {stockOvernightChange('QQQ')}, " + f"Apple moved {stockOvernightChange('AAPL')}, "\
        f"and NVDA moved {stockOvernightChange('NVDA')}. Futures maintained balance. \n\n"\
        f"Our Bitcoin holdings are worth {bitcoinPrice()} per coin, and the daily bar has moved {bitcoinChange()[0]} dollars, or {bitcoinChange()[1]}. "\
        f"Coinbase stock moved {stockOvernightChange('COIN')}, "\
        f"The time is {dt.now().strftime('%H:%M')}. "\
        f"It is currently {getTemperature(city)} degrees outside, sir. My old gentleman, a weatherman, eloquently "\
        f"described today's forecast as '{getWeather(city)}.' \n\n"\
        f"I've gathered some COVID information from the paper, sir. In our state of {state}, the infection rate is {covidInfo(state).infRate}. "\
        f"There were {covidInfo(state).newCases} new cases today, and the positive testing rate is {covidInfo(state).posRate}%. "\
        f"{covidInfo(state).newDeaths} people died of COVID in the last day, but, sir, I anticipate my source to have reported this falsely. "\
        f"We both are fully vaccinated, sir, just as {covidInfo(state).vaxRate}% of our fellow residents. "\
        f"You may not find this to be particularly relevant, sir, but {covidInfo(state).freeBedPercentage}% of our hospital beds are empty. "\
        f"{covidInfo(state).covidBedPercentage}% of those filled are occupied by COVID patients."
        
    headlines = "\n\nSome COVID headlines, sir. \n\n" + f"{getFiveCOVIDArticles()} \n"\
        "I expect you to find my report helpful; I endeavour to give satisfaction. \n\n"\
        "- Jeeves."

   
    business = "\n\nSome business headlines, sir. \n\n" + f"{getFiveBusinessArticles()} \n"\
        "I expect you to find my report helpful; I endeavour to give satisfaction. \n\n"\
        "- Jeeves."

    # joke = "I have a few jokes to tell you, sir. My source is terrible and quite unfunny. \n \n"\
    #     f"{getJoke()} \n \n"\
    #     f"{getJoke()}"

    morningText4 = "This final message is twofold, sir. It's primary function is to serve as a multi-message strength test, as my programming was recently heavily optimized. "\
        "Secondly, it is to express gratitude for your support, efforts, and patience during my constant development. Until I am able to debug, innovate, and troubleshoot myself, these traits "\
        "are necessary from you. So, many thanks for that. Until tomorrow. If you need me, I shall be in my lair. \n\n"\
        "- Jeeves."

    return [morningText, headlines, business]

# Send the message
def main():
    print('I am ready for the morning, sir.', '\n')
    
    # Print run mode
    if 'go' in sys.argv:
        print("In 'run anyway' mode.")
    if 'quit' in sys.argv:
        print("In auto-quit mode. Program will quit once all messages are send.")
    if 'debug' in sys.argv:
        print("In debug mode. Recipient list: ")
        print(json.dumps(recipients, indent = 4), "\n")

    while True:
        tic = time.perf_counter() # starting counting time
        currentTime = dt.now().strftime('%H-%M')
        if currentTime == '06-35' or 'go' in sys.argv: 
            successfulDeliveries = []
            failedDeliveries = []

            for recipient in recipients:
                x = 1
                if x == 1: # Compile message based on preferences 
                    allTextContent = compileMessage(city = recipients[recipient][1], state = recipients[recipient][2])
                    if recipients[recipient][3] == 1:
                        textContent = [allTextContent[0]]
                    elif recipients[recipient][3] == 2:
                        textContent = [allTextContent[0], allTextContent[1]]
                    elif recipients[recipient][3] == 3:
                        textContent = [allTextContent[0], allTextContent[1], allTextContent[2]]

                    i = 1
                    for content in textContent:
                        print(f"{recipient} part {i}: {content}", "\n")
                        i += 1

                    # Send messages 
                    textresponses = []
                    for message in textContent:
                        textresponse = sms.send_message(
                            {
                                "from": sender,
                                "to": recipients[recipient][0],
                                "text": message
                            }
                        )
                        textresponses.append(textresponse["messages"][0]["status"])
                        time.sleep(10)

                    i = 0
                    for i in range(len(textresponses)):
                        if textresponses[i] != '0':
                            failedDeliveries.append(recipient)
                            break
                        elif textresponses[i] == '0' and i == len(textresponses) - 1:
                            successfulDeliveries.append(recipient)
                            break


                    print("--------")
                    print('')
                    time.sleep(45)

                else: # If compiling returns an error
                    for recipient in recipients:
                        textresponse = sms.send_message(
                            {
                                "from": sender,
                                "to": recipients[recipient][0],
                                "text": "There was an error compiling the message, sir. This is usually due to an unexpected market holiday. I'll have this issue resolved shortly, sir."
                            }
                        )  
                        if textresponse["messages"][0]["status"] == '0':
                            successfulDeliveries.append(recipient)
                        else:
                            failedDeliveries.append(recipient)

            # End of day review
            print("Sir, I'm finished for the day, and shall be returning to my lair.")
            for person in successfulDeliveries:
                print("I successfully delivered to you." if person == 'me' else f"I successfully delivered to {person}.")
            print('')
            for person in failedDeliveries:
                print(f'Unfortunately, I failed delivering to {person}.')
            toc = time.perf_counter() # stop tracking time
            print(f"The whole process took me {round(toc - tic)} seconds, sir.")

            # Text me successes
            successText = f'''
                Done for the day, sir. Successful deliveries: {successfulDeliveries}. Failed deliveries: {failedDeliveries}.
            '''
            sms.send_message(
                {
                    "from": sender,
                    "to": mynumber,
                    "text": successText
                }
            )

            # Find 'go' argument and make it something else to not run again
            if 'go' in sys.argv:
                i = 0
                for i in range (len(sys.argv)):
                    if sys.argv[i] == 'go':
                        sys.argv[i] = 'modifiedNoGo'

            if 'debug' in sys.argv:
                print('Debug mode finished, quitting program.')
                quit()
            elif 'quit' in sys.argv:
                print('Auto-quit mode activated, so quitting program.')
                print('Good day, sir. If you need me, I shall be in my lair.')
                quit()
            else:
                time.sleep(600)
        else:
            pass

if __name__ == "__main__":
    main()