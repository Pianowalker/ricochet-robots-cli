"""
Sonidos básicos para la GUI.
Si no hay archivos de sonido, se usan tonos generados con pygame.
"""
import pygame
import math
import array

# Tipos de sonido
SOUND_ROBOT_MOVE = "robot_move"
SOUND_BUMPER_HIT = "bumper_hit"
SOUND_WIN_ROUND = "win_round"
SOUND_LOSE_ROUND = "lose_round"
SOUND_BUTTON_CLICK = "button_click"

_sounds_cache = {}
_mixer_initialized = False


def _init_mixer():
    global _mixer_initialized
    if _mixer_initialized:
        return
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        _mixer_initialized = True
    except pygame.error:
        pass


def _generate_tone(frequency: float, duration_ms: int, volume: float = 0.3) -> pygame.mixer.Sound:
    """Genera un tono sinusoidal como placeholder de sonido."""
    _init_mixer()
    sample_rate = 22050
    n_samples = int(sample_rate * duration_ms / 1000.0)
    max_vol = int(32767 * volume)
    buf = array.array("h")
    for i in range(n_samples):
        t = float(i) / sample_rate
        val = int(max_vol * math.sin(2 * math.pi * frequency * t) * (1 - i / n_samples))
        buf.append(val)
        buf.append(val)
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


def _load_or_create_sounds():
    """Carga archivos desde gui/assets/sounds/ o crea placeholders."""
    if _sounds_cache:
        return
    _init_mixer()
    import os
    base = os.path.join(os.path.dirname(__file__), "assets", "sounds")
    files = {
        SOUND_ROBOT_MOVE: "robot_move.wav",
        SOUND_BUMPER_HIT: "bumper_hit.wav",
        SOUND_WIN_ROUND: "win_round.wav",
        SOUND_LOSE_ROUND: "lose_round.wav",
        SOUND_BUTTON_CLICK: "button_click.wav",
    }
    for key, filename in files.items():
        path = os.path.join(base, filename)
        if os.path.isfile(path):
            try:
                _sounds_cache[key] = pygame.mixer.Sound(path)
            except pygame.error:
                pass
        if key not in _sounds_cache:
            if key == SOUND_ROBOT_MOVE:
                _sounds_cache[key] = _generate_tone(400, 80, 0.2)
            elif key == SOUND_BUMPER_HIT:
                _sounds_cache[key] = _generate_tone(200, 120, 0.25)
            elif key == SOUND_WIN_ROUND:
                _sounds_cache[key] = _generate_tone(523, 150, 0.3)
            elif key == SOUND_LOSE_ROUND:
                _sounds_cache[key] = _generate_tone(150, 200, 0.25)
            elif key == SOUND_BUTTON_CLICK:
                _sounds_cache[key] = _generate_tone(600, 50, 0.2)


def play(sound_name: str):
    """Reproduce un sonido por nombre."""
    _load_or_create_sounds()
    if sound_name in _sounds_cache:
        try:
            _sounds_cache[sound_name].play()
        except pygame.error:
            pass
