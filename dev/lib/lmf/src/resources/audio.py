#! /usr/bin/env python

"""! @package resources
"""

from material import Material

class Audio(Material):
    """! Audio is a Material subclass representing an audio recording.
    """
    def __init__(self):
        """! @brief Constructor.
        Audio instances are owned by FormRepresentation.
        @return An Audio instance.
        """
        self.quality = None
        self.sound = None
        self.startPosition = None
        self.durationOfEffectiveSpeech = None
        self.externalReference = None
        self.audioFileFormat = None
        self.transcription = None
