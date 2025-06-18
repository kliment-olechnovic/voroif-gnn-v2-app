# About VoroIF-GNN-v2

VoroIF-GNN-v2 scores protein-protein interfaces, it is a new version of the [VoroIF-GNN](https://doi.org/10.1002/prot.26554) [1] method.
The core idea of VoroIF-GNN remained the same - to train and apply a graph attention-based graph neural network that predicts CAD-score-based local scores
for interface residue-residue contacts that can be summed into global, interface-level scores.
The unique aspect of the VoroIF-GNN approach is that it considers the graph of interface contacts and their adjacencies, not the graph of atoms or residues.

Compared to the first version of VoroIF-GNN, VoroIF-GNN-v2 uses new tessellation contact area-based pseudoenergy descriptors.
The new descriptors are based on the observed and expected probabilities of contacts to occur and persist in folded conformations.
The probabilities were derived from the contact areas calculated using [Voronota-LT](https://www.voronota.com/expansion_lt/) [2] for ensembles of structures collected from PDB.
VoroIF-GNN-v2 graph neural network models were trained using the same collection of diverse docking models as the first version of VoroIF-GNN.

VoroIF-GNN-v2 was used by group "Olechnovic" that participated in the CAPRI Round 57 scoring challenge
by running the VoroIF-jury (Voronoi tessellation-based InterFace jury) algorithm [3] that utilized VoroIF-GNN-v2 as the primary single-model scoring method.
According to the official CAPRI scoring challenge assessment presented in the CASP16 conference, the results of "Olechnovic" were [relatively good](https://bsky.app/profile/capridock.bsky.social/post/3lcdk2v7xhs2c).

Both VoroIF-GNN and VoroIF-GNN-v2 were developed by Kliment Olechnovic ([www.kliment.lt](https://www.kliment.lt)).

# Obtaining and setting up VoroIF-GNN-v2

## Getting the latest version

The currently recommended way to obtain VoroIF-GNN-v2 is cloning the VoroIF-GNN-v2 git repository [https://github.com/kliment-olechnovic/voroif-gnn-v2-app](https://github.com/kliment-olechnovic/voroif-gnn-v2-app):

```bash
git clone https://github.com/kliment-olechnovic/voroif-gnn-v2-app.git
cd ./voroif-gnn-v2-app
```

## Building the included software

VoroIF-GNN-v2 comes with a statically built 'voronota-js' binary for Linux.

The source code for 'voronota-js' is also included, and can be used to build 'voronota-js' with the following command: 

```bash
./build-voronota-js.bash
```

## Setting up an environment for running VoroIF-GNN-v2

VoroIF-GNN-v2 requires PyTorch, PyTorch Geometric, Pandas, and R.

Below is an example of setting up a suitable environment:

```bash
# install and activate Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/miniconda3/bin/activate

# import and activate provided environment
conda env create --file voroif-gnn-v2-env.yaml
conda activate voroif-gnn-v2-env

# if you do not have R installed in your system, install it (below is an example for Ubuntu)
sudo apt-get install r-base
```


# Running the VoroIF-GNN-v2 command-line tool

The overview of command-line options, as well as input and output, is printed when running the "voronota-js-voroif-gnn-v2" executable with "--help" or "-h" flags:

```bash
voronota-js-voroif-gnn-v2 --help

voronota-js-voroif-gnn-v2 -h
```

The following is the help message output:

```bash

'voronota-js-voroif-gnn-v2' scores protein-protein interfaces using the VoroIF-GNN-v2 method

Options:
    --gnn-bundle-dir          string     GNN bundle directory, default is the script directory
    --gnn-models-dir          string     directory with GNN models files, default is '${GNN_BUNDLE_DIR}/trained_gnn_models/set1'
    --conda-path              string     conda installation path, default is ''
    --conda-env               string     conda environment name, default is 'voroif-gnn-v2-env'
    --processors              number     suggested maximum number of processors to run in parallel, default is 1
    --stdin-file              string     input file path to replace stdin, default is '_stream'
    --as-assembly             string     flag to treat input files as biological assemblies
    --restrict-input          string     query to restrict input atoms, default is '[]'
    --run-faspr               string     path to FASPR data library to rebuild side-chains, default is ''
    --subselect-contacts      string     query to subselect inter-chain contacts, default is '[]'
    --output-table-file       string     output file path for the table of global scores, default is ''
    --output-dir              string     output directory path for all detailed results, default is ''
    --help | -h                          flag to display help message and exit

Standard input:
    list of input PDB files

Standard output:
    space-separated table of global scores
    
Important note about output interpretation:
    higher GNN scores are better, lower GNN scores are worse

Examples:

    find ./models/ -type f -name '*.pdb' | ./voronota-js-voroif-gnn-v2 --conda-path ~/miniconda3 > ./table.txt
    
    ./voronota-js-voroif-gnn-v2 --conda-path ~/miniconda3 --stdin-file ./list_of_input_paths.txt --output-table-file ./table.txt
    
```

# Output example

Running

```bash
find "./tests/input/" -type f -name '*.pdb' | ./voronota-js-voroif-gnn-v2 --conda-path ~/miniconda3 --conda-env "voroif-gnn-v2-env"
```

gives

```
ID          pgoodness         area          pgoodness_average  pcadscore          num_of_residues  residue_pcadscore
target.pdb  3950.86379466157  1052.6115266  3.7533921060347    0.989939100410307  55               0.962183314934303
model2.pdb  3278.5901377528   980.6629806   3.34323840362247   0.980264382968966  57               0.892452551708428
model1.pdb  3173.20794179111  982.909923    3.22838122552061   0.976199693464367  63               0.84179649837125
```

# References

1. Olechnovič, K., Venclovas, Č. VoroIF-GNN: Voronoi tessellation-derived protein-protein interface assessment using a graph neural network. Proteins 91(12):1879-1888 [doi:10.1002/prot.26554](https://doi.org/10.1002/prot.26554). (2023)
2. Olechnovič, K., Grudinin, S. Voronota-LT: efficient, flexible and solvent-aware tessellation-based analysis of atomic interactions. Preprint in bioRxiv [doi:10.1101/2024.02.05.577169](https://doi.org/10.1101/2024.02.05.577169). (2024)
3. Olechnovič, K., Banciul, R., Dapkūnas, J., Venclovas, Č. FTDMP: a framework for protein-protein, protein-DNA and protein-RNA docking and scoring. Proteins [doi:10.1002/prot.26792](https://doi.org/10.1002/prot.26792). (2025)

