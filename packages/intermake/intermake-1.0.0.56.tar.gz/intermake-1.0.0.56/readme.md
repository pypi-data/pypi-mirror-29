Intermake
=========
___APPLICATION FRONTEND VIA REFLECTION___

[](toc)

What is Intermake?
------------------

Iɴᴛᴇʀᴍᴀᴋᴇ is a library that automatically provides multiple front-ends a Pʏᴛʜᴏɴ application.
The following frontends are provided:

* `ARG`: Call from **command line arguments**
* `CLI`: Interactive terminal-like shell (**CLI**)
* `PYI`: Interactive **Pʏᴛʜᴏɴ shell** (PYI)
* `GUI`: Graphical user interface (**GUI**)
* `PYS`: Call from any **Pʏᴛʜᴏɴ script** or application
* `JUP`: Interactive **Jᴜᴩʏᴛᴇʀ** notebook
* `***`: **Custom** front-ends are also supported


### Rationale ###

Unlike other utilities, Iɴᴛᴇʀᴍᴀᴋᴇ:
* Requires minimal setup – only an `import intermake` and the `@command` decorator
* Isn't intrusive or branding
* Generates help and documentation _automatically_ – using the [PEP-257](https://www.python.org/dev/peps/pep-0257/) documentation you probably already use
* Generates an _appropriate_ UI _automatically_:
    * Uses [PEP-484](https://www.python.org/dev/peps/pep-0484/) annotations
    * Converts information provided by the user _automatically_:
        * A function, requiring an `int`, receives an `int`, not the `str` the user typed
        * A function, requiring a `MyOwnClass`, receives a `MyOwnClass`
    * Supports annotation hints:
        * Function defaults
        * The `typing` library: `List[T]`, `Union[T, U]`, `Optional[T]`, etc.
        * Includes custom-annotations: `Filename[extension]` (str), `Dirname` (str), `Nonzero[T]` (T)
* Abstracts common concepts – progress bars, feedback to user, questions to user, etc.
* Abstracts threading to the host UI


Instructions
------------

* Please go to the [usage tutorial](#Usage-tutorial) section for how to **use** an Iɴᴛᴇʀᴍᴀᴋᴇ application
* Please go to the [development tutorial](#Development-tutorial) section for how to **create** an Iɴᴛᴇʀᴍᴀᴋᴇ application


Usage tutorial
--------------

Where `sample` is the name of your application, the following command will launch it:

| Mode                                 | Command                                          |
|--------------------------------------|--------------------------------------------------|
| ARG: Command-line arguments          | `sample "<commands>"`                            |
| CLI: Command line interface          | `sample`                                         |
| GUI: Graphical user interface        | `sample gui`                                     |
| PYI: Pʏᴛʜᴏɴ interactive shell        | `sample pyi`                                     |
| PYS: Interface for Pʏᴛʜᴏɴ scripting  | `import sample`                                  |

Iɴᴛᴇʀᴍᴀᴋᴇ provides an ***extensive, context-dependent, in-line help*** system.

For instance, inside `sample` CLI, use the `help` command to get started:

```bash
$   help
    ECO help
    INF   _help____________________________________________
          Aliases: basic_help
    
                        You are in command-line mode.
    
... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
```

Using the inbuilt interfaces
----------------------------

### Command Line Interactive (CLI) ###

Iɴᴛᴇʀᴍᴀᴋᴇ applications support a Command Line Interactive UI, with a Paup-like interface.
To start this, from your terminal, type:

```bash
intermake
```

Where `intermake` is replaced by the name of your application.

Once in CLI mode, type commands to run them.
e.g. to see the list of the application's commands type:

```
cmdlist
```

Or to run the "eggs" command type:

```
eggs
```
    
(You can abbreviate all commands, so you can also just type `egg`)

You can use `?` to get help on a command:

```
eggs?
```
    
(You can also type `?eggs` or `help eggs`)

See that "eggs" takes two arguments, "name" and "good".

You can specify the arguments after the command:

```
eggs Humpty True
```

You can also name the arguments:

```
eggs good=True
```

You can also use `?` to get help on the last argument:

```
eggs name?
```

Specify `+` to quickly set boolean arguments:

```
eggs +good
```
    
In CLI mode you can abbreviate all arguments, so you can just use `eggs +g`.
CLI mode is case insensitive, so `eggs`, `EGGS` and `Eggs` are all the same.
CLI mode also uses underscore (`_`) dot (`.`) and dash (`-`) interchangeably.

To pass multiple commands on the same line use ` : ` (surrounded with spaces)

```
eggs Tweedledum : eggs Tweedledee
``` 

You need to use quotes to pass parameters with spaces:

```
eggs "Humpty Dumpty"
```

### Python Interactive (PYI) ###

Iɴᴛᴇʀᴍᴀᴋᴇ apps can be run from a Python Interactive session (PYI mode).
To start your application in PYI mode, from your terminal just type

```
intermake pyi
```

Where `intermake` is replaced by the name of your application.
Once in PYI mode the interface behaves like regular Python.
The application's commands have already been imported into the global namespace. 
e.g. to see the list of the application's commands type:

```
cmdlist()
```

Or, to run the `eggs` command:

```
eggs()
```

All commands are Python objects, so you can use `.help()` for help:

```
eggs.help()
```

See that `eggs` takes two arguments, `name` and `good`.

You can specify arguments like so:

```
eggs("Humpty", True)
```

Or you can name them:

```
eggs(name = "Humpty", good = True)
```
    
For help on Python itself, invoke the standard Python help via:

```
python_help()
```

### Python Scripted (PYS) ###
Iɴᴛᴇʀᴍᴀᴋᴇ apps can be run from a Python script (PYS mode).

Usage is the same as for any other Python library, simply import the application's namespace.
e.g. where `intermake` is the name of your application:

```python
import intermake
```

You can then run commands as for the PYI mode, e.g. to run the `cmdlist` command:

```python
intermake.cmdlist()
```

Or to run the `eggs` command:

```
intermake.eggs()
```

All commands are Python objects, so you can use `.help()` for help:

```
intermake.eggs.help()
```

See that `eggs` takes two arguments, `name` and `good`.

You can specify arguments like so:

```
eggs("Humpty", True)
```

Or you can name them:

```
eggs(name = "Humpty", good = True)
```
    
For more help on Python itself, invoke the standard Python help via:

```
help()
```

You can start the user interfaces via their respective commands, e.g. to start the CLI run:

```
intermake.cli()
```

For extending an Iɴᴛᴇʀᴍᴀᴋᴇ application and providing your own commands, please see the [development tutorial](#Development-tutorial). 

### Command Line Arguments (ARG) ###

Iɴᴛᴇʀᴍᴀᴋᴇ apps can be run directly from the command line (ARG mode)
For instance, where `intermake` is the name of the application, from your terminal just type:

```
intermake commands ...
```
    
For instance, to see the list of commands type:

```bash
intermake cmdlist
```
    
Or to run the `eggs` command:

```bash
intermake eggs
```
    
(all commands can be abbreviated so you can also use `intermake egg`)

You can use `?` to get help on a command:

```bash
intermake eggs?
```
    
(you can also use `intermake ?eggs` or `intermake help eggs`)

See that "eggs" takes two arguments, "name" and "good".

You can specify the arguments after the command:

```bash
intermake eggs Humpty True
```
    
If it's complex, you can put your command in quotes so as not to confuse your terminal:

```bash
intermake "eggs Humpty True"
```

You can name the arguments:

```bash
intermake eggs good=True
```

You can also use `?` to get help on the last argument:

```bash
intermake eggs name?
```
    
This works for quick reference, if you are busy typing a command:

```bash
intermake eggs name=Humpty good?
```

Specify `+` to quickly set boolean arguments:

```bash
intermake eggs +good
```
    
ARG mode allows you to abbreviate all arguments, so you can just use `intermake eggs +g`
ARG mode is case insensitive, so `eggs`, `EGGS` and `Eggs` are all the same.
ARG mode also uses underscore (`_`) dot (`.`) and dash (`-`) interchangeably.

You should use quotes to pass parameters with spaces:

```bash
intermake eggs "Humpty Dumpty"
```
    
For the list of commands type:

```bash
intermake cmdlist
```
    
To start the UI:

```bash
intermake cli
```

Multiple commands can be specified at once using the Unix-like specifier `--`:

```bash
intermake --cmdlist --cli
```


#### Additional notes ####

* It is fine to surround your entire command string with quotes.
* Same as in the CLI, you can also use ` : ` or ` then ` (surrounded with spaces) to delimit multiple commands. 
* If you don't specify any commands, the CLI UI will start automatically.

### Graphical User Interface (GUI) ###

All Iɴᴛᴇʀᴍᴀᴋᴇ applications can also be run in a graphical user interface (GUI) mode.
To start this mode from your terminal type:

```
intermake gui
```

Where `intermake` is the name of your application.

A window will then appear showing you the available commands.

### Jupyter Notebook (JUP) ###
 
You can load an Intermake application into a Jupyter notebook by running:

```
import intermake
intermake.run_jupyter( "spam" )
```

Where `spam` is substituted for the name of your application.
Following this, usage is the same as PYI mode, with the application's functions added to the global namespace - if you
don't want the application's functions in the global namespace, follow the PYS instructions instead.

Advanced usage
--------------

### Starting the application ###

Please see the [Usage Tutorial](#Usage-tutorial) above. 

### Running a command ###

Please run the `help` command for information on how to run commands and pass arguments to them.
This will give you help specific to the particular mode you are running.

* Examples:
    * CLI: `help`
    * PYS: `import intermake; intermake.help()`
    * PYI: `help()`
    * JUP: `help()`
    * ARG: `my_application help`
    * GUI: Navigate to `plugins/common/help` and click `run`.

### Changing the main settings ###

Use the `local` command to view and modify settings.

* Example:
    * CLI: `local console/error_traceback=True`
* Notes:
    * GUI: This command is an _advanced_ command and is hidden by default. Please see the [listing special commands](#Listing-special-commands) section for information on how to enable advanced commands.


### Listing commands ###

Use the `cmdlist` command to list the most common commands.

* Example:
    * `cmdlist`
* Notes: 
    * GUI: The GUI lists all commands in the main window, so you don't need to do this.


### Listing special commands ###

Advanced commands include lesser used Iɴᴛᴇʀᴍᴀᴋᴇ commands, as well as commands specific to the application.
To show them you can use the `use` command.

* Example:
    * CLI: `use advanced`
* Notes:
    * GUI: From the GUI you will be unable to use the advanced commands without showing them first.
    * Other modes: These modes still allow you to run commands regardless of whether they are hidden or not, however typing `cmdlist` will now show the `advanced` commands.


### Configuring the workspace directory ###

Iɴᴛᴇʀᴍᴀᴋᴇ stores its data in a "workspace" this folder is by default `~/.intermake-data/application-name`, however you can change this by using the `workspace` command.

* Example:
    * CLI: `workspace c:\my\folder`
* Notes:
    * GUI: This command is an _advanced_ command and is hidden by default. Please see the [listing special commands](#Listing-special-commands) section for information on how to enable advanced commands.


### Using compute clusters ###

Use the `compute_cluster` command to configure parallel jobs. This option is only shown by default if there is at least one command supporting a parallel workload.

* Example:
    * CLI: `compute.cluster 7 9

### Switching the user interface ###

Use the `ui` command.

* Example:
    * CLI: `ui gui`


### Exploring object hierarchies ###

Use the `cd` and `ls` commands.

* Example:
    * CLI: `cd ../results`
* Notes:
    * These commands are only shown if the application actually has an object hierarchy to explore. 
    * GUI: The GUI shows the object hierarchies in the main window, so you do not need to use these commands.
    
### Running a script ###

Since Iɴᴛᴇʀᴍᴀᴋᴇ is written in Pʏᴛʜᴏɴ, the best way to write a script is in Python!
However, for simple scripts, it can be easier to use the `source` command to run a sequence of CLI commands from a file:

```bash
my_application source my_file.txt
```


    

Development tutorial
--------------------

### Implementation ###

Get right in there with the full implementation of a simple Iɴᴛᴇʀᴍᴀᴋᴇ application, called Sᴀᴍᴩʟᴇ!
It has two amazing functions "`say_hello`" and "`do_some_work`".
Paste the following contents into the appropriate files:

[`sample/sample/__init__.py`]
```python
from intermake import MCMD, MENV, command

@command()
def say_hello():
    """
    Says hello
    """
    MCMD.print( "hello" )

@command()
def do_some_work( count : int ):
    """
    Does nothing.
    
    :param count: The number of times to do nothing.
    """
    with MCMD.action( "Doing some work for you!", count ) as action:
        for n in range( count ):
            action.increment()

MENV.init( name = "sample" )
```

[`sample/sample/__main__.py`]:
```python
import sample
import intermake

if __name__ == "__main__":
    intermake.start()
```

**_That's all there is!_** The next section describes what we actually did!

### Explanation ###

1. We used the `@command()` decorator to expose our function through Iɴᴛᴇʀᴍᴀᴋᴇ.
2. We properly documented our functions using PEP-287 doc comments :)
3. We properly annotated our function parameters using PEP-484 :)
4. We used the `MCMD` field to obtain the abstraction to the current UI.
    * We called `MCMD.print` to print a message.
    * We called `MCMD.action` to show a progress bar.
5. We set the application name `MENV.init`.
    * (if we don't do this our application just gets called "`Untitled`"!)
6. Finally, we called `intermake.start` to start Iɴᴛᴇʀᴍᴀᴋᴇ with the appropriate UI.

### Running our application ###

This is Pʏᴛʜᴏɴ boilerplate stuff, but if you don't already know:
* Do a quick-and-dirty registration with Pʏᴛʜᴏɴ by running:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/sample`.
alias sample="python3 -m sample"
```

Now you can try out the various modes. They all do the same thing, in different ways...

#### CLI mode ####

```bash
BASH   <<< sample
SAMPLE <<< say_hello
       <<< do_some_work count=10000
       <<< exit
```

#### ARG mode ####

```bash
BASH   <<< sample "say_hello : do_some_work count=10000"
```

#### GUI mode ####

```bash
BASH   <<< sample "ui gui"
SAMPLE <<< *click say_hello*
       <<< *click run*
       <<< *click do_some_work*
       <<< *set count to 10000*
       <<< *click run*
       <<< *close the window*
```

#### PYI mode ####

```bash
BASH   <<< sample "ui pyi"
PYTHON <<< say_hello()
       <<< do_some_work(10000)
```

#### PYS mode ####

```python
PYTHON <<< import sample
       <<< sample.say_hello()
       <<< sample.do_some_work(10000)
```

Advanced development
--------------------

### Calling plugins internally ###

When a plugin (`@command`-decorated function) is called, it is called by the current host.

Normally, this makes no difference; call the plugins as you would any other function, since when you call a plugin you usually be doing so from _within_ another plugin, and the host will _always_ make the call synchronously.

The following code is acceptable:

```python
@command
def spam() -> int:
    return 1
    
@command
def beans() -> int:
    x = spam()
    MCMD.print( str( x ) )
```

* Calling `@command` decorated functions from _outside_ may be asynchronous (see [calling plugins externally](#calling-plugins-externally)).

### Creating your own frontend or GUI ###

You can provide your own frontend by changing `MENV.host_provider`.

An commented example of this can be found in the [Gʀᴏᴏᴛ](https://bitbucket.org/mjr129/groot) application, at `groot/groot/frontends/gui/gui_host.py`.

Note you will have to make concessions for [Calling plugins externally](#calling-plugins-externally), if you want buttons to start specific plugins.

### Calling plugins externally ###

If you define your own host, frontend, GUI, or spawn your own threads, then when you call a plugin it is not guaranteed to block and *the result is not guaranteed to be delivered synchronously*!

For instance, the GUI host cannot runs plugins synchronously since this would block the GUI and freeze the window.
The user might even _cancel_ running the plugin before or whilst it is running.

Results from calling plugins externally must therefore be received _asynchronously_:

```python
@command
def spam() -> int:
    return 1
    
class MyDialogue( QMainWindow, IGuiPluginHostWindow ):
    def plugin_completed( self, result: AsyncResult ) -> None:
        QMessageBox.info( self, "Result", str(result) )

    def on_my_pushbutton_clicked( self, state : bool ):
        spam()
```

Again there is a documented example in [Gʀᴏᴏᴛ](https://bitbucket.org/mjr129/groot), at `groot/groot/frontends/gui/forms/frm_main.py`.

Notes:
* The _default_ `GuiHost` blocks the GUI itself while a plugin is running, hence the user cannot run two plugins at once, and so you don't need to worry about multi-threading from _within_ the plugins!
* The _default_ `ConsoleHost` runs synchronously - console frontends _can_ receive synchronous calls if they make the assumption that they run under a `ConsoleHost`.
* Calling plugins from _within_ plugins is always seamless (see [calling plugins internally](#calling-plugins-internally)).


### Adding support for new types ###

If you have a special class, lets say a `DateTime` class, you probably want Iɴᴛᴇʀᴍᴀᴋᴇ to recognise it, for instance by providing a calendar in the GUI and allowing the user to type dates as `xx/xx/xx` in the console.


#### GUI ####
* Iɴᴛᴇʀᴍᴀᴋᴇ uses the Eᴅɪᴛᴏʀɪᴜᴍ library to supply the Qᴛ GUI editor.
    * To add GUI support for new types call `editorium.register` 
    * See the [Editorium](https://bitbucket.org/mjr129/editorium) package itself for details.


#### CLI/ARG ####
* Iɴᴛᴇʀᴍᴀᴋᴇ uses the SᴛʀɪɴɢCᴏᴇʀᴄɪᴏɴ library to supply the CLI translations from text.
    * To add support for translation from text to new types `stringcoercion.register`
    * See the [StringCoercion](https://bitbucket.org/mjr129/stringcoercion) package itself for details.  
    
    
### Creating advanced plugins ###

In our example we provided a _plugin_ through the `@command` decorator, this:
    * Creates a `CommandPlugin` object, with the decorated function as its target.
    * Calls `MENV.plugins.register` on the created object.

You can just as easily create your own plugin instances and register them yourself.
All plugins inherit from the `Plugin` class, which is well documented.
See `HelpPlugin` and `SetterPlugin` for examples of some inbuilt classes which derive from `Plugin`.


### Creating extensions ###

Iɴᴛᴇʀᴍᴀᴋᴇ runs as a singleton instance; you cannot have two Iɴᴛᴇʀᴍᴀᴋᴇ applications hosted by the same process.

Normally, you set `MENV.name` once and, if you try to change the name again, an error is raised.
This way, if you accidentally import another `Intermake` application into the current one, you'll get an error, rather than ending up with some weird chimera of both applications.

That said, applications _can_ build on top of each other, providing increased levels of functionality.

* To add plugins to an existing application:
    * Import the existing application's module, then use `@command` to register your own plugins.
* To build on top of an existing application, replacing the name, version, root object, etc.
    * Import the existing application's module, then call `MENV.unlock` to let Iɴᴛᴇʀᴍᴀᴋᴇ know the name change is intentional, rather than accidental.
* To provide a new application, that can optionally extend an existing application. 
    * Check `MENV.is_locked`. If this is `True`, another Iɴᴛᴇʀᴍᴀᴋᴇ application is already setup, proceed to add plugins as required but don't redefine the Intermake environment.
    
See also: [Locked envirionment error](#locked-envirionment-error).


### Customising the application ###

The example above set only the application title, more customisations are available via the `MENV` field, notably the `root` field, that exposes an application hierarchy derived from `IVisualisable`:

```python
MENV.root = my_root
```

Once your root is set, the user can navigate your hierarchy using UNIX/DOS like commands:

```bash
$   sample
$   cd plugins
```

The `MENV` field itself is a `__Environment` object defined in `environment.py`.

***Please see the doc-comments on `__Environment` and `IVisualisable` for full details.***

System requirements
-------------------

* Iɴᴛᴇʀᴍᴀᴋᴇ uses type annotations, which require at least Pʏᴛʜᴏɴ 3.6.
    * This must be installed first. 

* Supported platforms
    * Windows 7,8
        * Iɴᴛᴇʀᴍᴀᴋᴇ uses Cᴏʟᴏʀᴀᴍᴀ to add support for ANSI-escape sequences
        * Iɴᴛᴇʀᴍᴀᴋᴇ instructs the user on how to enable UTF-8
    * Windows 10
    * Ubuntu
    * MacOS
        * Beware that this ships with a legacy version of Pʏᴛʜᴏɴ 2 by default, you'll need to update!

* Terminal environment requisites (`CLI`/`ARG`/`PYI`/`PYS`)
    * ANSI escape sequences
        * _If not supported_: Weird characters in console output
    * ANSI colours (optional)
        * _If not supported_: No colours will be shown
    * UTF8 (optional)
        * _If not supported_: Weird/missing data in console output.
            * Note: Pʏᴛʜᴏɴ itself must still be notified via the `PYTHONIOENCODING` environment variable, e.g. `export PYTHONIOENCODING=ascii:replace`. If this is not done the application will crash (Iɴᴛᴇʀᴍᴀᴋᴇ supplements the Python error with a more helpful error description).
    * _readline_
        * _If not supported_: Up/down will not work to invoke command history in console. 

* Graphical user interface requisites (`GUI`)
    * _PyQt5_.
        * Note: at the time of writing, some versions of Ubuntu ship with a broken _Qt_/_PyQt5_/_Sip_ install, giving a `killed 9` or `segfault` error on GUI startup. This will require re-installation of _Qt_/_PyQt_/_Sip_ by the user.
        * _If not supported_: Cannot start GUI. Iɴᴛᴇʀᴍᴀᴋᴇ's UI components are isolated so the console modes should still work fine providing the application itself also isolates its GUI (which it should).
    
Troubleshooting
---------------

### Generally weird errors ###

User errors:

* Iɴᴛᴇʀᴍᴀᴋᴇ requires at least Pʏᴛʜᴏɴ 3.6.
    * (This is especially problematic on Mac, which for some reason ships with a legacy version of Pʏᴛʜᴏɴ 2) 


### Unicode errors ###

User errors:

* You're using Pʏᴛʜᴏɴ 2, Iɴᴛᴇʀᴍᴀᴋᴇ requires at least Pʏᴛʜᴏɴ 3.6.
* You've changed the terminal encoding.
    * Check the solutions for Ubuntu and Windows below, regardless of your platform.

On Ubuntu:

* Problem: The terminal is using an implicit encoding `LC_ALL=C`. Pʏᴛʜᴏɴ can't handle this.
    * Solution - Use UTF8. Call `export LC_ALL="en_GB.utf8"` from the command line.
        * (Replace the `en_GB` (UK) with your own locale, e.g. `es.utf8` for Spain or `zh_CN.utf8` for China.)

On Windows:

* Problem: `cmd.exe` or _PowerShell_ with an `ASCII`-only font.
    * Solution - Change your font to a Unicode one.
    * Quick workaround - call `set PYTHONIOENCODING=ascii:replace` from the command line
    
On Mac:

* No known problems unless you've reconfigured your terminal, see "User errors" above.


### Segmentation fault, killed 9, or GUI fails to run ###

On Ubuntu:

* Problem: At the time of writing, some Linux systems have a corrupt installation of PyQt and/or Qt.
    * Solution: Build PyQt and/or Qt properly from source yourself, see: 
        * [riverbankcomputing.com](https://riverbankcomputing.com/software/pyqt/intro)
        * [qt.io](https://www.qt.io/)
    * Workaround: Just use your Iɴᴛᴇʀᴍᴀᴋᴇ application from one of the CLI modes.
    
On Windows or Mac:

* No known problems

On other systems (e.g. Android):

* Problem: Qt is not supported.
    * Solution: See if you can find a Qt installation for your system.
    * Workaround: Use your Iɴᴛᴇʀᴍᴀᴋᴇ application from one of the CLI modes.
    
    
### An Iɴᴛᴇʀᴍᴀᴋᴇ application doesn't start for some other reason ###

User errors:

* Problem: Requisite libraries not installed
    * Solution: Please follow the installation instructions included with the application, generally your software should have been installed via `pip`, here are some common errors:
        * You are using `pip` for Pʏᴛʜᴏɴ2 to try and install a Pʏᴛʜᴏɴ3 application.
        * You are running `pip` without sufficient privileges:
            * Use `sudo` (UNIX)
            * Use the administrator shell (Windows)
            * Use `virtualenv`
            
    
### General errors ###

Coding errors:

* Problem: A Iɴᴛᴇʀᴍᴀᴋᴇ error occurs.
    * Solution: Report it so it can be fixed. Please include the debug information in your bug report. 
        * GUI: Iɴᴛᴇʀᴍᴀᴋᴇ writes debugging information to the console (`stderr`) whenever it encounters an error in the GUI.
          Launch the GUI from the command line (e.g. `./xxxx "ui gui"`) to see this information.
        * CLI: If an error occurs in the CLI version, details can be retrieved using the `error` command.
            * You can instruct all errors to be dumped by default via the `set` command.
    * Solution: Fix it yourself! All Iɴᴛᴇʀᴍᴀᴋᴇ code is heavily documented in-line using standard Pʏᴛʜᴏɴ documentation. 
    
    
### Hard to read text in CLI mode ###

Iɴᴛᴇʀᴍᴀᴋᴇ does its best to use colours to distinguish on-screen items, and expects standard ANSI/DOS colours.
If you're getting unreadable items, such as yellow text on a white background, the colours should be changed in your terminal preferences (not the Iɴᴛᴇʀᴍᴀᴋᴇ application itself).
Modify your terminal profile/theme or simply turn off ANSI colour support.


### Locked environment error ###

If you get a locked environment error, you've tried to `import` another Iɴᴛᴇʀᴍᴀᴋᴇ application module, and that application is trying to overwrite the current one.
This might be because:
* You've using `import` on an unrelated Iɴᴛᴇʀᴍᴀᴋᴇ application.
* You're trying to `unpickle` data from that application.
* You've not checked `MENV.is_locked`.
* You've not called `MENV.unlock`.

See [creating extensions](#creating-extensions) for further details.





Meta
----

```ini
type        = library
author      = Martin Rusilowicz
language    = python3
created     = 2017
host        = bitbucket,pypi
```
