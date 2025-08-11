# DFT Functional Reference Finder

This tool automatically finds all DFT functionals and quantum chemistry method references in Gaussian output files within the ARGO repository.

## Overview

The DFT Reference Finder is a comprehensive tool that scans Gaussian log files (`.log`, `.out`, `.com`, `.gjf`) and identifies:

- **DFT Functionals**: B3LYP, PBE, M06, SCAN, etc.
- **Wave Function Methods**: HF, RHF, MP2, CCSD, etc.
- **Composite Methods**: G1, G2, G3, G4, CBS, etc.
- **Special References**: Harris functional, exchange-correlation components

## Found Methods in ARGO Repository

Based on analysis of the example files in this repository, the following quantum chemistry methods have been identified:

### Hartree-Fock Methods
- **HF**: Hartree-Fock method (3 occurrences)
- **RHF**: Restricted Hartree-Fock (2,396 occurrences)

### Meta-GGA Functionals  
- **SCAN**: Strongly Constrained and Appropriately Normed functional (1 occurrence)

### Other References
- **DFT**: General DFT references (1 occurrence)
- **Harris functional**: Used for initial SCF guess (1,370 occurrences)

**Total**: 5 unique methods with 3,771 total occurrences across 2 files.

## Usage

### Command Line Usage

```bash
# Run on current directory
python source/DFT_Reference_Finder.py

# Run on specific directory with custom output
python source/DFT_Reference_Finder.py -d /path/to/gaussian/files -o my_results.txt

# Run on specific file patterns
python source/DFT_Reference_Finder.py --file-patterns "*.log" "*.out"
```

### Example Analysis

To analyze just the example files:

```bash
cd examples
python run_dft_analysis.py
```

This will create `Example_DFT_References.txt` with method references found in the example files.

## Output Format

The tool generates a comprehensive report with:

1. **Summary**: Total methods and occurrences
2. **Methods by Category**: Organized by functional type
3. **Detailed References**: Line-by-line occurrences with context

### Example Output

```
ARGO - DFT Functional and Quantum Chemistry Method References
=================================================================

SUMMARY
------------------------------
Total unique methods found: 5
Total occurrences: 3771

METHODS BY CATEGORY
------------------------------
Meta-GGA Functionals:
  • SCAN

Hartree-Fock Methods:
  • HF
  • RHF

DETAILED REFERENCES
------------------------------

HF (3 occurrences)
----------------------
  File: ./examples/IR and Raman intensitites/ch3oh.log
    Line 85: #p HF/cc-pvdz Freq=Raman
```

## Supported Methods

The tool recognizes a comprehensive list of quantum chemistry methods:

### DFT Functionals
- **Hybrid**: B3LYP, PBE0, M06-2X, HSE06, CAM-B3LYP, wB97X-D, etc.
- **Pure**: PBE, BLYP, BP86, TPSS, revPBE, OLYP, etc.
- **Meta-GGA**: M06, M06-L, M11, MN15, SCAN, etc.
- **Range-Separated**: wb97, wb97x, wb97xd, LC-wPBE, etc.

### Wave Function Methods
- **HF variants**: HF, RHF, UHF, ROHF
- **Post-HF**: MP2, MP3, MP4, CCSD, CCSD(T), QCISD, etc.
- **CI methods**: CIS, CISD

### Composite Methods
- **Gaussian-n**: G1, G2, G3, G4
- **Other**: CBS, W1

## Files

- `source/DFT_Reference_Finder.py`: Main analysis script
- `examples/run_dft_analysis.py`: Example runner script  
- `DFT_References_Final.txt`: Complete analysis results
- `examples/Example_DFT_References.txt`: Example-only results

## Requirements

- Python 3.x
- Standard library modules: `os`, `re`, `glob`, `collections`, `argparse`

## Notes

- The tool is designed to avoid false positives (e.g., "scan" in geometry optimization vs "SCAN" functional)
- Large files may have thousands of method references due to iterative SCF cycles
- Harris functional references are common in Gaussian output as they're used for initial SCF guesses