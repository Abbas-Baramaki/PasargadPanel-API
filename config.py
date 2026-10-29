import requests
import datetime
import random
import uuid

class AuthenticationError(Exception):
    """The point in time when the token or authentication information is invalid."""
    pass
class LoginError(Exception):
    """No login has taken place yet, or the access token is empty."""
class TokenUnfilledError(Exception):
    """The token has not been filled in correctly."""
    pass
class UserAlreadyExists(Exception):
    """User already exists in panel"""
    pass

class Config:
    def __init__(self,panel,username,password):
        self.panel = panel
        self.username = username
        self.password = password
        self.logged = False
        self.access_token = None
        self.token_type = None
        print("Config panel estabished")
    
    def handle_exception(self,status_code : int):
        match status_code:
            case 201:
                raise UserAlreadyExists
            case 401:
                raise AuthenticationError
            case 404: 
                raise requests.exceptions.HTTPError 

    def login(self)->bool:
        """Function for logging into the panel, submitting user credentials, and receiving an access token.
        Args:

        Returns:
            bool: True if the login is successful and the access token is correctly received; otherwise, False.

        Raises:
            AuthenticationError: Raised when the provided credentials or token are invalid.
            requests.exceptions.HTTPError: Raised if an HTTP error occurs.
            requests.exceptions.RequestException: Raised if a network or connection failure occurs.
        """
        payload = {
            "grant_type":"password",
            "username":self.username,
            "password":self.password
        }
        _login_res = requests.post(f"{self.panel}/api/admin/token",data=payload)
        _login_data = _login_res.json()

        if _login_res.status_code == 200:
            self.access_token = _login_data["access_token"]
            self.token_type = _login_data["token_type"]
            if self.access_token and self.token_type :
                self.logged == True
                return True
            else :
                raise TokenUnfilledError
        else :
            self.handle_exception(_login_res.status_code)
            return False
    
    def create_sub(self,data_limit:float,expire:int,name:str,note="",group=[2])->dict:
        """Creates a new user account in the panel.
        Args:
            data_limit (float): Data usage limit allowed for the user in gigabytes.
            expire (int): Expiration duration in days for the user account.
            name (str): Unique username for the subscription.
            note (str, optional): Additional note or description for the user. Defaults to "".
            group (list, optional): List of group IDs assigned to the user. Defaults to [2].

        Returns:
            dict: The JSON response from the server containing the created user details or status.

        Raises:
            requests.exceptions.HTTPError: If the server returns an HTTP error response (e.g., 404 Page/Endpoint Not Found).
            requests.exceptions.RequestException: If a network or request connection fails.
        """
        
        header = {
            "accept":"application/json",
            "authorization":f"""{self.token_type} {self.access_token}"""
        }
        subname = random.choice(str(uuid.uuid4()).split("-"))
        payload = {
            "data_limit":data_limit,
            "expire" : (datetime.datetime.now() + datetime.timedelta(expire)).strftime("%Y-%m-%d"),
            "group_ids" : group,
            "hwid_limit" : None,
            "next_plan" : None,
            "note" : note,
            "proxy_settings" : {"shadowsocks": {"method": "chacha20-ietf-poly1305"}},
            "status" : "active",
            "username" : name + subname
        }
        if self.access_token and self.token_type:
            _create_res = requests.post(f"{self.panel}/api/user",headers=header,json=payload)
            _create_data = _create_res.json()
            # self.handle_exception(_create_res.status_code)
            return _create_data
        else : 
            raise LoginError
        
    def subscription(self,username)->dict:
    
        """Retrieves subscription details and status for a specific user from the panel.

        Args:
            username (str): The unique username whose subscription information is being requested.

        Returns:
            dict: A dictionary containing the user's subscription details, including status, expiration date, data limit, and other parameters.

        Raises:
            AuthenticationError: Raised when the provided credentials or token are invalid.
            requests.exceptions.HTTPError: Raised if an HTTP error occurs.
            requests.exceptions.HTTPError: If the server returns an HTTP error response (e.g., 404 User Not Found).
            requests.exceptions.RequestException: If a network or request connection fails.
        """
         
        header = {
                    "accept":"application/json",
                    "authorization":f"""{self.token_type} {self.access_token}"""
                }

        payload = {
            "limit":999999,
            "sort" : "-created_at",
            "load_sub" : True,
            "offset" : 0,
            "is_protocol" : False,
            "is_id" : False
        }
    
        _sub_res = requests.get(f"{self.panel}/api/users",data=payload,headers=header)
        _sub_data = _sub_res.json()
        
        if _sub_res.status_code == 200:
            for user in _sub_data["users"]:
                if user["username"] == username:
                    return user
        else : 
            self.handle_exception(_sub_res.status_code)
        return None # if statu s code doesnt find