import os
import hashlib
import shutil
import filecmp


def synchronize(path_source_folder: str, path_replica_folder: str, logger):
    """
    Synchronize two folders 'path_source_folder' and 'path_replica_folder'.
    Variable 'logger' is an instance of the Logger calss. It is passed to handle the logging.
    """
    logger.info("Synchronization started.")

    source_hash = hash_folder(path_source_folder)
    replica_hash = hash_folder(path_replica_folder)

    if source_hash != replica_hash:
        # adding new files
        # loop through source folder - if file does not exist in replica folder, copy it
        for root, dirs, files in os.walk(path_source_folder):
            for file in files:
                path_source_file = os.path.join(root, file)
                path_replica_file = get_absolute_path(path_source_file, path_source_folder, path_replica_folder)
                    
                # check if the file exists in the source directory
                if not os.path.exists(path_replica_file):
                    os.makedirs(os.path.dirname(path_replica_file), exist_ok=True)
                    copy_link_or_file(path_source_file, path_replica_file, logger)

                # exists, but different content
                elif not filecmp.cmp(path_replica_file, path_source_file, shallow=False):
                    os.remove(path_replica_file)
                    copy_link_or_file(path_source_file, path_replica_file, logger)
                        
            # check for empty folders
            for dir in dirs:
                path_source_dir = os.path.join(root, dir)
                path_replica_dir = get_absolute_path(path_source_dir, path_source_folder, path_replica_folder)

                if not os.path.exists(path_replica_dir) and is_directory_empty(path_source_dir):
                    logger.info(f"Creating folder {path_source_dir} in a replica folder.")
                    os.makedirs(path_replica_dir)


        # deleting old files - delete files in replica folder that are not present in source folder
        files_in_source_folder = set(list_all_files(path_source_folder))
        files_in_replica_folder = set(list_all_files(path_replica_folder))
        
        files_to_delete = files_in_replica_folder - files_in_source_folder
            
        for file_to_delete in files_to_delete:
            # get the absolute path
            file_to_delete = os.path.normpath(os.path.join(path_replica_folder, file_to_delete))

            if os.path.isfile(file_to_delete) or os.path.islink(file_to_delete):
                logger.info(f"Removing {file_to_delete} from replica folder.")
                os.remove(file_to_delete)

            elif os.path.isdir(file_to_delete):
                logger.info(f"Removing {file_to_delete} from replica folder.")
                shutil.rmtree(file_to_delete)
                
    logger.info("Synchronization completed.")
        


def get_absolute_path(path_source_file, path_source_folder, path_replica_folder):
    """
    For given path 'path_source_file' of the file from the source folder 'path_source_folder', get the absolute path of this file 
    with respect to the replica folder 'path_replica_folder'.
    """
    path_source_file_relative = os.path.relpath(path_source_file, path_source_folder)
    
    return os.path.join(path_replica_folder, path_source_file_relative)



def list_all_files(directory):
    """
    List all files and empty directories in a directory 'directory', including subdirectories.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        
        # add current directory itself if it's not the root directory
        if relative_root != '.':
            file_list.append(relative_root)
        
        # add files in the current directory
        for file in files:
            relative_file_path = os.path.join(relative_root, file)
            file_list.append(relative_file_path)
        
        # add empty directories in the current directory
        for dir in dirs:
            if len(os.listdir(os.path.join(root, dir))) == 0:
                relative_dir_path = os.path.join(relative_root, dir)
                file_list.append(relative_dir_path)

    return file_list


def copy_link_or_file(path_source_file, path_replica_file, logger):
    # copy link
    if os.path.islink(path_source_file):
        logger.info(f"Copying symbolic link {path_source_file} into a replica folder.")
        link_target = os.readlink(path_source_file)
        os.symlink(link_target, path_replica_file)

    # copy file
    else:
        logger.info(f"Copying file {path_source_file} into a replica folder.")
        shutil.copy2(path_source_file, path_replica_file)



def hash_folder(folder_path):
    """
    Get a has for given folder path 'folder_path'.
    """
    hash = hashlib.sha256()

    for root, dirs, files in os.walk(folder_path):
        # hash files
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                file_hash = hashlib.file_digest(f, "sha512").hexdigest()
                

            hash.update(file_hash.encode())

        # hash dirs
        for dir in dirs:
            dir_hash = hashlib.sha512(dir.encode()).hexdigest()
            hash.update(dir_hash.encode())

    return hash.hexdigest()


def test_path(path: str):
    """
    Test if path 'path' exits.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    

def is_directory_empty(directory):
    """
    Check if a directory is empty.
    """
    return not any(os.scandir(directory))