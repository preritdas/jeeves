"""
This module defines Pydantic models for validating a YAML configuration file containing API keys and settings
for various services such as Twilio, Deta, HumorAPI, OpenWeatherMap, OpenAI, GoogleSerper, WolframAlpha,
NewsAPI, ElevenLabs, UploadIO, and Transcription.
"""
from pydantic import BaseModel


class GeneralModel(BaseModel):
    """
    General items, like protection for the base agent endpoint and an access code
    for authenticating new users (getting their user codes).

    Attributes:
        password (str): The password for the base agent.
    """
    base_agent_password: str
    auth_access_code: str


class TwilioModel(BaseModel):
    """
    A Pydantic model for Twilio configurations.

    Attributes:
        account_sid (str): The Twilio account SID.
        auth_token (str): The Twilio authentication token.
        sender (str): The Twilio sender phone number.
        sender_sid (str): The Twilio sender SID.
        my_number (str): Your Twilio phone number.
    """
    account_sid: str
    auth_token: str
    sender: str
    sender_sid: str
    my_number: str


class DetaModel(BaseModel):
    """
    A Pydantic model for Deta configurations.

    Attributes:
        project_key (str): The Deta project key.
    """
    project_key: str


class MongoDBModel(BaseModel):
    """
    A Pydantic model for MongoDB configurations.

    Attributes:
        connect_str (str): The MongoDB connection string with username and pwd.
    """
    connect_str: str


class HumorAPIModel(BaseModel):
    """
    A Pydantic model for HumorAPI configurations.

    Attributes:
        api_key (str): The HumorAPI key.
    """
    api_key: str


class OpenWeatherMapModel(BaseModel):
    """
    A Pydantic model for OpenWeatherMap configurations.

    Attributes:
        api_key (str): The OpenWeatherMap API key.
    """
    api_key: str


class OpenAIModel(BaseModel):
    """
    A Pydantic model for OpenAI configurations.

    Attributes:
        api_key (str): The OpenAI API key.
    """
    api_key: str


class GoogleSerperModel(BaseModel):
    """
    A Pydantic model for GoogleSerper configurations.

    Attributes:
        api_key (str): The GoogleSerper API key.
    """
    api_key: str


class WolframAlphaModel(BaseModel):
    """
    A Pydantic model for WolframAlpha configurations.

    Attributes:
        app_id (str): The WolframAlpha App ID.
    """
    app_id: str


# class NewsAPIModel(BaseModel):
#     """
#     A Pydantic model for NewsAPI configurations.

#     Attributes:
#         api_key (str): The NewsAPI API key.
#     """
#     api_key: str


class ElevenLabsModel(BaseModel):
    """
    A Pydantic model for ElevenLabs configurations.

    Attributes:
        api_key (str): The ElevenLabs API key.
        voice_id (str): The ElevenLabs voice ID.
        eleven_model (str): The ElevenLabs generation model.
    """
    api_key: str
    voice_id: str
    eleven_model: str = "eleven_monolingual_v1"


class UploadIOModel(BaseModel):
    """
    A Pydantic model for UploadIO configurations.

    Attributes:
        account (str): The UploadIO account ID.
        api_key (str): The UploadIO API key.
    """
    account: str
    api_key: str


class TranscriptionModel(BaseModel):
    """
    A Pydantic model for Transcription configurations.

    Attributes:
        api_url (str): The Transcription API URL.
    """
    api_url: str


class PapertrailModel(BaseModel):
    """
    A Pydantic model for Papertrail logging in the cloud.

    Attributes:
        host (str): The Papertrail host.
        port (int): The Papertrail port.
    """
    host: str
    port: int


class TelegramModel(BaseModel):
    """
    A Pydantic model for Telegram configurations.

    Attributes:
        bot_token (str): The Telegram bot token.
        id_phone_mapping (dict[str, str]): A dictionary mapping ID to phone number.
    """
    bot_token: str
    api_secret_token: str


class ZapierModel(BaseModel):
    """
    Model for Zapier providership.
    
    Attributes:
        provider_id (str): The provider ID.
        client_id (str): The client ID.
        client_secret (str): The client secret key.
    """
    provider_id: str
    client_id: str
    client_secret: str


class Keys(BaseModel):
    """
    A Pydantic model for validating all API keys configurations.

    Attributes:
        Twilio (TwilioModel): The Twilio configuration model.
        Deta (DetaModel): The Deta configuration model.
        HumorAPI (HumorAPIModel): The HumorAPI configuration model.
        OpenWeatherMap (OpenWeatherMapModel): The OpenWeatherMap configuration model.
        OpenAI (OpenAIModel): The OpenAI configuration model.
        GoogleSerper (GoogleSerperModel): The GoogleSerper configuration model.
        ZapierNLA (Dict[str, str]): A dictionary containing phone numbers as keys and API keys as values.
        WolframAlpha (WolframAlphaModel): The WolframAlpha configuration model.
        NewsAPI (NewsAPIModel): The NewsAPI configuration model.
        ElevenLabs (ElevenLabsModel): The ElevenLabs configuration model.
        UploadIO (UploadIOModel): The UploadIO configuration model.
        Transcription (TranscriptionModel): The Transcription configuration model.
        Papertrail (PapertrailModel): The Papertrail logging configuration model.
        Telegram (TelegramModel): The Telegram configuration model.
        Zapier (ZapierModel): The Zapier configuration model.
    """
    # Required keys (tests and active applets)
    General: GeneralModel
    Twilio: TwilioModel
    Deta: DetaModel
    MongoDB: MongoDBModel
    HumorAPI: HumorAPIModel
    OpenWeatherMap: OpenWeatherMapModel
    OpenAI: OpenAIModel
    GoogleSerper: GoogleSerperModel
    WolframAlpha: WolframAlphaModel
    ElevenLabs: ElevenLabsModel
    UploadIO: UploadIOModel
    Transcription: TranscriptionModel
    Papertrail: PapertrailModel
    Telegram: TelegramModel
    Zapier: ZapierModel
    
