import os
import shutil
import ntpath
import csv
import itertools as IT

def check_if_directory_exists(dir_path):
    return os.path.isdir(dir_path)


def check_if_file_exists(file_path):
    return os.path.isfile(file_path)


def make_directory(directory_path):
    is_successful = True
    try:
        os.mkdir(directory_path)
    except OSError:
        is_successful = False

    return is_successful


def delete_directory(directory_path):
    is_successful = True
    try:
        shutil.rmtree(directory_path)
    except OSError:
        is_successful = False

    return is_successful


def get_list_of_subdirectory_paths(root_dir):
    paths = []
    if check_if_directory_exists(root_dir):
        for subdir_path in os.scandir(root_dir):
            #subdir_path = subdir_path.name
            #subdir_path = subdir_path.replace("\\", "/")
            paths.append(subdir_path)

    return paths


def get_list_of_file_paths_in_directory(root_dir):
    paths = [os.path.join(root_dir, f) for f in os.listdir(root_dir) if check_if_file_exists(os.path.join(root_dir, f))]
    return paths


def get_name_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_file_name_without_extension(file_name):
    return os.path.splitext(file_name)[0]


def merge_multiple_csv_files(filepaths, filelabels, destination_filepath):
    dest_rows = []
    for i in range(len(filepaths)):
        filepath = filepaths[i]
        file_label = filelabels[i]
        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            src_csv_rows = [["", "", file_label , ""]]
            for row in csv_reader:
                src_csv_rows.append(row)

            if len(dest_rows) == 0:
                dest_rows = src_csv_rows
            else:
                for index in range(len(dest_rows)):
                    dest_rows[index].extend(src_csv_rows[index][1:])

    with open(destination_filepath, 'w', newline='') as dest_csv_path:
        dest_csv_writer = csv.writer(dest_csv_path, delimiter=',')
        for row in dest_rows:
            dest_csv_writer.writerow(row)
