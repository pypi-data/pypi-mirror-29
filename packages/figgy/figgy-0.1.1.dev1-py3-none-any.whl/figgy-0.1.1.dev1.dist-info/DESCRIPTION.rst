# figgy

Are you sick and tired of writing packages or apps that are super great but don't work unless your end-user scours your README for instructions on how to structure config files and how and where to instantiate them? 

figgy is the app and package configuration generator package developed for developers who develop apps and/or packages for use by other developers.

figgy allows you to ship code and have the end-user developer install and configure it just by running your app or package. You can call it from setup.py or bind it to whatever you like in your code so the results of the new configuration are made immediately available to whatever context the app or package will be used in.

---

## Warning

This software is in alpha development. This should work, please report bugs. 

Key caveats:
* Outputs your configuration data to the screen in some cases.
* Only supports json
* Only available for python.
* You want this module to prompt from TTY.
* You're on a 'NIX system.
* You're okay figuring out how to make forcing a configuration regeneration for the user on your own.

These are intended to guide feature development for future versions, but in this state it should be useful nonetheless.

## Installation

    pip install git+git://github.com/dyspop/figgy

## Usage

To prompt and generate a configuration but not load it into the package/app context use:

    import figgy

    template = {
        'username': 'default',
        'password': 'anotherdefault'
    }

    figgy.make(template)

To prompt and generate a configuration then load the new configuration data into the package/app context use:

    config = figgy.make(template, get=True)

and the end user will be prompted with:

    Enter value for "username"
    (return for default "default")': ▋userinput
    Enter value for "username"
    (return for default "default")': 
    Set "username" to "userinput" in ./config.json
    Enter value for "password"
    (return for default "anotherdefault")': ▋anotheruserinput
    Enter value for "password"
    (return for default "anotherdefault")': 
    Set "password" to "anotheruserinput" in ./config.json

and generate a `config.json` file:

    {"username": "userinput", "password": "anotheruserinput"}

By default figgy assumes a few things:

* You want the file to be named `config.json`
* You want the file generated at the path the python code that executes it runs from
* You don't want to return the configuration data itself to the application context
* The user interface is TTY. 

But you can change most of that:


```
template = {
    'PORT': '3000',
    'DEBUG': 'True'
}
figgy.make(data=template, filename='appconfig')
Enter value for "PORT"
(return for default "3000")': ▋8080
Set "PORT" to "8080" in ./appconfig.json
Enter value for "DEBUG"
(return for default "True")': ▋False
Set "DEBUG" to "False" in ./appconfig.json
```
```
figgy.make(data=template, path='../configs/')
Enter value for "username"
(return for default "default")': ▋userinput
Enter value for "username"
(return for default "default")': 
Set "username" to "userinput" in ../configs/config.json
Enter value for "password"
(return for default "anotherdefault")': ▋anotheruserinput
Enter value for "password"
(return for default "anotherdefault")': 
Set "password" to "anotheruserinput" in ../configs/config.json
```
```
figgy.make(data=template, get=True)
Enter value for "username"
(return for default "default")': ▋userinput
Enter value for "username"
(return for default "default")': 
Set "username" to "userinput" in ./config.json
Enter value for "password"
(return for default "anotherdefault")': ▋anotheruserinput
Enter value for "password"
(return for default "anotherdefault")': 
Set "password" to "anotheruserinput" in ./config.json
{'./config.json': {'username': 'userinput', password: 'otheruserinput'}}
```

## Contributing

1. Fork the source repository https://github.com/dyspop/figgy 
2. Make a new branch
3. Write the feature code
4. Make sure you add some tests
5. Submit a pull request with helpful notes about your feature and test


