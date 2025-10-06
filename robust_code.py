"""
User Account Management System

This module provides functionality for managing user accounts including
authentication, profile management, and data validation.

Example:
    user = UserAccount('john_doe', 'secret123', 'john@example.com', 25)
    if user.login('secret123'):
        print('Login successful')
"""

from datetime import datetime
import requests
from typing import Optional, Dict, Any


# Custom exceptions
class UserAccountError(Exception):
    """Base exception for user account operations."""
    pass


class InvalidEmailError(UserAccountError):
    """Raised when email format is invalid."""
    pass


class AuthenticationError(UserAccountError):
    """Raised when authentication fails."""
    pass


class NetworkError(UserAccountError):
    """Raised when network operations fail."""
    pass


class userAccount:
    """
    A user account management class.

    This class handles user authentication, profile information,
    and account lifecycle management.

    Attributes:
        username (str): The user's unique username
        email (str): The user's email address
        age (int): The user's age
        created_at (datetime): Account creation timestamp
        last_login (datetime): Last successful login timestamp
        is_active (bool): Account active status

    Example:
        >>> user = UserAccount('john', 'pass123', 'john@email.com', 25)
        >>> user.login('pass123')
        True
    """

    Username: str
    Password: str
    Email: str
    Age: int
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        age: int
    ) -> None:
        """
        Initialize a new user account.

        Args:
            username (str): The user's unique username
            password (str): The user's password
            email (str): The user's email address
            age (int): The user's age

        Raises:
            ValueError: If any of the parameters are invalid
            InvalidEmailError: If the email format is invalid

        Example:
            >>> user = userAccount('john', 'pass123', 'john@email.com', 25)
        """
        # Input validation
        if not isinstance(username, str) or len(username.strip()) == 0:
            raise ValueError("Username must be a non-empty string")
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not validate_email(email):
            raise InvalidEmailError(f"Invalid email format: {email}")
        if not isinstance(age, int) or age < 0 or age > 150:
            raise ValueError("Age must be an integer between 0 and 150")
        # Set attributes only after validation
        self.Username = username.strip()
        self.Password = password
        self.Email = email.strip().lower()
        self.Age = age
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True

    def login(self, password: str) -> bool:
        """
        Authenticate user with provided password.

        Args:
            password (str): The password to verify

        Returns:
            bool: True if authentication successful, False otherwise

        Example:
            >>> user.login('correct_password')
            True
            >>> user.login('wrong_password')
            False
        """

        if password == self.Password:
            self.last_login = datetime.now()
            return True
        else:
            return False

    def get_account_info(self) -> Dict[str, Any]:
        """
        Retrieve account information.

        Returns:
            dict: Dictionary containing username, email, age, and active
            status.

        Example:
            >>> user.get_account_info()
            {'username': 'john', 'email': 'john@email.com', 'age': 25,
            'active': True}
        """

        return {
            "username": self.Username,
            "email": self.Email,
            "age": self.Age,
            "active": self.is_active,
        }

    def update_password(self, old_password: str, new_password: str) -> bool:
        """
        Update the user's password if the old password is correct.

        Args:
            old_password (str): The current password
            new_password (str): The new password to set

        Returns:
            bool: True if password updated successfully, False otherwise

        Example:
            >>> user.update_password('oldpass', 'newpass')
            True
        """

        if self.login(old_password):
            self.Password = new_password
            return True
        return False


def validate_email(email: str) -> bool:
    """
    Validate email address format with comprehensive checks.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email appears valid

    Raises:
        TypeError: If email is not a string
        InvalidEmailError: If email format is invalid
    """
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    email = email.strip().lower()
    if not email:
        raise InvalidEmailError("Email cannot be empty")
    if email.count('@') != 1:
        raise InvalidEmailError("Email must contain exactly one '@' symbol")
    username, domain = email.split('@')
    if not username or not domain:
        raise InvalidEmailError("Email must have both username and"
                                " domain parts")
    if '.' not in domain:
        raise InvalidEmailError("Domain must contain at least one dot")
    return True


def calculate_account_age(created_date: datetime) -> int:
    """
    Calculate the age of an account in days.

    Args:
        created_date (datetime): The account creation date

    Returns:
        int: Number of days since account creation

    Example:
        >>> calculate_account_age(datetime(2023, 1, 1))
        365
    """

    now = datetime.now()
    diff = now - created_date
    return diff.days


def fetch_user_data(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch user data from external API with error handling.

    Args:
        user_id (int): User ID to fetch data for

    Returns:
        Optional[Dict[str, Any]]: User data if successful, None otherwise

    Raises:
        NetworkError: If network request fails
        ValueError: If user_id is invalid
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer")
    url = f"https://api.example.com/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise NetworkError(f"Timeout while fetching user {user_id}")
    except requests.exceptions.ConnectionError:
        raise NetworkError(f"Connection error while fetching user {user_id}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise NetworkError(f"HTTP error {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request failed: {e}")
    except ValueError as e:
        raise NetworkError(f"Invalid JSON response: {e}")


if __name__ == "__main__":
    user = userAccount("john_doe", "secret123", "john@example.com", 25)
    print("User created:", user.get_account_info())
    if user.login("secret123"):
        print("Login successful")
    else:
        print("Login failed")
