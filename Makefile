 # create make command "prepare-env" that install miniconda if not installed then create conda environment "ira_env" and install all packages in requirements.txt
prepare-env:
	@echo "Creating conda environment..."
	@conda create --name ira_env python=3.11
	@echo "Conda environment created."

	@echo "Activating conda environment..."
	@conda activate ira_env
	@echo "Conda environment activated."

	@echo "Installing packages..."
	@pip install -r requirements.txt
	@echo "Packages installed."
	
	@echo "Done."