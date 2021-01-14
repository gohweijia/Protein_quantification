# Protein quantification
Quantifies BCA protein quantification assay results (.xlsx file) from Tecan Infinite M200


## Installation (MacOS)
```bash
#  Install MiniConda
bash Miniconda3-latest-MacOSX-x86_64.sh

#  Navigate to folder
cd Protein_quantification
pip install -r requirements.txt
```

## Usage
Copy .xlsx file to folder
```bash
python3 BSA.py
```
Enter name of file upon prompting
```python
Enter file name (excluding '.xlsx'): test
```
Change concentrations of standards if required
```python
The default concentration values are [0, 20, 40, 60, 80, 100, 150, 200].
To use a new set of values, enter space-separated concentration values. Otherwise, press enter.
```
Results will be saved in the folder labelled by date
```bash
Protein_quantification % ls
14Jan21_BSA		README.md		test.xlsx
BSA.py			requirements.txt

Protein_quantification % ls 14Jan21_BSA 
14Jan21_BSA.csv	plot.png
```

## License
[MIT](https://choosealicense.com/licenses/mit/)