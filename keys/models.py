"""
This module defines Pydantic models for validating a YAML configuration file containing API keys and settings
for various services such as Twilio, Deta, HumorAPI, OpenWeatherMap, OpenAI, GoogleSerper, WolframAlpha,
NewsAPI, ElevenLabs, UploadIO, and Transcription.
"""
from pydantic import BaseModel


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


class NewsAPIModel(BaseModel):
    """
    A Pydantic model for NewsAPI configurations.

    Attributes:
        api_key (str): The NewsAPI API key.
    """
    api_key: str


class ElevenLabsModel(BaseModel):
    """
    A Pydantic model for ElevenLabs configurations.

    Attributes:
        api_key (str): The ElevenLabs API key.
        voice_id (str): The ElevenLabs voice ID.
    """
    api_key: str
    voice_id: str


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
    id_phone_mapping: dict[int, str]


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
    """
    # Required keys (tests and active applets)
    Twilio: TwilioModel
    Deta: DetaModel
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

    # Optional keys (Optional features and inactive applets/features)
    ZapierNLA: dict[str, str] | None
    NewsAPI: NewsAPIModel | None
