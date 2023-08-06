# -*- coding: utf8 -*-
import json
import logging
import os


class MetadataFiles(object):
    metadata_ext = '.metadata.json'

    @classmethod
    def __meta_companion_file_name(cls, metadata_file_name):
        return metadata_file_name[:-len(cls.metadata_ext)]

    @classmethod
    def __is_meta_folder_file_name(cls, metadata_file_name):
        return os.path.basename(metadata_file_name).lower() == 'folder' + cls.metadata_ext

    @classmethod
    def __convert_data_unsupported_type(cls, data):
        for key, val in data.items():
            if isinstance(val, (dict, list)):  # we convert arrays and dicts into string as we don't support them yet
                data[key] = json.dumps(val)

    @classmethod
    def __handle_json_file(cls, metadata_json_file, on_data):
        from .data_sync import InvalidJsonFile

        with open(metadata_json_file) as metadata_file:
            try:
                data = json.load(metadata_file)
                return on_data(data)
            except ValueError:
                raise InvalidJsonFile(metadata_json_file)

    @classmethod
    def __get_metadata_info(cls, repo, rel_metadata_file_name):
        full_path_metadata = os.path.join(repo.data_path, rel_metadata_file_name)

        rel_path_key = rel_metadata_file_name[:-len(cls.metadata_ext)]

        def handle_data(data):
            cls.__convert_data_unsupported_type(data)

            return rel_path_key, data

        return cls.__handle_json_file(full_path_metadata, handle_data)

    @classmethod
    def __get_folder_metadata_info(cls, repo, rel_metadata_file_name):
        full_path_metadata = os.path.join(repo.data_path, rel_metadata_file_name)

        rel_path = os.path.relpath(os.path.dirname(full_path_metadata), repo.data_path)

        if rel_path == '.':
            rel_path = ''

        def handle_data(all_files_data):
            for filename, file_data in all_files_data.items():
                cls.__convert_data_unsupported_type(file_data)
                rel_path_key = os.path.join(rel_path, filename)

                yield rel_path_key, file_data

        return cls.__handle_json_file(full_path_metadata, handle_data)

    @classmethod
    def __get_metadata(cls, repo, data_files_info, metadata_rel_file_name):
        if cls.__is_meta_folder_file_name(metadata_rel_file_name):
            for rel_path_key, data in cls.__get_folder_metadata_info(repo, metadata_rel_file_name):
                yield rel_path_key, data
        elif cls.__meta_companion_file_name(metadata_rel_file_name) in data_files_info:
            rel_path_key, data = cls.__get_metadata_info(repo, metadata_rel_file_name)

            yield rel_path_key, data
        else:
            logging.debug("file %s doesn't have a data point file", metadata_rel_file_name)

    @classmethod
    def load_all_metadata(cls, repo, data_files_info, metadata_files_list, no_progressbar=False):
        from tqdm import tqdm

        files_metadata = {}
        if len(metadata_files_list) == 0:
            return files_metadata

        for metadata_rel_file_name in tqdm(metadata_files_list, desc='Read metadata', unit=' files', ncols=80, disable=no_progressbar):
            for rel_path_key, data in cls.__get_metadata(repo, data_files_info, metadata_rel_file_name):
                files_metadata.setdefault(rel_path_key, {}).update(data)

        return files_metadata
