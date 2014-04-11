import os
CURRENT_DIR =os.getcwd()
activate= open(CURRENT_DIR+'/venv/bin/activate','r')
activate_list=activate.read().split('\n')
for line in  activate_list:
	if line[:line.find('=')] == "VIRTUAL_ENV":
		print line
		updated_line ='VIRTUAL_ENV="'+os.path.join(CURRENT_DIR,"venv")+'"'
		print updated_line
		activate_list[activate_list.index(line)]=updated_line
		break
activate.close()

activate= open(CURRENT_DIR+'/venv/bin/activate','w')
for line in activate_list:
	activate.write(line +"\n")
activate.close()