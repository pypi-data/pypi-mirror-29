# list_all_envs
A tool for printing a list of enviornments and their packages

It is possible to produce a list of enviornments in Python by 
```Python
conda env list
```
however finding which packages are available within the enviornment can only be discovered once the user activates the enviornment by
```Python
conda list
```

This command is useful as it prints the list of the all Python enviornments and thier packages without having to individual activate all of them.
