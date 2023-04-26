import pulumi

from pulumi_terraform_module import Module, ModuleInputs

config = pulumi.Config()
file_content = config.require('file_content')

module = Module(name='registry-module', 
                args=ModuleInputs(source='opendevsecops/file/local', 
                                    version='0.2.0',
                                    inputs={
                                        'filename': 'testfile.txt',
                                        'content': file_content
                                    }))

pulumi.export('filename', module.outputs.apply(lambda outputs: outputs.get('filename')))
pulumi.export('content', module.outputs.apply(lambda outputs: outputs.get('content')))