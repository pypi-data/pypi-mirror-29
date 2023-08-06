README v3.0 / 14 MARCH 2018

Logo: ![Alt](MyProject/2.png "Team Logo")

### QSPR MODELING: APPLICATION OF MACHINE LEARNING ALOGRITHMS IN CLASSIFYING THE FAMILY AND PREDICTING FLASH POINTS AND CETANE NUMBER OF BIOFUEL COMPOUNDS

### Introduction

This Biofuel Software will predict the family of the input chemicals and predict thermo-physical properties (flashing point and cetane number) according to the family. The GUI is designed by using tkinter. Numerical regression and classification methods, including MLPR, GRNN, OLS, PLS, KNN, SVM, LDA, were used in the machine learning approach to make better predictions of family and properties.

### Usage

To predict the family and the thermo-physical properties  of the imported molecule, user can run the software following the instructions below.
1. Git clone our GitHub address `git clone https://github.com/Zhangjt9317/Biofuel-Group-Project.git`;
2. Then, users input `cd Biofuel-Group-Project/MyProject` command into bash;
3. Next, users input `python Project_GUI.py` command to open the Graphic User Interface;
4. Enter the `CID number` of that chemical and click `Get CID` to comfirm input. if `Get CID` is not clicked, no CID will be gotten for the machine learning models;
5. Click `Model selection` to chose differient machine learning methods and properties, and then click `Begin` to confirm selection;
6. Then click `Result` to plot the training and predction result.

Or users can run the demo jupyter notebook in sequence.

### Contribution

- Issue Tracker: https://github.com/Zhangjt9317/Biofuel-Group-Project/issues
- Source Code: https://github.com/Zhangjt9317/Biofuel-Group-Project

### Requirements

Our code could only run in the PC mode because some of the packages are only available on a PC interface. Please check package availability before running the code.

### Installation

This program runs on python. User must have the following packages installed in local environment.

Packages used in this program include:
Openbabel, Neupy, Numpy, Matplotlib, Pandas, Pubchempy, Sklearn, tkinter, xlrd. The address of several packages are as following. 

* [NeuPy](http://neupy.com/docs/tutorials.html#): Neural Networks package in Python.
* [Open Babel](http://openbabel.org/wiki/Main_Page): Search, convert, analyze, or store data from molecular modeling.
* [PubChemPy](https://pubchempy.readthedocs.io/en/latest/): Enable chemical searches by CID, name, substructure and conversion between different chemical file formats.
* [PyBEL](http://pybel.readthedocs.io/en/latest/): Enables the expression of complex molecular relationships and their context in a machine-readable form
* [Tkinter](https://docs.python.org/2/library/tkinter.html): Standard Python interface to the Tk GUI toolkit
* [XLRD](https://pypi.python.org/pypi/xlrd): Extract data from Excel spreadsheets

### One example

Please see the example for our software on the Demo.ipynb in the example folder.

### Credits

Jingtian Zhang, Cheng Zeng, Renlong Zheng, Chenggang Xi

### Contact

If you are having issues, please contact Cheng Zeng and Jingtian Zhang by [zengcheng95 --At-- gmail.com](mailto:zengcheng95@gmail.com), [jtz9317 --At-- gmail.com](mailto:jtz9317@gmail.com).

### License

The project is licensed under the MIT license.
