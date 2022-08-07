import requests
import time


class piShock:
    """
    piShock methods: shock, vibe, beep

    Shock: piShock.shock(username, apikey, code, name, duration, intensity, <Optional>warning)
    Vibe: piShock.vibe(username, apikey, code, name, duration, intensity)
    Beep: piShock.beep(username, apikey, code, name, duration)
    """
    def __init__(self, username:str, apikey:str, code:str, name:str, duration:int=0, intensity:int=0, warning:int=0):
        if name.lower() == "pishock":
            """'name' must be different from piShock"""
        elif duration > 15 or duration < 1:
            """Duration must be between 1 and 15"""
        elif intensity > 100 or intensity < 1:
            """Intensity must be between 1 and 100"""
        self.username = username
        self.apikey = apikey
        self.code = code
        self.name = name
        self.duration = duration
        self.intensity = intensity
        self.warning = warning

    def shock(self):
        """
        Shock the device for a duration of time, with warning if desired.
        Requires Username, API Key, Share Code, a name for the API call, duration between 1-15, and intensity between 1-100.
        You can also include a warning, in a duration of seconds between the shock and the warning.

        Use: piShock.shock(username, apikey, code, name, duration, intensity, <<Optional>warning)
        """
        if self.warning > 0:
            do(self.username, self.apikey, self.code, self.name, 1, 1, self.intensity)
            time.sleep(self.warning)
        return do(self.username, self.apikey, self.code, self.name, 0, self.duration, self.intensity)

    def vibe(self):
        """
        Vibe the device for a duration of time.
        Requires Username, API Key, Share Code, a name for the API call, duration between 1-15, and intensity between 1-100.

        Use: piShock.vibe(username, apikey, code, name, duration, intensity)
        """
        return do(self.username, self.apikey, self.code, self.name, 1, self.duration, self.intensity)

    def beep(self):
        """
        Beep the device for a duration of time.
        Requires Username, API Key, Share Code, a name for the API call, duration between 1-15.
        
        Use: piShock.beep(username, apikey, code, name, duration)
        """
        return do(self.username, self.apikey, self.code, self.name, 2, self.duration)

        
#Submit api request.
def do(username, apikey, code, name, operation, duration, intensity=0):
    """
    Submit api request.
    """
    session = requests.Session()
    session.params = {}
    session.params['Username'] = username
    session.params['Name'] = name
    session.params['Code'] = code
    session.params['Intensity'] = intensity
    session.params['Duration'] = duration
    session.params['Apikey'] = apikey
    session.params['Op'] = operation
    response = session.post('https://do.pishock.com/api/apioperate', json=session.params)
    return [response.status_code, response.text]