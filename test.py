import torch
print(torch.cuda.is_available())

from db import trunc_descs, create
trunc_descs()
create()