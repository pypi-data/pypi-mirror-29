# mcgpyutils
mcgpyutils(MCG Python Utilities) is a project containing utility classes 
commonly used in Python projects at [MCG Strategic](https://www.mcgstrategic.com/).

## Requirements
  * Python3, version >= 3.6

## Usage
Example: 
```
from mcgpyutils import FileSystemUtils

fsu = FileSystemUtils()
print(fsu.get_path_to_script(__file__))
```
