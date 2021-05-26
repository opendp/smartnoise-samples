# Setup Scripts for Testing

- Internal notes, e.g. very manual process to add to the CI.

# Steps to Test (very manual process)

1. Open the Terminal and invoke a virtualenv that has the packages in the `/requirements.txt` file installed
   ```
   cd testing`
   # Open `testing/nb_debug.py` for editing
   # Change the end of `nb_debug.py` to run the function `run_analysis_notebooks()`

   # Run the script
   python nb_debug.py
  
   ```
2. Output files will be written to:
   - `/analysis/output`
   - Extensions: `.ipynb`,
    `.ipynb.html`
7. Open the files ending in `.ipynb.html` and look for unexpected errors.
   - Many of these files DO have expected errors. 
   - View the `.ipynb` files on GitHub for context. 
     - For example, the [`basic_data_analysis.ipynb` notebook](/analysis/basic_data_analysis.ipynb) has expected errors when demonstrating how attempts failed when certain parameters are not set. 
8. Hint: within the [`run_analysis_notebooks`](/testing/nb_debug.py#L97) function, it can be helpful to run/check a single notebook at a time by commenting out all but one of the tuples in the `inputs`.


 
