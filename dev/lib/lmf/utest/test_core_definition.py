#! /usr/bin/env python

from startup import *
from core.definition import Definition
from core.statement import Statement

## Test Definition class

class TestDefinitionFunctions(unittest.TestCase):

    def setUp(self):
        # Instantiate a Definition object
        self.definition = Definition()

    def tearDown(self):
        # Release instantiated objects
        del self.definition

    def test_init(self):
        self.assertIsNone(self.definition.language)
        self.assertIsNone(self.definition.definition)
        self.assertIsNone(self.definition.gloss)
        self.assertIsNone(self.definition.literally)
        self.assertListEqual(self.definition.text_representation, [])
        self.assertListEqual(self.definition.statement, [])

    def test_set_language(self):
        lang = "Python"
        self.assertIs(self.definition.set_language(lang), self.definition)
        self.assertEqual(self.definition.language, lang)

    def test_get_language(self):
        # Set language
        lang = "python"
        self.definition.language = lang
        # Test get language
        self.assertEqual(self.definition.get_language(), lang)

    def test_set_definition(self):
        # Test definition only
        definition = "blablabla"
        self.assertIs(self.definition.set_definition(definition), self.definition)
        self.assertEqual(self.definition.definition, definition)
        # Test definition and language
        definition = "This is a definition."
        language = "eng"
        self.assertIs(self.definition.set_definition(definition, language), self.definition)
        self.assertEqual(self.definition.definition, definition)
        self.assertEqual(self.definition.language, language)

    def test_get_definition(self):
        # Set definition
        definition = "whatever"
        self.definition.definition = definition
        # Test get definition
        self.assertEqual(self.definition.get_definition(), definition)
        # Test with a language filter
        language = "eng"
        self.definition.language = language
        self.assertEqual(self.definition.get_definition(), definition)
        self.assertIsNone(self.definition.get_definition("fra"))
        self.assertEqual(self.definition.get_definition(language), definition)

    def test_set_gloss(self):
        # Test gloss only
        gloss = "BLA"
        self.assertIs(self.definition.set_gloss(gloss), self.definition)
        self.assertEqual(self.definition.gloss, gloss)
        # Test gloss and language
        gloss = "This is a gloss."
        language = "eng"
        self.assertIs(self.definition.set_gloss(gloss, language), self.definition)
        self.assertEqual(self.definition.gloss, gloss)
        self.assertEqual(self.definition.language, language)

    def test_get_gloss(self):
        # Set gloss
        gloss = "WHATEVER"
        self.definition.gloss = gloss
        # Test get gloss
        self.assertEqual(self.definition.get_gloss(), gloss)
        # Test with a language filter
        language = "eng"
        self.definition.language = language
        self.assertEqual(self.definition.get_gloss(), gloss)
        self.assertIsNone(self.definition.get_gloss("fra"))
        self.assertEqual(self.definition.get_gloss(language), gloss)

    def test_create_statement(self):
        # Test create statement
        statement = self.definition.create_statement()
        self.assertIsInstance(statement, Statement)
        # Release Statement instance
        del statement

    def test_add_statement(self):
        # Create statements
        state1 = Statement()
        state2 = Statement()
        # Test add statements to the definition
        self.assertIs(self.definition.add_statement(state1), self.definition)
        self.assertListEqual(self.definition.statement, [state1])
        self.assertIs(self.definition.add_statement(state2), self.definition)
        self.assertListEqual(self.definition.statement, [state1, state2])
        # Release Statement instances
        del self.definition.statement[:]
        del state1, state2

    def test_get_statements(self):
        # List of Statement instances is empty
        self.assertListEqual(self.definition.get_statements(), [])
        # Create Statement instances and add them to the list
        state1 = Statement()
        state2 = Statement()
        self.definition.statement = [state1, state2]
        # Test get statements
        self.assertListEqual(self.definition.get_statements(), [state1, state2])
        # Delete Statement instances
        del self.definition.statement[:]
        del state1, state2

    def test_set_note(self):
        note = "note"
        # There is no Statement instance
        self.assertIs(self.definition.set_note(note), self.definition)
        self.assertEqual(len(self.definition.statement), 1)
        self.assertEqual(self.definition.statement[0].note, note)
        # Test set a second note
        language = "Python"
        self.assertIs(self.definition.set_note(note, language=language), self.definition)
        self.assertEqual(len(self.definition.statement), 2)
        self.assertEqual(self.definition.statement[1].note, note)
        self.assertEqual(self.definition.statement[1].language, language)

    def test_find_notes(self):
        # Create several statements with different notes, types and languages
        state1 = Statement().set_note("note1", "comparison", "eng")
        state2 = Statement().set_note("note2", "general", "fra")
        state3 = Statement().set_note("note3", "comparison")
        state4 = Statement().set_note("note4", "history")
        # Add statements to the definition
        self.definition.statement = [state1, state2, state3, state4]
        # Test find notes
        self.assertListEqual(self.definition.find_notes("general"), [state2.note])
        # List is randomly ordered => create a set to avoid random results
        self.assertEqual(set(self.definition.find_notes("comparison")), set([state1.note, state3.note]))
        # Release Statement instances
        del self.definition.statement[:]
        del state1, state2, state3, state4

suite = unittest.TestLoader().loadTestsFromTestCase(TestDefinitionFunctions)

## Run test suite

testResult = unittest.TextTestRunner(verbosity=2).run(suite)
