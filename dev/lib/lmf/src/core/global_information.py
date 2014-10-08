#! /usr/bin/env python

"""! @package core
"""

from utils.error_handling import Error

class GlobalInformation():
    """! "Global Information is a class for administrative information and other general attributes, such as /language coding/ or /script coding/, which are valid for the entire lexical resource." (LMF)
    """
    def __init__(self):
        """! @brief Constructor.
        GlobalInformation instance is owned by LexicalResource.
        @return A GlobalInformation instance.
        """
        self.languageCode = "ISO-639-3"
        self.author = None
        self.version = "0.1"
        self.lastUpdate = None
        self.license = "GPL"
        self.characterEncoding = "UTF-8"
        self.dateCoding = "ISO-8601"
        self.creationDate = None
        self.projectName = "ANR HimalCo"
        self.description = None
        self.bibliographicCitation = None

    def __del__(self):
        """! @brief Destructor.
        """
        pass

    def check_date_format(self, date):
        """! @brief Verify that date format is composed as follows: YYYY-MM-DD.
        If not, raise an Error.
        @param date Date to check.
        """
        import re
        if not re.match("^\d{4}-\d{2}-\d{2}$", date):
            raise Error("Date must be formatted as follows: YYYY-MM-DD (given date is %s)" % date)

    def set_creationDate(self, date):
        """! @brief Set global information creation date.
        @param date The date to set.
        @return GlobalInformation instance.
        """
        self.check_date_format(date)
        self.creationDate = date
        return self

    def get_creationDate(self):
        """! @brief Get global information creation date.
        @return GlobalInformation attribute 'creationDate'.
        """
        return self.creationDate

    def set_lastUpdate(self, date):
        """! @brief Set global information last update.
        @param date The date to set.
        @return GlobalInformation instance.
        """
        self.check_date_format(date)
        self.lastUpdate = date
        return self

    def get_lastUpdate(self):
        """! @brief Get global information last update.
        @return GlobalInformation attribute 'lastUpdate'.
        """
        return self.lastUpdate

    def set_author(self, author):
        """! @brief Set global information author.
        @param author The author's name to set.
        @return GlobalInformation instance.
        """
        self.author = author
        return self

    def get_author(self):
        """! @brief Get global information author.
        @return GlobalInformation attribute 'author'.
        """
        return self.author

    def set_description(self, description):
        """! @brief Set global information description.
        @param description The description to set.
        @return GlobalInformation instance.
        """
        self.description = description
        return self

    def get_description(self):
        """! @brief Get global information description.
        @return GlobalInformation attribute 'description'.
        """
        return self.description

    def compute_bibliographicCitation(self):
        """! @brief Compute bibliographic citation from date and author.
        Set GlobalInformation attribute 'bibliographicCitation'.
        """
        self.bibliographicCitation = "Online dictionaries"
        if self.get_author() is not None:
            self.bibliographicCitation += ", " + self.get_author()
        if self.get_lastUpdate() is not None:
            self.bibliographicCitation += ", " + self.get_lastUpdate()

    def get_bibliographicCitation(self):
        """! @brief Get global information bibliographic citation.
        @return GlobalInformation attribute 'bibliographicCitation'.
        """
        self.compute_bibliographicCitation()
        return self.bibliographicCitation
