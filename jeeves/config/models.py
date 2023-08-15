"""Models for configuration."""
from pydantic import BaseModel, validator

import pytz


class GeneralConfig(BaseModel):
    """
    General configuration, affects the application as a whole.

    Attributes:
        sandbox_mode (bool): Prevents certain actions, ex. sending SMS.
        threaded_inbound (bool): Whether to process inbound SMS in a thread.
        dev_phone (str): Phone number used when running apps in command line.
    """
    sandbox_mode: bool
    threaded_inbound: bool
    dev_phone: str
    default_timezone: str

    @validator("dev_phone")
    def validate_dev_phone(cls, v):
        if v.startswith("+"):
            return v[1:]

        if len(v) != 11:
            raise ValueError(
                "Please provide your phone number in E.164 format, "
                "with or without the leading +."
            )

        return v

    @validator("default_timezone")
    def validate_default_timezone(cls, v):
        try:
            pytz.timezone(v)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(
                "Please provide a valid timezone from the tz database, "
                "ex. America/New_York."
            )

        return v

    
class SecurityConfig(BaseModel):
    """
    Security configuration, validation of various services.

    Attributes:
        validate_twilio_inbound (bool): Whether to validate inbound Twilio requests.
        validate_telegram_inbound (bool): Whether to validate inbound Telegram requests.
    """
    validate_twilio_inbound: bool 
    validate_telegram_inbound: bool 


class WeatherConfig(BaseModel):
    """
    Weather configuration, affects the weather API.

    Attributes:
        default_city (str): The default city to use for weather requests.
    """
    default_city: str


class GroceriesConfig(BaseModel):
    """
    Groceries configuration, affects the groceries API.

    Attributes:
        translation (bool): Whether to translate the grocery list to English.
        full_dt_format (str): The format to use for full datetimes.
    """
    translation: bool
    full_dt_format: str


class CocktailsConfig(BaseModel):
    """
    Cocktails configuration, affects the cocktails API.

    Attributes:
        result_limit (int): The maximum number of results to return.
    """
    result_limit: int


class GPTConfig(BaseModel):
    """
    GPT configuration, affects the GPT API.

    Attributes:
        console_agent (bool): Whether to log to the console.
    """
    console_agent: bool


class TelegramConfig(BaseModel):
    """
    Telegram configuration, affects the Telegram API.

    Attributes:
        voice_note_responses (bool): Send voice note responses when spoken to.
        threaded_inbound (bool): Whether to process inbound Telegram in a thread.
    """
    voice_note_responses: bool
    threaded_inbound: bool


class Config(BaseModel):
    """
    Base Model collecting and validating all individual configurations.
    
    Attributes:
        General (GeneralConfig): General configuration.
        Weather (WeatherConfig): Weather configuration.
        Groceries (GroceriesConfig): Groceries configuration.
        Cocktails (CocktailsConfig): Cocktails configuration.
        GPT (GPTConfig): GPT configuration.
    """
    General: GeneralConfig
    Security: SecurityConfig
    Weather: WeatherConfig
    Groceries: GroceriesConfig
    Cocktails: CocktailsConfig
    GPT: GPTConfig
    Telegram: TelegramConfig
