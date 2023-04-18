import dataclasses


@dataclasses.dataclass
class Voice:
    service: str
    language: str
    speaker: str
    speed: float
    tone: float
    emotion: str

@dataclasses.dataclass
class CreationTask:
    audio_name: str
    audio_name_source: str
    video_name: str
    video_name_source: str
    voice: Voice
    pause_symbol: str
    text: list
    correction_of_pauses_in_the_voice: int
    pauses_between_segments: int


@dataclasses.dataclass
class RequestData:
    index: int
    text: str
    task: CreationTask
