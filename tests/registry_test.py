import os
import unittest

from pulumi import automation as auto


class RegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.STACK_NAME = cls.__name__
        cls.CONTENT = 'a test string'
        cls.WORK_DIR = os.path.join(os.path.dirname(__file__),'..', 'examples', 'registry')

        cls.stack = auto.create_or_select_stack(stack_name=cls.STACK_NAME, work_dir=cls.WORK_DIR)
        cls.stack.set_config('file_content', auto.ConfigValue(cls.CONTENT))
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(cls.STACK_NAME)

    def test_update(self):
        self.CONTENT = 'another test string'
        self.stack.set_config('file_content', auto.ConfigValue(self.CONTENT))
        self.stack.up(on_output=print)
        self.outputs = self.stack.outputs()
        output = self.outputs.get('content').value
        self.assertEqual(self.CONTENT, output)


if __name__ == '__main__':
    unittest.main()
