# Copy Git Repo

## 1 - Context

This is a small convenience Python CLI package.  

If, like me, you
+ have your git repo is located inside a [GoogleDrive](https://www.google.com/intl/en_ALL/drive/) or a [Dropbox](https://www.dropbox.com/) on you computer
+ use npm/yarn frequently

then each `npm/yarn install` typically
+ downloads thousands of files
+ which triggers a massive sync operation
+ which sends your laptop fan spinning and battery nosediving..

To avoid that you need put your local repo outside the synced drives.  
There is not .googledriveignore or .dropboxignore - as far as I know.  
But it may convenient to keep just the source code synced.

This small package helps copy all folders and files not matched by the .gitignore file from one directory to another.  


## 2 - Installation

To install:
```bash
$ pip install copy_git_repo
```

## 3 - User Guide

To use it:

```bash
$ copy-repo --help
Usage: copy-repo [OPTIONS] <source> <destination>

  This script copies folder <source> which must be a git repo (i.e.
  containing a .gitignore file) to folder <destination>. Only those files
  not mentionned in .gitignore are copied.

  If <overwrite> is set the <destination> folder contents are overwritten.

Options:
  -ow, --overwrite  Overwrite dst folder if exists
  --help            Show this message and exit.
```

Example:

```bash
# Copy current directory to another location
# Only files not matched by .gitignore are copied
# .git folder not copied
$ copy-repo -ow . /Users/Olivier/Documents/dev/test-zone/copied-repo
source = /Users/Olivier/Documents/dev/my-repo
destination = /Users/Olivier/Documents/dev/test-zone/my-repo-copied
src is a git repo ? True
destination folder will be created
make copy
done

# Overwrite
$ copy-repo -ow . /Users/Olivier/Documents/dev/test-zone/copied-repo
source = /Users/Olivier/Documents/dev/my-repo
destination = /Users/Olivier/Documents/dev/test-zone/my-repo-copied
src is a git repo ? True
destination folder exists
overwrite ? [y/N]: y
make copy
done

# Include .git folder
$ copy-repo -g . /Users/Olivier/Documents/dev/test-zone/copied-repo
source = /Users/Olivier/Documents/dev/my-repo
destination = /Users/Olivier/Documents/dev/test-zone/my-repo-copied
src is a git repo ? True
destination folder will be created
make copy
done
```

## 4 - Credits

The [Click](http://click.pocoo.org/6/) Python package to create CLI interfaces is really flexible and convenient.  
Highly recommended !

