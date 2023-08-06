# Pics2Word

A command line program to copy pictures into a word document.

Usage can be found using

`$ pics2word -h help`

## Installation

Installing the Pics2Word software:

1. Install Python (Latest version of 3.X series, NOT 2.7). This is a dependency that is required for the program to work and allows us to install pics2word with pip. (Pip is a recursive acronym for pip installs packages)

2. When that is installed, open the command line (or PowerShell) and then type:

    `$ pip install pics2word`

    This installs the latest version of pics2word onto the system.

    From the latest Windows 10 update, the PowerShell can be opened from windows file explorer > File > Open Windows PowerShell
    From Linux you may need root privillages. If the above does not work, try

    `$ sudo pip install pics2word --user`

3. You can now run “pics2word” from the command line anywhere. Type:

    `$ pics2word –h help`

    for information on how to use it.

Note: pics2word can be updated to the latest release with:

`$ pip install --upgrade pics2word`

note the two dashes before upgrade.

Useful supplementary third party software:

- [Caesium](https://saerasoft.com/caesium/) – image compression software. Useful if dealing with a large number of pictures to reduce the file size of the word document and speed up image processing.
- [Bulk Rename Utility](http://www.bulkrenameutility.co.uk/Download.php) – allows large numbers of files to be renamed automatically. Especially useful if following a format such as “Photo 1, Photo 2... Photo X”

## New to this release 0.9.2

- Picture files are now sorted more intellegently by picking integers from strings then ordering by number.

## TODO tasks

### High Priority

#### Features

- Add help features
- Save & load modules from a standard, cross-platform file location.

#### Bug fix's

- Fix "Path" as this is not taking pictures from other folders as it should!

### Low Priority

#### Features

- Use Docopt module to make arg parsing simpler and to a more modern standard??

- Allow the user to omit the picture name??

#### Bug fix's
