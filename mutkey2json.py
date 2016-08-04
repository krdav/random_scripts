import gzip
import json
import os
import sys
import copy
from shutil import copyfile


datafile = '/home/projects/cu_10020/ddg_constriants/constraint_single_mut_buried_min40X_max2A.tsv'
pdb_database_folder = '/home/projects/pr_46690/data/db/pdb/split'
pdb_dump_folder = '/home/projects/cu_10020/ddg_constriants/pdbs'


constraint_temp = dict()
constraint_temp["AggregateType"] = "SingleValue"
constraint_temp["DDG"] = 99999  # Placeholder add constraint value here
constraint_temp["DerivedMutation"] = False
constraint_temp["ExperimentalDDGs"] = list()
constraint_temp["ExperimentalDDGs"].append(dict())
constraint_temp["ExperimentalDDGs"][0]["DDG"] = 99999  # Placeholder add constraint value here
constraint_temp["ExperimentalDDGs"][0]["DDGType"] = 'constrain_score'
constraint_temp["ExperimentalDDGs"][0]["LocationOfValueInPublication"] = 'NA'
constraint_temp["ExperimentalDDGs"][0]["Publication"] = 'NA'
constraint_temp["ExperimentalDDGs"][0]["Temperature"] = 25
constraint_temp["ExperimentalDDGs"][0]["pH"] = 7
constraint_temp["Mutations"] = list()
constraint_temp["Mutations"].append(dict())
constraint_temp["Mutations"][0]["Chain"] = 'X' # Placeholder for chain ID
constraint_temp["Mutations"][0]["DSSPExposure"] = 0
constraint_temp["Mutations"][0]["DSSPSimpleSSType"] = 'H'
constraint_temp["Mutations"][0]["DSSPType"] = 'H'
constraint_temp["Mutations"][0]["MutantAA"] = 'X' # Placeholder for mutant amino acid type
constraint_temp["Mutations"][0]["Pfam domains"] = 'PF00000'
constraint_temp["Mutations"][0]["ResidueID"] = 0 # Placeholder for residue number
constraint_temp["Mutations"][0]["SCOP class"] = 'd.0.0.0'
constraint_temp["Mutations"][0]["WildTypeAA"] = 'X' # Placeholder for wild type amino acid type
constraint_temp["PDBFileID"] = 'XXXX' # Placeholder for PDB file
constraint_temp["RecordID"] = 999999999 # Placeholder for record ID
constraint_temp["_DataSetDDGID"] = 999999999 # Placeholder for record ID
constraint_temp["_ExperimentID"] = 999999999 # Placeholder for record ID

constraints = dict()
constraints["data"] = list()


def move_PDB_file(PDB_ID, chain_name):
    pdb_folder = pdb_database_folder.rstrip('/')
    # abs_path = pdb_database_folder + '/' + PDB_ID[1:3].lower()
    PDB_ID = PDB_ID.lower()
    pdb_path = '{}/{}/pdb{}.ent.gz'.format(pdb_folder, PDB_ID[1:3], PDB_ID)
    pdb_dump = pdb_dump_folder + '/' + PDB_ID.upper() + '.pdb.gz'
    
    # fnam_out = '{}/{}'.format(pair_folder, pdb_file)
    # fh_out = open(fnam_out, 'w')
    # Notice this is opened directly as gzipped and therefore comes in binary:
    AA_count = 0
    with gzip.open(pdb_path, 'r') as fh_in:
        lines = fh_in.readlines()
        for line in lines:
            # Decode from binary to unicode:
            line = str(line, 'utf-8')
            # Then only keep 'ATOM' cards or HETATM on the whitelist:
            if line[0:6] == 'ATOM  ' and line[21] == chain_name:
                AA_count += 1
                # print(line, file=fh_out, end='')
    #fh_out.close()
    if AA_count > 60:
        copyfile(pdb_path, pdb_dump)
    else:
        return(False)
    
    return(True)



short2long = {'P': 'position', 'ID': 'PDB_ID', 'C': 'chain', 'W': 'wild_type', 'M': 'mutant_type'}
with open(datafile) as fh_in:
    fh_in.readline()  # Skip header
    for idx, line in enumerate(fh_in):
        cols = line.split('\t')
        constr = cols[1]
        mut_key = cols[0].split('_')
        mut_key_dict = {short2long[el.split('=')[0]]: el.split('=')[1] for el in mut_key if el}
        PDB_ID = mut_key_dict['PDB_ID'].upper()
        chain_name = mut_key_dict['chain'].upper()
        if not move_PDB_file(PDB_ID, chain_name):
            continue

        constraint = copy.deepcopy(constraint_temp)
        constraint["DDG"] = constr
        constraint["ExperimentalDDGs"][0]["DDG"] = constr
        constraint["Mutations"][0]["Chain"] = chain_name
        constraint["Mutations"][0]["MutantAA"] = mut_key_dict['mutant_type']
        constraint["Mutations"][0]["ResidueID"] = mut_key_dict['position']
        constraint["Mutations"][0]["WildTypeAA"] = mut_key_dict['wild_type']
        constraint["PDBFileID"] = PDB_ID
        constraint["RecordID"] = idx
        constraint["_DataSetDDGID"] = idx
        constraint["_ExperimentID"] = idx

        constraints["data"].append(constraint)
        # print(mut_key_dict)


print(json.dumps(constraints, sort_keys=True, indent=4, separators=(',', ': ')))








