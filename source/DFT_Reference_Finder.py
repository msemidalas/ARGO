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

import os
import re
import glob
from collections import defaultdict
import argparse

def extract_dft_functionals_from_file(filepath):
    """
    Extract DFT functional and quantum chemistry method references from a Gaussian output file.
    
    Args:
        filepath (str): Path to the Gaussian output file
        
    Returns:
        dict: Dictionary containing found methods and their line numbers
    """
    methods = defaultdict(list)
    
    # Comprehensive DFT functionals and quantum chemistry methods patterns
    # Organized by type for better understanding
    dft_patterns = {
        # === DFT Functionals ===
        # Hybrid functionals
        'B3LYP': r'(?:^|\s|#)B3LYP(?:\s|/|$)',
        'PBE0': r'(?:^|\s|#)PBE0(?:\s|/|$)',
        'M06-2X': r'(?:^|\s|#)M06-?2X(?:\s|/|$)',
        'HSE06': r'(?:^|\s|#)HSE06(?:\s|/|$)',
        'CAM-B3LYP': r'(?:^|\s|#)CAM-?B3LYP(?:\s|/|$)',
        'wB97X-D': r'(?:^|\s|#)wB97X-?D(?:\s|/|$)',
        'wB97X': r'(?:^|\s|#)wB97X(?:\s|/|$)',
        'B3PW91': r'(?:^|\s|#)B3PW91(?:\s|/|$)',
        'B3P86': r'(?:^|\s|#)B3P86(?:\s|/|$)',
        'X3LYP': r'(?:^|\s|#)X3LYP(?:\s|/|$)',
        'BMK': r'(?:^|\s|#)BMK(?:\s|/|$)',
        'TPSSh': r'(?:^|\s|#)TPSSh(?:\s|/|$)',
        'LC-wPBE': r'(?:^|\s|#)LC-?wPBE(?:\s|/|$)',
        
        # Pure DFT functionals
        'PBE': r'(?:^|\s|#)PBE(?:\s|/|$)(?!0)',
        'BLYP': r'(?:^|\s|#)BLYP(?:\s|/|$)',
        'BP86': r'(?:^|\s|#)BP86(?:\s|/|$)',
        'TPSS': r'(?:^|\s|#)TPSS(?:\s|/|$)(?!h)',
        'revPBE': r'(?:^|\s|#)revPBE(?:\s|/|$)',
        'OLYP': r'(?:^|\s|#)OLYP(?:\s|/|$)',
        'B97D': r'(?:^|\s|#)B97-?D(?:\s|/|$)',
        
        # Meta-GGA functionals
        'M06': r'(?:^|\s|#)M06(?:\s|/|$)(?!-)',
        'M06-L': r'(?:^|\s|#)M06-?L(?:\s|/|$)',
        'M06-HF': r'(?:^|\s|#)M06-?HF(?:\s|/|$)',
        'M11': r'(?:^|\s|#)M11(?:\s|/|$)(?!-)',
        'M11-L': r'(?:^|\s|#)M11-?L(?:\s|/|$)',
        'MN15': r'(?:^|\s|#)MN15(?:\s|/|$)(?!-)',
        'MN15-L': r'(?:^|\s|#)MN15-?L(?:\s|/|$)',
        'MN12-L': r'(?:^|\s|#)MN12-?L(?:\s|/|$)',
        'MN12-SX': r'(?:^|\s|#)MN12-?SX(?:\s|/|$)',
        'SCAN': r'(?:^|\s|#)SCAN(?:\s|/|$)(?![a-z])',  # SCAN functional, not "scan" operations
        'N12': r'(?:^|\s|#)N12(?:\s|/|$)(?!-)',
        'N12-SX': r'(?:^|\s|#)N12-?SX(?:\s|/|$)',
        'SOGGA11': r'(?:^|\s|#)SOGGA11(?:\s|/|$)(?!-)',
        'SOGGA11-X': r'(?:^|\s|#)SOGGA11-?X(?:\s|/|$)',
        
        # Range-separated functionals
        'wb97': r'(?:^|\s|#)wb97(?:\s|/|$)(?![xd])',
        'wb97x': r'(?:^|\s|#)wb97x(?:\s|/|$)(?!d)',
        'wb97xd': r'(?:^|\s|#)wb97xd(?:\s|/|$)',
        
        # === Wave Function Methods ===
        'HF': r'(?:^|\s|#)HF(?:\s|/|$)',
        'RHF': r'\bRHF\b',
        'UHF': r'\bUHF\b',
        'ROHF': r'\bROHF\b',
        
        # Post-HF methods
        'MP2': r'\bMP2\b',
        'MP3': r'\bMP3\b',
        'MP4': r'\bMP4\b',
        'CCSD': r'\bCCSD\b(?!\()',
        'CCSD(T)': r'\bCCSD\(T\)\b',
        'QCISD': r'\bQCISD\b(?!\()',
        'QCISD(T)': r'\bQCISD\(T\)\b',
        'CIS': r'\bCIS\b',
        'CISD': r'\bCISD\b',
        
        # Composite methods
        'G1': r'\bG1\b',
        'G2': r'\bG2\b',
        'G3': r'\bG3\b',
        'G4': r'\bG4\b',
        'CBS': r'\bCBS\b',
        'W1': r'\bW1\b',
        
        # === Special References ===
        'Harris functional': r'Harris functional',
        'DFT': r'\bDFT\b',
        'Slater exchange': r'Slater',
        'VWN correlation': r'\bVWN\b',
        'LYP correlation': r'\bLYP\b(?![A-Z])',  # LYP but not part of B3LYP, etc.
        'Becke exchange': r'\bBecke\b',
        'Perdew exchange': r'\bPerdew\b',
    }
    
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} does not exist")
        return methods
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Skip lines that are clearly scan parameters or other non-method contexts
            if any(skip in line.lower() for skip in ['scan                                      !', 
                                                     'scan 18   10.',
                                                     'number of optimizations in scan',
                                                     'optimization in scan']):
                continue
                
            for method_name, pattern in dft_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    methods[method_name].append({
                        'line_number': line_num,
                        'line_content': line.strip(),
                        'file': filepath
                    })
                    
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        
    return methods

