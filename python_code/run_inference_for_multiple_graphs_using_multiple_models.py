import sys
import pandas
import torch
import torch_geometric
import numpy

from custom_gnn_va import CustomGNNvA

def read_list_of_strings(list_file):
	strings=[]
	with open(list_file) as file:
		strings=[line.rstrip() for line in file]
	return strings

def read_list_of_numbers(list_file):
	with open(list_file) as file:
		return list(map(float, file.read().strip().split()))

def read_graph(files_prefix):
	nodes_file=files_prefix+"nodes.csv"
	links_file=files_prefix+"links.csv"
	data_frame_nodes=pandas.read_csv(nodes_file)
	data_frame_links=pandas.read_csv(links_file)
	x=torch.tensor(data_frame_nodes[['area', 'adjacency', 'boundary', 'VE', 'VESSa', 'VESSb', 'MVE', 'MVESSa', 'MVESSb', 'AKBP_kbp1_obs_pdb_aa', 'AKBP_kbp1_exp_pdb_aa', 'AKBP_kbp1_pdb_aa', 'AKBP_kbp2_obs_pdb_aa', 'AKBP_kbp2_exp_pdb_aa', 'AKBP_kbp2_pdb_aa', 'AKBP_kbp1_obs_pdb_rr', 'AKBP_kbp1_exp_pdb_rr', 'AKBP_kbp1_pdb_rr', 'AKBP_kbp2_obs_pdb_rr', 'AKBP_kbp2_exp_pdb_rr', 'AKBP_kbp2_pdb_rr', 'AKBP_kbp2_obs_pdb_rrfaa', 'AKBP_kbp2_exp_pdb_rrfaa', 'AKBP_kbp2_pdb_rrfaa', 'AKBP_kbp1_obs_idp_rr', 'AKBP_kbp1_exp_idp_rr', 'AKBP_kbp1_idp_rr', 'AKBP_kbp2_obs_idp_rr', 'AKBP_kbp2_exp_idp_rr', 'AKBP_kbp2_idp_rr', 'AKBP_kbp1_obs_revoromqa_aa', 'AKBP_kbp1_exp_revoromqa_aa', 'AKBP_kbp1_revoromqa_aa', 'AKBP_kbp1_obs_pdb_aa_solvated', 'AKBP_kbp1_exp_pdb_aa_solvated', 'AKBP_kbp1_pdb_aa_solvated', 'AKBP_kbp2_obs_pdb_aa_solvated', 'AKBP_kbp2_exp_pdb_aa_solvated', 'AKBP_kbp2_pdb_aa_solvated', 'AKBP_kbp1_obs_pdb_rr_solvated', 'AKBP_kbp1_exp_pdb_rr_solvated', 'AKBP_kbp1_pdb_rr_solvated', 'AKBP_kbp2_obs_pdb_rr_solvated', 'AKBP_kbp2_exp_pdb_rr_solvated', 'AKBP_kbp2_pdb_rr_solvated', 'AKBP_kbp2_obs_pdb_rrfaa_solvated', 'AKBP_kbp2_exp_pdb_rrfaa_solvated', 'AKBP_kbp2_pdb_rrfaa_solvated', 'AKBP_kbp1_obs_idp_rr_solvated', 'AKBP_kbp1_exp_idp_rr_solvated', 'AKBP_kbp1_idp_rr_solvated', 'AKBP_kbp2_obs_idp_rr_solvated', 'AKBP_kbp2_exp_idp_rr_solvated', 'AKBP_kbp2_idp_rr_solvated', 'AKBP_kbp1_obs_revoromqa_aa_solvated', 'AKBP_kbp1_exp_revoromqa_aa_solvated', 'AKBP_kbp1_revoromqa_aa_solvated', 'adjacency_coeff', 'boundary_coeff', 'VE_coeff', 'VESSa_coeff', 'VESSb_coeff', 'MVE_coeff', 'MVESSa_coeff', 'MVESSb_coeff', 'AKBP_kbp1_obs_pdb_aa_coeff', 'AKBP_kbp1_exp_pdb_aa_coeff', 'AKBP_kbp1_pdb_aa_coeff', 'AKBP_kbp2_obs_pdb_aa_coeff', 'AKBP_kbp2_exp_pdb_aa_coeff', 'AKBP_kbp2_pdb_aa_coeff', 'AKBP_kbp1_obs_pdb_rr_coeff', 'AKBP_kbp1_exp_pdb_rr_coeff', 'AKBP_kbp1_pdb_rr_coeff', 'AKBP_kbp2_obs_pdb_rr_coeff', 'AKBP_kbp2_exp_pdb_rr_coeff', 'AKBP_kbp2_pdb_rr_coeff', 'AKBP_kbp2_obs_pdb_rrfaa_coeff', 'AKBP_kbp2_exp_pdb_rrfaa_coeff', 'AKBP_kbp2_pdb_rrfaa_coeff', 'AKBP_kbp1_obs_idp_rr_coeff', 'AKBP_kbp1_exp_idp_rr_coeff', 'AKBP_kbp1_idp_rr_coeff', 'AKBP_kbp2_obs_idp_rr_coeff', 'AKBP_kbp2_exp_idp_rr_coeff', 'AKBP_kbp2_idp_rr_coeff', 'AKBP_kbp1_obs_revoromqa_aa_coeff', 'AKBP_kbp1_exp_revoromqa_aa_coeff', 'AKBP_kbp1_revoromqa_aa_coeff', 'AKBP_kbp1_obs_pdb_aa_solvated_coeff', 'AKBP_kbp1_exp_pdb_aa_solvated_coeff', 'AKBP_kbp1_pdb_aa_solvated_coeff', 'AKBP_kbp2_obs_pdb_aa_solvated_coeff', 'AKBP_kbp2_exp_pdb_aa_solvated_coeff', 'AKBP_kbp2_pdb_aa_solvated_coeff', 'AKBP_kbp1_obs_pdb_rr_solvated_coeff', 'AKBP_kbp1_exp_pdb_rr_solvated_coeff', 'AKBP_kbp1_pdb_rr_solvated_coeff', 'AKBP_kbp2_obs_pdb_rr_solvated_coeff', 'AKBP_kbp2_exp_pdb_rr_solvated_coeff', 'AKBP_kbp2_pdb_rr_solvated_coeff', 'AKBP_kbp2_obs_pdb_rrfaa_solvated_coeff', 'AKBP_kbp2_exp_pdb_rrfaa_solvated_coeff', 'AKBP_kbp2_pdb_rrfaa_solvated_coeff', 'AKBP_kbp1_obs_idp_rr_solvated_coeff', 'AKBP_kbp1_exp_idp_rr_solvated_coeff', 'AKBP_kbp1_idp_rr_solvated_coeff', 'AKBP_kbp2_obs_idp_rr_solvated_coeff', 'AKBP_kbp2_exp_idp_rr_solvated_coeff', 'AKBP_kbp2_idp_rr_solvated_coeff', 'AKBP_kbp1_obs_revoromqa_aa_solvated_coeff', 'AKBP_kbp1_exp_revoromqa_aa_solvated_coeff', 'AKBP_kbp1_revoromqa_aa_solvated_coeff']].values, dtype=torch.float32)
	edge_index=torch.tensor(data_frame_links[['ir_contact_index1', 'ir_contact_index2']].values.T, dtype=torch.long)
	edge_attr=torch.tensor(data_frame_links[['edge_value', 'angle_value', 'self_edge_value', 'self_angle_value']].values, dtype=torch.float32)
	graph=torch_geometric.data.Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
	return graph

