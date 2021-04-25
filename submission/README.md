# FBB-Pride

We are the participants of the PH Bio Hackathon 2021
We are the students of the Lomonosov Moscow State University, Faculty of Bioengineering and Bioinformatics.

Our team's objective was to create a model to predict protein solubility.

A picture below represents the major steps of our solution.
![solution](https://user-images.githubusercontent.com/38766545/115983806-2fcf3a00-a5ac-11eb-8189-e5668ba0ba4b.png)

First, we have performed the preprocessing of PDB files: removing HETATOM, re-numerating residue ids, calculating DSSP and SASA, and finding the amino acids that are exposed to the surface.

**We used several characteristics as the features for our model**:

### Standard characteristics of proteins

 - protein length and weight
 - instability index and isoelectric point of protein
 - secondary structure fractions (helix, turn, sheet)
 - molar extinction coefficient
 - charge at pH 7 and flexibility
 - % of each amino acid type in protein

### Our additional characteristics 

 - percentage of exposed hydrophobic atoms of amino acid side chains
 - number of clusters with the exposed amino acids
 - cluster volume
 - average cluster kD
 - number of TM helices (by Phobios)

## Selecting the amino acids exposed to the protein surface

We have selected amino acids that are located on the surfaces of the protein based on exposure evaluation. We have obtained these values ​​from the DSSP, calculated by a third-party program called mkDSSP, using the Prody method. Each of the residues selected was characterised by using kD scale and the number of exposed hydrophobic atoms. This number was then used as node weights.
We have also calculated the solvent accessible area for all the atoms of the exposed residues using a FreeSASA library, and then selected only the atoms with a value greater than the threshold.

## Clusters 

Using the residue hydrophobic characteristic, we have merged the amino acids that are located next to each other to form the hydrophobic clusters.
For top-4 such clusters we have estimated their mean volume of side chain AA residues and mean kD, which were lately used as features.

## Graph

Graph vertices have been connected to each other based on the measured distance between the nearest atoms of such amino acids. The distance has been calculated from three-dimensional PDB coordinates. After this step we have also calculated the graph kernels and used them as graph vector embeddings.

## Model

 We had 3 types of features: 
 * standard
 * custom tabular 
 * custom graph embeddings.

We have constructed three types of graphs, where each one encodes one distinct feature about nodes(exposed amino acids) - kd, hydrophobicity and amino acid name. Each graph was then transformed into the graph embeddings (vector representation) using the best fitting graph kernel (we’ve tried about five different kernel types). Based on each graph type we trained models (select best for each graph type) and made predictions. Each prediction of such base models was then used as a feature. 
We concatenate these predictions with hydrophobic clusters parameters and our other tabular features to create big feature tables which then were used to train meta-model. 
Overall, the final model random forest has been trained and gave a final prediction of solubility. 
We have extracted a tree from the random forest ensemble and looked at its decision rules.
The root-closest rule represents the number of the surface-exposed residues that were predicted to be able to form hydrogen bonds.
The mean kD of selected hydrophobic clusters was also rather important for the final model model.
