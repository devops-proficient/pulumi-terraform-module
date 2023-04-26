## Pulumi Terraform Module
Use your battle-tested or 3rd party terraform modules directly in your pulumi workflow.


## Examples

### Local Terraform module
```python
module = Module(name='local-module', 
                args=ModuleInputs(source='./tf', 
                                  inputs={'input': 'some_input'}))

```


### Registry Terraform module
```python
module = Module(name='registry-module', 
                args=ModuleInputs(source='opendevsecops/file/local', 
                                    version='0.2.0',
                                    inputs={
                                        'filename': 'testfile.txt',
                                        'content': 'some_content'
                                    }))
```

See [examples](tree/main/examples) for more details.


### Output

```
@ updating....
    pulumi:pulumi:Stack local-UpdateTest running
 +  pulumi-python:dynamic:Resource local-module creating (0s)
@ updating.......
    pulumi:pulumi:Stack local-UpdateTest running Terraform used the selected providers to generate the following execution
    pulumi:pulumi:Stack local-UpdateTest running plan. Resource actions are indicated with the following symbols:
    pulumi:pulumi:Stack local-UpdateTest running   + create
    pulumi:pulumi:Stack local-UpdateTest running Terraform will perform the following actions:
    pulumi:pulumi:Stack local-UpdateTest running   # module.execute.random_string.random will be created
    pulumi:pulumi:Stack local-UpdateTest running   + resource "random_string" "random" {
    pulumi:pulumi:Stack local-UpdateTest running       + id               = (known after apply)
    pulumi:pulumi:Stack local-UpdateTest running       + length           = 16
    pulumi:pulumi:Stack local-UpdateTest running       + lower            = true
    pulumi:pulumi:Stack local-UpdateTest running       + min_lower        = 0
    pulumi:pulumi:Stack local-UpdateTest running       + min_numeric      = 0
    pulumi:pulumi:Stack local-UpdateTest running       + min_special      = 0
    pulumi:pulumi:Stack local-UpdateTest running       + min_upper        = 0
    pulumi:pulumi:Stack local-UpdateTest running       + number           = true
    pulumi:pulumi:Stack local-UpdateTest running       + numeric          = true
    pulumi:pulumi:Stack local-UpdateTest running       + override_special = "/@£$"
    pulumi:pulumi:Stack local-UpdateTest running       + result           = (known after apply)
    pulumi:pulumi:Stack local-UpdateTest running       + special          = true
    pulumi:pulumi:Stack local-UpdateTest running       + upper            = true
    pulumi:pulumi:Stack local-UpdateTest running     }
    pulumi:pulumi:Stack local-UpdateTest running Plan: 1 to add, 0 to change, 0 to destroy.
    pulumi:pulumi:Stack local-UpdateTest running Changes to Outputs:
    pulumi:pulumi:Stack local-UpdateTest running   + a_string = (known after apply)
    pulumi:pulumi:Stack local-UpdateTest running   + input    = "output-123"
    pulumi:pulumi:Stack local-UpdateTest running module.execute.random_string.random: Creating...
    pulumi:pulumi:Stack local-UpdateTest running module.execute.random_string.random: Creation complete after 0s [id=WUrJMvU7YiFh3@JF]
    pulumi:pulumi:Stack local-UpdateTest running Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    pulumi:pulumi:Stack local-UpdateTest running Outputs:
    pulumi:pulumi:Stack local-UpdateTest running a_string = "WUrJMvU7YiFh3@JF"
    pulumi:pulumi:Stack local-UpdateTest running input = "output-123"
 +  pulumi-python:dynamic:Resource local-module created (4s)
    pulumi:pulumi:Stack local-UpdateTest  30 messages

Outputs:
  - a_string: "WUrJMvU7YiFh3@JF"
  - input   : "output-1234"

Resources:
    - 2 created

Duration: 5s
```
