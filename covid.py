import requests
from keys import *

api_key = covid_apiKey

def queryUrl(state):
    return f"http://api.covidactnow.org/v2/state/{state}.json?apiKey=" + api_key

class covidInfo:
    def __init__(self, state):
        # Infection Rate
        try:
            self.infRate = float(requests.get(queryUrl(state)).json()['metrics']['infectionRate'])
        except TypeError:
            self.infRate = "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
            self.infRate = "NaN"
        
        # Positive Rate
        try:
            self.posRate = round(100*float(requests.get(queryUrl(state)).json()['metrics']['testPositivityRatio']), 2)
        except TypeError:
            self.posRate = "NaN"
        except Exception as e:
            self.posRate = "NaN"
            print(f"An error occured in data collection: {e}")
        
        # Vax Rate
        try:
            self.vaxRate = round(100*float(requests.get(queryUrl(state)).json()['metrics']['vaccinationsCompletedRatio']), 2)
        except TypeError:
            self.vaxRate = "NaN"
        except Exception as e:
            self.vaxRate = "NaN"
            print(f"An error occured in data collection: {e}")
        
        # Free Bed Percentage
        try:
            self.freeBedPercentage = round(100*float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageTotal'])/\
                float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            self.freeBedPercentage = "NaN"
        except Exception as e:
            self.freeBedPercentage = "NaN"
            print(f"An error occured in data collection: {e}")
        
        # New Cases
        try:
            self.newCases = int(requests.get(queryUrl(state)).json()['actuals']['newCases'])
        except TypeError:
            self.newCases = "NaN"
        except Exception as e:
            self.newCases = "NaN"
            print(f"An error occured in data collection: {e}")

        # New Deaths
        try:
            self.newDeaths = int(requests.get(queryUrl(state)).json()['actuals']['newDeaths'])
        except TypeError:
            self.newDeaths = "NaN"
        except Exception as e:
            self.newDeaths = "NaN"
            print(f"An error occured in data collection: {e}")
        
        # Covid Bed Percentage
        try:
            self.covidBedPercentage = round(100*float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageCovid'])/\
                float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            self.covidBedPercentage = "NaN"
        except Exception as e:
            self.covidBedPercentage = "NaN"
            print(f"An error occured in data collection: {e}")