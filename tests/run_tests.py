#!/usr/bin/env python3
import unittest
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from unit.test_utils import TestUtils
from unit.test_messages import TestMessages
from unit.test_agent import TestMistralAgent
from unit.test_discord_wrapper import TestDiscordWrapper
from unit.test_moderation import TestModeration

def create_test_suite():
    """Create a test suite containing all tests."""
    test_suite = unittest.TestSuite()
    
    # Add test cases using the correct method
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMessages))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMistralAgent))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDiscordWrapper))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModeration))
    
    return test_suite

if __name__ == "__main__":
    # Create the test suite
    test_suite = create_test_suite()
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful()) 