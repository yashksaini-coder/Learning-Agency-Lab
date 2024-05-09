import os

def create_plot_directory():
    """
    Function to create a folder named "plots" one folder above the current directory
    """
    # Get the current working directory
    current_dir = os.getcwd()
    # Navigate to the parent directory
    parent_dir = os.path.dirname(current_dir)
    
    # Create a directory named "plots" in the parent directory if it doesn't exist
    plots_dir = os.path.join(parent_dir, "plots")
    if not os.path.exists(plots_dir):
        os.mkdir(plots_dir)
