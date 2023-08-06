# repo\_state #

This repository defines two command line tools:  
```
$ save_repo_state
$ enforce_repo_state
```

These tools are intended to capture the state of multiple git repositories and save that state to a file, and then later enforce the state specified in the file onto a set of git repos. 

## Install ##

OSX and Posix only. Does not support Windows. 

```
$ pip install repo_state
```

## Usage ##

Each tool supports the -h and --help flags. 

```
$ save_repo_state --help

$ enforce_repo_state --help
```

## License ##

See LICENSE.txt


## Who do I talk to? ##

Jeff Gable  jeff@promenadesoftware.com
