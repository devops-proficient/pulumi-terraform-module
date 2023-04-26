import pulumi

from pulumi_terraform_module import Module, ModuleInputs

config = pulumi.Config()
input = config.require('input')


module = Module(name='local-module', 
                args=ModuleInputs(source='./tf', 
                                  inputs={'input': input}))


pulumi.export('input', module.outputs.apply(lambda outputs: outputs.get('input')))
pulumi.export('a_string', module.outputs.apply(lambda outputs: outputs.get('a_string')))