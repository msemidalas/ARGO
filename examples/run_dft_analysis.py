#Argo, an open-source data analysis software for quantum chemical calculations
#Copyright (C) 2016-2023 Emmanouil Semidalas, Charis Semidalas.
#E-mail:msemidalas@yahoo.com, chsemid@teiath.gr

#Argo is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Argo; if not, see <https://www.gnu.org/licenses/>.

# This is a symlink/copy of the main DFT_Reference_Finder.py from the source directory
# Run this to find all DFT functional references in the example files

import sys
import os

# Add the source directory to the path so we can import the main module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))

try:
    from DFT_Reference_Finder import main
    
    print("Running DFT Reference Finder on example files...")
    print("=" * 50)
    
    # Override sys.argv to run on current directory with custom output
    original_argv = sys.argv.copy()
    sys.argv = ['DFT_Reference_Finder.py', '-d', '.', '-o', 'Example_DFT_References.txt']
    
    main()
    
    # Restore original argv
    sys.argv = original_argv
    
    print("\nExample analysis complete!")
    print("Check 'Example_DFT_References.txt' for results.")
    
except ImportError as e:
    print(f"Error importing DFT_Reference_Finder: {e}")
    print("Please make sure DFT_Reference_Finder.py is in the source directory.")