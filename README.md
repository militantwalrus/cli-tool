## Cli Tool "framework" to make a cli tool which does `$ tool [module] [cmd] <options...> <args...>`

### Motivation

TKTK

#### But it _only_ does `$ tool module cmd` things. I just want `$ tool module`...
Then use argparse subparsers, and do 
```
foo_subparser.set_defaults(func=do_foo)
```
and then invoke `opts.func()`

### Implementation

TKTK

### How to Use

Create src/modules/your_module/__init__.py

In src/modules/your_module/__init__.py

1. Imports
```python
from src.commands import  BaseCommand, ToolCommand
```
2. write a class called `Commands(BaseCommand)`
* The class should have a property `USAGE`. See examples.
3. The `Commands(BaseCommand)` `__init__(self, opts: argparse.Namespace):` method should
* Adjust USAGE with `self.command_methods()`. Again, see examples
* Assign `self.arg_parser = argparse.ArgumentParser(usage=self.USAGE)`
* Do any `self.arg_parser.add_argument() calls for module-specific options
* Call `super().__init__()` - Yes, it needs to come last for module-level `--help` to work properly
4. Write the command methods, decorated with `@ToolCommand`.

#### The `@ToolCommand` decorator

Put the `@ToolCommand` decorator from src.util outermost on `Commands` class methods to make them show up in the module/command listing produced by running `$ cli-tool --list`. It MUST go before (above) other decorators such as @MutuallyExclusiveOptions().

#### The `@MutuallyExclusiveOptions()` decorator
Decorate command methods which have mutually exclusive options like `@MutuallyExclusiveOptions(["--yes", "--no"])` to prevent the method being called with options which won't work together.


