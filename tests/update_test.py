import os
import unittest

from pulumi import automation as auto


class UpdateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.STACK_NAME = cls.__name__
        cls.INPUT = '123'
        cls.WORK_DIR = os.path.join(os.path.dirname(__file__),'..', 'examples', 'local')

        cls.stack = auto.create_or_select_stack(stack_name=cls.STACK_NAME, work_dir=cls.WORK_DIR)
        cls.stack.set_config('input', auto.ConfigValue(cls.INPUT))
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(cls.STACK_NAME)

    def test_update(self):
        self.INPUT = '1234'
        self.stack.set_config('input', auto.ConfigValue(self.INPUT))
        self.stack.up(on_output=print)
        self.outputs = self.stack.outputs()
        output = self.outputs.get('input').value
        self.assertEqual('output-'+self.INPUT, output)


if __name__ == '__main__':
    unittest.main()
