import torch
import torch_geometric

class CustomGNNvA(torch.nn.Module):
	def __init__(self, input_size, num_of_conv_layers, hidden_size1, hidden_size2, attention_heads, dropout_rate):
		super().__init__()
		self.num_of_conv_layers=num_of_conv_layers
		self.conv_layers=torch.nn.ModuleList()
		self.conv_bn_layers=torch.nn.ModuleList()
		self.conv_layers.append(torch_geometric.nn.GATv2Conv(input_size, hidden_size1, heads=attention_heads, edge_dim=4, add_self_loops=False, dropout=dropout_rate))
		self.conv_bn_layers.append(torch_geometric.nn.BatchNorm(hidden_size1*attention_heads))
		for i in range(1, num_of_conv_layers):
			self.conv_layers.append(torch_geometric.nn.GATv2Conv(hidden_size1*attention_heads, hidden_size1, heads=attention_heads, edge_dim=4, add_self_loops=False, dropout=dropout_rate))
			self.conv_bn_layers.append(torch_geometric.nn.BatchNorm(hidden_size1*attention_heads))
		self.lin1=torch.nn.Linear(hidden_size1*attention_heads, hidden_size2)
		self.lin1_do=torch.nn.Dropout(dropout_rate)
		self.lin1_bn=torch_geometric.nn.BatchNorm(hidden_size2)
		self.lin2=torch.nn.Linear(hidden_size2, 1)
		self.config_str=f"is_{input_size}_nc_{num_of_conv_layers}_hs1_{hidden_size1}_hs2_{hidden_size2}_ah_{attention_heads}_do_{dropout_rate}"
	
	def forward(self, data_x, data_edge_index, data_edge_attr):
		x=data_x
		for cvl, bnl in zip(self.conv_layers, self.conv_bn_layers):
			x=cvl(x, data_edge_index, data_edge_attr)
			x=bnl(x)
			x=torch.nn.functional.elu(x)
		x=self.lin1(x)
		x=self.lin1_do(x)
		x=self.lin1_bn(x)
		x=torch.nn.functional.elu(x)
		x=self.lin2(x)
		x=5*torch.tanh(x)
		return x

