import nbtlib
import os
import shutil


# REturn [T/F] if healing machine is in NBT file
def check_healing_machine(nbt_file_path):
    try:
        nbt_file = nbtlib.load(nbt_file_path)
        def recursive_find(data):
            if isinstance(data, nbtlib.tag.String):
                if str(data) == "cobblemon:healing_machine":
                    return True
            elif isinstance(data, dict):
                for key, value in data.items():
                    if recursive_find(value):
                        return True
            elif isinstance(data, list):
                for _, item in enumerate(data):
                    if recursive_find(item):
                        return True
        if recursive_find(nbt_file):
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Error: File not found at {nbt_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")  


# Replaces "cobblemon:healing_machine" with "minecraft:brewing_stand"
def replace_healing_machine(nbt_file_path, output_file_path):
    try:
        nbt_file = nbtlib.load(nbt_file_path)

        def recursive_replace(data):
            if isinstance(data, nbtlib.tag.String):
                if str(data) == "cobblemon:healing_machine":
                    return nbtlib.tag.String("minecraft:brewing_stand")
                else:
                    return data
            elif isinstance(data, dict):
                for key, value in data.items():
                    data[key] = recursive_replace(value)
                return data
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    data[i] = recursive_replace(item)
                return data
            else:
                return data

        nbt_file = recursive_replace(nbt_file)

        # nbtlib.save(nbt_file, output_file_path)
        nbt_file.save(output_file_path)
        print(f"Successfully replaced and saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {nbt_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def test():
    input_file = "pokecenter.nbt"
    output_file = "new.nbt"
    print(check_healing_machine(input_file))
    replace_healing_machine(input_file, output_file)



"""
Recursively scans a source directory for .nbt files, filters them using the check_healing_machine function,
and converts passing files to the destination directory using replace_healing_machine function.
Empty directories are not created in the destination.

Args:
    source_dir (str): Path to the source directory
    destination_dir (str): Path to the destination directory
    check_healing_machine (function): Function that takes a filepath and returns True/False
    replace_healing_machine (function): Function that takes input and output filepaths
"""
def filter_and_convert_nbt_files(source_dir, destination_dir):
    # Keep track of directories we've created to avoid creating empty ones
    created_dirs = set()
    
    # Walk through all files and directories in the source
    for root, dirs, files in os.walk(source_dir):
        # Filter for .nbt files
        nbt_files = [f for f in files if f.endswith('.nbt')]
        
        for file in nbt_files:
            input_file = os.path.join(root, file)
            
            # Check if the file passes our criteria
            if check_healing_machine(input_file):
                # Get the relative path from source to destination
                rel_path = os.path.relpath(root, source_dir)
                dest_dir = os.path.join(destination_dir, rel_path)
                
                # Create the destination directory if needed
                if dest_dir not in created_dirs and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    created_dirs.add(dest_dir)
                
                # Generate output file path
                output_file = os.path.join(dest_dir, file)
                
                # Convert the file using the provided function
                replace_healing_machine(input_file, output_file)


if __name__ == "__main__":
    source = "structure_original"
    destination = "structure"
    filter_and_convert_nbt_files(source, destination)