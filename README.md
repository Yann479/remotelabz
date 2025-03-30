The "rector.php" script can be used to automate the modification of annotations in Entity, to attributes compatible with PHP 8.x

To use this script, install rector via the command :
`composer require rector/rector:^0.16 --dev`

Create a file named “rector.php” at the root of the project, and insert the code.

Create the file “phpstan.php” at the root of the project, with the following content:
```
parameters:
  level: 5
  paths:
    - src
```

Then run the following 2 commands, the first to check for changes and potential errors, and the second to make the changes.
```
vendor/bin/rector process src/Entity --dry-run
vendor/bin/rector process src/Entity/
```

The "script_modif_annotation.py" script allows you to :
- Convert @IsGranted and @Security annotations to PHP 8.x attributes.
- Modifies @Rest annotations into PHP 8.x attributes.
- Removes unnecessary annotation blocks that lead to errors/deprecations (when the following functions are in comments)

To use it, create a python file at the root of the project, add the code and run the following command:
`python3 script.py`