def find_all_dft_references(directory_path='.', file_patterns=['*.log', '*.out', '*.com', '*.gjf']):
    """
    Find all DFT functional references in Gaussian files within a directory.
    
    Args:
        directory_path (str): Directory to search
        file_patterns (list): List of file patterns to search
        
    Returns:
        dict: Dictionary containing all found methods across all files
    """
    all_methods = defaultdict(list)
    processed_files = []
    
    for pattern in file_patterns:
        search_pattern = os.path.join(directory_path, '**', pattern)
        files = glob.glob(search_pattern, recursive=True)
        
        for filepath in files:
            if filepath not in processed_files:
                processed_files.append(filepath)
                print(f"Processing: {filepath}")
                file_methods = extract_dft_functionals_from_file(filepath)
                
                for method, occurrences in file_methods.items():
                    all_methods[method].extend(occurrences)
    
    return all_methods, processed_files

def generate_reference_report(all_methods, output_file='DFT_Functional_References.txt'):
    """
    Generate a comprehensive report of all DFT functional references found.
    
    Args:
        all_methods (dict): Dictionary of found methods
        output_file (str): Output file name for the report
    """
    with open(output_file, 'w') as f:
        f.write("ARGO - DFT Functional and Quantum Chemistry Method References\n")
        f.write("=" * 65 + "\n\n")
        f.write("This report contains all DFT functionals and quantum chemistry methods\n")
        f.write("referenced in the analyzed Gaussian output files.\n\n")
        
        if not all_methods:
            f.write("No DFT functionals or quantum chemistry methods found.\n")
            return
        
        # Summary section
        f.write("SUMMARY\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total unique methods found: {len(all_methods)}\n")
        total_occurrences = sum(len(occurrences) for occurrences in all_methods.values())
        f.write(f"Total occurrences: {total_occurrences}\n\n")
        
        # Organize methods by category
        hybrid_dft = []
        pure_dft = []
        metagga = []
        wavefunction = []
        post_hf = []
        composite = []
        other = []
        
        for method in sorted(all_methods.keys()):
            if method in ['B3LYP', 'PBE0', 'M06-2X', 'HSE06', 'CAM-B3LYP', 'wB97X-D', 'wB97X', 'B3PW91', 'B3P86', 'X3LYP', 'BMK', 'TPSSh', 'LC-wPBE']:
                hybrid_dft.append(method)
            elif method in ['PBE', 'BLYP', 'BP86', 'TPSS', 'revPBE', 'OLYP', 'B97D', 'wb97', 'wb97x', 'wb97xd']:
                pure_dft.append(method)
            elif method in ['M06', 'M06-L', 'M06-HF', 'M11', 'M11-L', 'MN15', 'MN15-L', 'MN12-L', 'MN12-SX', 'SCAN', 'N12', 'N12-SX', 'SOGGA11', 'SOGGA11-X']:
                metagga.append(method)
            elif method in ['HF', 'RHF', 'UHF', 'ROHF']:
                wavefunction.append(method)
            elif method in ['MP2', 'MP3', 'MP4', 'CCSD', 'CCSD(T)', 'QCISD', 'QCISD(T)', 'CIS', 'CISD']:
                post_hf.append(method)
            elif method in ['G1', 'G2', 'G3', 'G4', 'CBS', 'W1']:
                composite.append(method)
            else:
                other.append(method)
        
        # Methods by category
        f.write("METHODS BY CATEGORY\n")
        f.write("-" * 30 + "\n")
        if hybrid_dft:
            f.write("Hybrid DFT Functionals:\n")
            for method in hybrid_dft:
                f.write(f"  • {method}\n")
            f.write("\n")
        if pure_dft:
            f.write("Pure DFT Functionals:\n")
            for method in pure_dft:
                f.write(f"  • {method}\n")
            f.write("\n")
        if metagga:
            f.write("Meta-GGA Functionals:\n")
            for method in metagga:
                f.write(f"  • {method}\n")
            f.write("\n")
        if wavefunction:
            f.write("Hartree-Fock Methods:\n")
            for method in wavefunction:
                f.write(f"  • {method}\n")
            f.write("\n")
        if post_hf:
            f.write("Post-Hartree-Fock Methods:\n")
            for method in post_hf:
                f.write(f"  • {method}\n")
            f.write("\n")
        if composite:
            f.write("Composite Methods:\n")
            for method in composite:
                f.write(f"  • {method}\n")
            f.write("\n")
        if other:
            f.write("Other Methods/References:\n")
            for method in other:
                f.write(f"  • {method}\n")
            f.write("\n")
        
        # Detailed section
        f.write("DETAILED REFERENCES\n")
        f.write("-" * 30 + "\n")
        
        for method in sorted(all_methods.keys()):
            occurrences = all_methods[method]
            f.write(f"\n{method} ({len(occurrences)} occurrence{'s' if len(occurrences) != 1 else ''})\n")
            f.write("-" * (len(method) + 20) + "\n")
            
            # Group by file
            files = defaultdict(list)
            for occurrence in occurrences:
                files[occurrence['file']].append(occurrence)
            
            for filepath in sorted(files.keys()):
                f.write(f"  File: {filepath}\n")
                for occurrence in files[filepath][:10]:  # Limit to first 10 per file to avoid huge output
                    f.write(f"    Line {occurrence['line_number']}: {occurrence['line_content']}\n")
                if len(files[filepath]) > 10:
                    f.write(f"    ... and {len(files[filepath]) - 10} more occurrences\n")
                f.write("\n")

