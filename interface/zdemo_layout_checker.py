
import os
from layout_checker import check_file_for_container_conflicts

# Get the path dynamically
script_dir = os.path.dirname(__file__)
file_to_check = os.path.join(script_dir, "app.py")

check_file_for_container_conflicts(file_to_check)