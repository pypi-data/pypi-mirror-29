# Asset Engine



[![License](https://www.gnu.org/graphics/gplv3-88x31.png)](https://gitlab.com/lvxejay/materialx-blender/LICENSE.md)


### Repository:

The Asset Engine repository consists of the following packages:

    asset_engine        - Asset Engine Package
        bsetup          - Blender Setup Modules
        pipe            - Core Pipeline Context System
        utils           - Utilities





### Usage:
1) Install the library to system python using `pip install bpy_asset_engine`

2) Install the library to Blender using the following commands:
    test
    
    ````
    cd ~/<path/to/blender>/2.79/python/bin
    ./python3.5m -m pip install bpy_asset_engine
    
    # Note: Requires pip to be installed in blender for this to work. 
    ````
3) Import this library with `import asset_engine`



### Test Case:
```python
    
"""
Test: Pipe Context Path Resolution

    This test suite evaluates the sanity of the pipeline logic required for parsing
    formulas and turning them into paths on disk.
    There are 3 Tests.
    
    1) Single Path 
    Find a 'pr_base_dir' path given a set of keyword arguments to establish context.
        
        - Evaluates 1 Path
        - Establishes Context with kwargs
    
    2) Child Paths
    Find an 'as_base_dir' path given a positional argument parent_formula ('p'), 
    and a set of keyword arguments to establish context.
    
        - Evaluates Parent Path to establish context
        - Evaluates Child Path within updated context
        
    3) Multiple Paths
    Find 'pipe_sbs_dir' and 'pr_as_dir' (a list of formulas), given a set of keyword -
    arguments to establish context.
        
        - Evaluates each path, while subsequently updating a shared context pointer.
"""

def test():
    from asset_engine.utils.io import IO
    
    from asset_engine.pipe.pipe_core import pipe_context as PC
    pipe_base_dir = '/home/lvxejay/pipeline'
    
    IO.info("|----- Executing Test Suite -----|")
    
    #region Test 1: Single Path
    IO.info("Starting Tests")
    IO.debug("Base Directory: %s" % pipe_base_dir)
    IO.info("| Runtime: Single Path {INIT} |")
    
    # Get a path from PipeContext
    path = PC.get_path(
            'pr_base_dir',
            drive=pipe_base_dir, project='avengers', 
            asset_type='alien', asset="nova_prime_soldier.blend"
            )
    
    IO.debug("Found Path: %s" % path)
    IO.info("| Runtime: Single Path {END} |")
    #endregion
    
    #region Test 2: Child Path
    IO.info("| Runtime: Child Path {INIT} |")
    
    # Get a path from PipeContext
    path = PC.get_path(
            'as_base_dir', 'pr_as_type_dir', 
            drive=pipe_base_dir, project='project_2', 
            asset_type='architecture', asset="building.blend"
            )
    
    IO.debug("Found Path: %s" % path)
    IO.info("| Runtime: Child Path {END} |")
    #endregion

    #region Test 3: Multi Paths
    IO.info("| Runtime: Multi Paths {INIT} |")
    
    # Get a path from PipeContext
    path_list = ['pipe_sbs_dir', 'pr_as_dir']
    path = PC.get_path(
            path_list,
            drive=pipe_base_dir, project='project_3', 
            asset_type='heroes', asset="hercules.blend"
            )
    
    IO.debug([x for x in path])
    IO.info("| Runtime: Multi Paths {END} |")
    #endregion
    
    IO.info("|----- Closing Test Suite -----|")
    
if __name__ == '__main__':
    test()
    
```
    
            
            
            


### External Documentation
    WIP
---
