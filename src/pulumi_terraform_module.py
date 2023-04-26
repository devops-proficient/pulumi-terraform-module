import binascii
import os
import json

from typing import Protocol, Optional

from pathlib import Path
from tempfile import TemporaryDirectory

from pulumi import Input, Output
from pulumi.dynamic import ResourceProvider, Resource, CreateResult, DiffResult, UpdateResult

from tftest import TerraformTest, TerraformPlanOutput, TerraformState



class ModuleProtocol(Protocol):
    @property
    def source(self) -> str:
        pass
    @property
    def version(self) -> str:
        pass
    @property
    def inputs(self) -> dict:
        pass


class ModuleRaw:
    source: str
    version: Optional[str] = None
    inputs: Optional[dict] = {}
    def __init__(self, source, version = None, inputs = {}, outputs = {}, tf_state=''):
        self.source = source
        self.version = version
        self.inputs = inputs


class ModuleInputs(object):
    source: Input[str]
    version: Input[str]
    inputs: Input[dict]
    def __init__(self, source, version = None, inputs = {}):
        self.source = source
        self.version = version
        self.inputs = inputs


class ModuleProvider(ResourceProvider):
    def create(self, args):
        module, main_tf = generate_tf_module_from(args)

        with TemporaryDirectory(prefix='pulumi-tf-m') as temp_dir:
            tf = setup_terraform(main_tf, temp_dir)
            output = tf.plan(output=True, tf_vars=module.inputs)

            copy_outputs(main_tf, output)
            write_main_tf(main_tf, Path(temp_dir))   

            output = tf.apply(tf_vars=module.inputs, color=True)
            print_output(output)    
            state = tf.state_pull()
            args['tf_state'] = json.dumps(state._raw)
            args['outputs'] = collect_outputs(state)
            
        return CreateResult("tf-"+binascii.b2a_hex(os.urandom(16)).decode("utf-8"), outs=args)
    
    def delete(self, id, args):
        module, main_tf = generate_tf_module_from(args)

        with TemporaryDirectory(prefix='pulumi-tf-m') as temp_dir:
            tf = setup_terraform(main_tf, temp_dir, args.get('tf_state', ''))
            output = tf.plan(output=True, tf_vars=module.inputs)

            copy_outputs(main_tf, output)
            write_main_tf(main_tf, Path(temp_dir))   

            output = tf.destroy(tf_vars=module.inputs, color=True)
            print_output(output)    
    
    def diff(self, id, old_inputs, new_inputs):
        module, main_tf = generate_tf_module_from(new_inputs)

        with TemporaryDirectory(prefix='pulumi-tf-m') as temp_dir:
            tf = setup_terraform(main_tf, temp_dir, old_inputs.get('tf_state', ''))
            output = tf.plan(output=True, tf_vars=module.inputs)

            changes = []
            for resource in output.get('resource_changes', []):
                if 'no-op' not in resource.get('change', {}).get('actions', []):
                    changes.append(resource.get('address', 'Unknown'))
            for output_name, output in  output.get('output_changes', {}).items():
                if 'no-op' not in resource.get('actions', []):
                    changes.append(output_name)

        return DiffResult(
            changes=len(changes) > 0,
            replaces=[],
            stables=['tf_state'],
            delete_before_replace=False)

    def update(self, id, old_inputs, new_inputs):
        module, main_tf = generate_tf_module_from(new_inputs)

        with TemporaryDirectory(prefix='pulumi-tf-m') as temp_dir:
            tf = setup_terraform(main_tf, temp_dir, old_inputs.get('tf_state', ''))
            output = tf.plan(output=True, tf_vars=module.inputs)

            copy_outputs(main_tf, output)
            write_main_tf(main_tf, Path(temp_dir))   

            output = tf.apply(tf_vars=module.inputs, color=True)
            print_output(output)    
            state = tf.state_pull()
            new_inputs['tf_state'] = json.dumps(state._raw)
            new_inputs['outputs'] = collect_outputs(state)

        return UpdateResult(outs=new_inputs)


class Module(Resource):
    source: Output[str]
    version: Output[str]
    inputs: Output[dict]
    outputs: Output[dict]
    tf_state: Output[str]
    def __init__(self, name: str, args: ModuleInputs, opts = None):
        full_args = {**vars(args), 'outputs': None, 'tf_state': None}
        super().__init__(ModuleProvider(), name, full_args, opts)


def print_output(output: str) -> None:
    print(output)


def setup_terraform(main_tf: str, temp_dir: str, tf_state: str = None) -> TerraformTest:
    write_main_tf(main_tf, Path(temp_dir))
    if tf_state:
        write_tfstate(tf_state, Path(temp_dir))
    tf = TerraformTest(temp_dir)
    tf.setup()
    return tf


def generate_tf_module_from(args: dict) -> dict:
    module_atrr = {k: v for k, v in args.items() if not k.startswith('__')}
    module = ModuleRaw(**module_atrr)

    return module, generate_tf_module(module)


def generate_tf_module(module: ModuleProtocol) -> dict:
    if module.source.startswith('./'):
        source = os.path.abspath(module.source)
    else:
        source = module.source
    main_tf = {'module': [{'execute': [{}]}]}
    main_tf['module'][0]['execute'][0]['source'] = source
    if module.version:
        main_tf['module'][0]['execute'][0]['version'] = module.version

    main_tf['variable'] = []
    for output_name, v in module.inputs.items():
        main_tf['variable'].append({output_name: [{'default': v}]})
        main_tf['module'][0]['execute'][0][output_name] = v
    return main_tf


def copy_outputs(main_tf: dict, plan: TerraformPlanOutput) -> dict:
    main_tf['output'] = []
    for output_name, v in plan['configuration']['root_module']['module_calls']['execute']['module']['outputs'].items():
        main_tf['output'].append({output_name: [{'sensitive': v.get('sensitive', False), 'value': '${{module.execute.{}}}'.format(output_name)}]})

    return main_tf


def collect_outputs(state: TerraformState) -> dict:
    return dict([(k, v.get('value')) for k,v in state.get('outputs', {}).items()])


def write_tfstate(state: str, temp_dir: Path) -> None:
    with open((temp_dir / 'terraform.tfstate'), 'w') as f:
        f.write(state)


def write_main_tf(main_tf: dict, temp_dir: Path) -> None:
    with open((temp_dir / 'main.tf.json'), 'w') as f:
        f.write(json.dumps(main_tf))
