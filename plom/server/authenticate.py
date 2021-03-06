# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2020 Andrew Rechnitzer
# Copyright (C) 2020 Dryden Wiebe
# Copyright (C) 2020 Vala Vakilian

import uuid
from passlib.context import CryptContext


class Authority:
    """A class to do all our authentication - passwords and tokens."""

    def __init__(self, masterToken):
        """Set up cryptocontext, userlist and tokenlist"""
        self.ctx = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
        # set master token, being careful of what user supplies
        # is hex string of uuid4
        self.masterToken = self.build_master_token(masterToken)
        # convert it to int - is base 16
        self.mti = int(self.masterToken, 16)
        # we need this for xor-ing.

    def build_master_token(self, token):
        """Creates a new masterToken or validates existing masterToken.

        Arguments:
            token {masterToken} -- Current masterToken, if None, a new one is created.

        Returns:
            masterToken -- Valid masterToken.
        """
        if token is None:
            masterToken = uuid.uuid4().hex
            print("No masterToken given, creating one")
        else:
            try:
                masterToken = uuid.UUID(token).hex
                print("Supplied masterToken is valid. Using that.")
            except ValueError:
                masterToken = uuid.uuid4().hex
                print(
                    "Supplied masterToken is not a valid UUID. Creating new masterToken."
                )
        return masterToken

    def get_master_token(self):
        """Getter for the masterToken"""
        return self.masterToken

    def check_password(self, password, passwordHash):
        """Check the password against the hashed one.

        Arguments:
            password {str} -- Password to check.
            passwordHash {hex} -- Hashed password.

        Returns:
            bool -- True if passwords are the same, False otherwise.
        """

        if passwordHash is None:  # if there is no hash, then always fail.
            return False
        return self.ctx.verify(password, passwordHash)

    def create_token(self):
        """Create a token for a validated user, return that token as hex and int-xor'd version for storage.

        Returns:
            list -- Client and storage tokens in the form [clientToken, storageToken].
        """
        clientToken = uuid.uuid4().hex
        storageToken = hex(int(clientToken, 16) ^ self.mti)
        return [clientToken, storageToken]

    def validate_token(self, clientToken, storageToken):
        """Validates a given token against the storageToken.

        Arguments:
            clientToken {hex} -- The token we have.
            storageToken {hex} -- The token we are checking against.

        Returns:
            bool -- True if validated, False otherwise
        """
        if hex(int(clientToken, 16) ^ self.mti) == storageToken:
            return True
        else:
            return False

    def check_string_is_UUID(self, tau):
        """Checks that a given string is a valid UUID.

        Arguments:
            tau {str} -- String to check.

        Returns:
            bool -- True if a valid UUID, False otherwise.
        """
        try:
            token = uuid.UUID(tau)
        except ValueError:
            return False
        return True

    def basic_user_password_check(self, username, password):
        """Sanity check for usernames and passwords.

        Arguments:
            username {str} -- Given username.
            password {str} -- Given password.

        Returns:
            bool -- True if valid, false otherwise.
        """
        # username must be length 4 and alphanumeric
        if not (len(username) >= 4 and username.isalnum()):
            return False
        # password must be length 4 and not contain username.
        if (len(password) < 4) or (username in password):
            return False
        return True

    def create_password_hash(self, password):
        """Creates a hash of a string password.

        Arguments:
            password {str} -- Password to hash.

        Returns:
            hex -- Hashed password.
        """
        return self.ctx.hash(password)
