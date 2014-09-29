#! /usr/bin/env python

"""! @package morphosyntax
"""

class Paradigm():
    """! Paradigm is a class representing a morphological paradigm.
    """
    def __init__(self):
        """! @brief Constructor.
        Paradigm instances are owned by Sense.
        @return A Paradigm instance.
        """
        self.paradigmLabel = None
        self.paradigm = None
        self.language = None
        self.morphology = None
        # LexicalEntry lexeme
        self.targets = None
        ## Pointer to an existing LexicalEntry
        # There is zero or one LexicalEntry pointer per Paradigm instance
        self.__lexical_entry = None

    def __del__(self):
        """! @brief Destructor.
        """
        # Decrement the reference count on pointed objects
        self.__lexical_entry = None

    def get_lexical_entry(self):
        """! @brief Get pointed lexical entry.
        @return Paradigm private attribute '__lexical_entry'.
        """
        return self.__lexical_entry