def main():
    """Main function to execute the DFT functional reference finder."""
    parser = argparse.ArgumentParser(
        description='Find all DFT functional and quantum chemistry method references in Gaussian files'
    )
    parser.add_argument(
        '-d', '--directory', 
        default='.', 
        help='Directory to search (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output', 
        default='DFT_Functional_References.txt',
        help='Output file name (default: DFT_Functional_References.txt)'
    )
    parser.add_argument(
        '--file-patterns',
        nargs='*',
        default=['*.log', '*.out', '*.com', '*.gjf'],
        help='File patterns to search (default: *.log *.out *.com *.gjf)'
    )
    
    args = parser.parse_args()
    
    print("ARGO - DFT Functional Reference Finder")
    print("=" * 40)
    print(f"Searching directory: {args.directory}")
    print(f"File patterns: {', '.join(args.file_patterns)}")
    print(f"Output file: {args.output}")
    print("-" * 40)
    
    all_methods, processed_files = find_all_dft_references(args.directory, args.file_patterns)
    
    print(f"\nProcessed {len(processed_files)} files")
    print(f"Found {len(all_methods)} unique methods/functionals")
    
    generate_reference_report(all_methods, args.output)
    
    print(f"\nDetailed report saved to: {args.output}")
    
    # Display summary to console
    if all_methods:
        print("\nSUMMARY OF FOUND METHODS:")
        print("-" * 30)
        for method in sorted(all_methods.keys()):
            count = len(all_methods[method])
            print(f"• {method}: {count} occurrence{'s' if count != 1 else ''}")
    else:
        print("\nNo DFT functionals or quantum chemistry methods found.")

if __name__ == '__main__':
    main()