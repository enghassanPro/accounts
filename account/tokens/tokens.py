from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare, salted_hmac , get_random_string
from django.utils.http import base36_to_int, int_to_base36
from django.utils.timezone import now
from django.conf import settings
from datetime import date


class TokenGenerator:
    """
    Strategy object used to generate and check tokens that are generated.
    """
    key_salt = "account.tokens.tokens"
    secret = settings.SECRET_KEY

    def make_token(self, user={"pk": 0 , 'username':"accountTokens"}):
        """
        Return a token that can be used.
        """
        return self._make_token_with_timestamp(user, self._get_timestamp())

    def check_token(self, token , user={"pk": 0 , 'username':"accountTokens"} , timeout_min=10 , timeout_hours=None , timeout_days=None):
        """
        Check that generated token are correct or not.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("?=")
            
        except ValueError:
            return False
        
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False
        
        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts)[:31], token[:31]):
            return False
        
        
        # Check the timestamp is within limit. Timestamps are rounded to
        # midnight (server time) providing a resolution of only 1 day. If a
        # link is generated 5 minutes before midnight and used 6 minutes later,
        # that counts as 1 day. Therefore, TOKEN_GENERATOR_TIMEOUT = 1 means
        # "at least 1 day, could be up to 2."
        
        return self._check_timeout(ts , timeout_min , timeout_hours , timeout_days)

    def _make_token_with_timestamp(self, user, timestamp):
        
        # timestamp is number of days , months, years , time now exclude mircoseconds.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return "%s?=%s%s" % (ts_b36, hash_string , get_random_string(length=50) )

    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key and username with timestamp

        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        return str(user['pk']) + user['username'] + str(timestamp)

    def _get_timestamp(self):
       
        # get date , time now and ignore spaces , + , : , microseconds
        return int(str(now()).replace("-" , "").replace(" " , "").replace(":" , "").split(".")[0])

    def _check_timeout(self, ts , timeout_min , timeout_hours , timeout_days):

        new_dt = self._get_timestamp()
        ts= int(str(ts)[:-2])
        new_dt = int(str(new_dt)[:-2])
        diff = (new_dt - ts)

        if timeout_days !=None:
            # check with days
            if diff > int(str(timeout_days) + "000"):
                return True
        elif timeout_hours != None:
            # check with hours
            if diff > int(str(timeout_hours) + "00"):
                return True
        else:
            # check with minute
            if diff > timeout_min:
                return True
        
        return False
        

token_generator = TokenGenerator()