try:
	file_with_model_files=sys.argv[1]
	file_with_input_graph_files_prefixes=sys.argv[2]
	file_with_output_predictions_files=sys.argv[3]
except IndexError:
	sys.stderr.write("Not all required arguments were provided.\n")
	sys.exit(1)
except ValueError:
	sys.stderr.write("One or more arguments could not be converted to the required type.\n")
	sys.exit(1)

model_files=read_list_of_strings(file_with_model_files)
input_graph_files_prefixes=read_list_of_strings(file_with_input_graph_files_prefixes)
output_predictions_files=read_list_of_strings(file_with_output_predictions_files)

if len(input_graph_files_prefixes) != len(output_predictions_files):
	sys.stderr.write("Input and output lists are not of the same length.\n")
	sys.exit(1)

device=torch.device('cpu')

models=[]

for model_file in model_files:
	model_params=read_list_of_numbers(model_file+".params")
	model=CustomGNNvA(
		input_size=int(model_params[0]),
		num_of_conv_layers=int(model_params[1]),
		hidden_size1=int(model_params[2]),
		hidden_size2=int(model_params[3]),
		attention_heads=int(model_params[4]),
		dropout_rate=float(model_params[5])
	)
	model.load_state_dict(torch.load(model_file, map_location=device))
	model = model.to(device)
	model=model.to(device)
	model.eval()
	models.append(model)

with torch.no_grad():
	for input_graph_files_prefix, output_predictions_file in zip(input_graph_files_prefixes, output_predictions_files):
		data=read_graph(input_graph_files_prefix)
		data=data.to(device)
		N=data.x.size(0)
		sum_of_pred_y=torch.zeros(N, device=device)
		for model in models:
			pred_y=model(data.x, data.edge_index, data.edge_attr)
			sum_of_pred_y+=pred_y.squeeze()
		average_of_pred_y=sum_of_pred_y/len(models)
		average_of_pred_y_np=average_of_pred_y.cpu().detach().numpy()
		numpy.savetxt(output_predictions_file, average_of_pred_y_np, fmt='%10.5f')

