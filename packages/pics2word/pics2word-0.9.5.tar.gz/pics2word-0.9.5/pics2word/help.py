def help(arg):
    Message = {}
    Message['help'] = '''Usage: pics2word [-command] [value]
Options:
\t-h\t- Pass "help" to print this help message to the terminal.
\t\t  Pass the name of a command below without the '-' for more informatio about that command.
\t\t  Pass "?" if you cant find what you are looking for or having issues.
\t-P\t- Pass an alternative path to be used. i.e. \"C:\\\\Pictures\\\". Defaults to current directory.
\t-f\t- format pictures. pass either "normal" or "table". Defaults to normal. 
\t-T\t- Override the default title. Defaults to PhotoDoc_<current date> (See Td, below).
\t-Td\t- Choose to append the title with the current date. Options: \"y\" or \"n\". Defaults to \"y\".
\t-pw\t- Set the width of imported pictures in inches. Defaults to 4 inches
\t-ph\t- Set the height of imported pictures in inches. Defaults to 4 inches
\t-tw\t- Set the number of columns used in table format. Note: table format must be enabled! Defaults to 2.
\t-m\t- Module. Allows the creation of templates. 

Commands may be passed as command-value pairs in any order.
All commands are optional and the defaults will be used if no commands are given.

Example: pics2word -P \"C:\\\\Pictures\\\" -T Report -Td n -f table\n'''

    Message['p'] = '''Name: Path command
Function: This allows the user to use pictures from an alternative directory.
Options: Any valid path. i.e. \"C:\\\\user\\Joe Bloggs\\pictures\"
Default: In the absense of any path being passed, the program will 
\t  use the current directory of the terminal running it.'''

    Message['f'] = '''Name: Format command
Function: Allows the user to define the format that the pictures are presented.
\t  Normal simply copies the picture into the table with the title on the next line
\t  Table will copy the pictures into a table with the title in the cell beneath.
Options: "normal" and "table" are valid options.
Default: "normal"'''

    Message['t'] = '''Name: Title command
Function: Allows the user to specify a title for the saved word document.
\t  Note: If this command is used then a value for 'Td' MUST be given. 
Options: If giving a name with spaces then you will need to pass the name in quotes, thus: "my report"
Default: "PhotoDoc_<date>" where <date> is the current date.'''

    Message['td'] = '''Name: Title Date command
Function: Gives the user the option to append the current date at the end of the title of the word document.
\t  Note: If a custom title is used then a value for 'Td' MUST be given.
\t  Example date format is produced thus: "09Mar2018"  For 9th March 2018
Options: 'y' or 'n' for yes or no.
Default: 'y' as part of the default title. Otherwise the user will have to give an option.'''

    Message['pw'] = '''Name: Picture Width
Function: Allows the user to define the width of the picture in inches.
\t  Important: Aspect ratio is preserved. This option restricts the width of landscape pictures only.
\t  for further control it is recommended that the an option for 'ph' also be passed. 
Options: Any positive number. Recommended values of 5 for normal usage, 3 for table usage (2 columns)
Default: 4 inches'''

    Message['ph'] = '''Name: Picture Height 
Function: Allows the user to define the height of the picture in inches.
\t  Important: Aspect ratio is preserved. This option restricts the height of portrait pictures only.
\t  for further control it is recommended that the an option for 'pw' also be passed. 
Options: Any positive number. Recommended values of 5 for normal usage, 2.5 for table usage (2 columns)
Default: 4 inches'''

    Message['tw'] = '''Name: Table Width
Function: Define the number of columns in the table.
\t  Important: The "table" format MUST be specified for this command to take effect.
Options: Any positive integer. Recommended values between 1 & 3 for portrait A4.
Default: 2 columns'''

    Message['m'] = '''Name: Module command
Function: This command allows the user to define and use templates Pass -m "report" to load the arguments saved in that module. 
\t\t  If the module name does not exist then one will be created under the passed name using the passed arguments as saved values.
\t\t  Note that when loading the template, arguments passed with a loaded module will overwrite the template values but do not save permanently.
Options: A valid name for a module must be used. If you are looking to load a module, make sure it exists in the current directory.
Default: If no modifications to the commands are given, then the default values set by the program will be used.'''

    Message['?'] = '''Please report all issues to: https://github.com/Ghostom998/pics2word/issues
Raise a new issue then:
- Please describe the issue as accurately as possible with the ouput from the log file and any error message given in the terminal window.
- Please describe exactly what you did to trigger the event including the commands that were passed
- Note the operating system, version of python used and pics2word version
- Include any further relavent information you deem useful.'''

    try:
        print(Message[arg.lower()])
    except:
        print("Please enter a valid option.\nRemember to pass the right command without the hyphen.")