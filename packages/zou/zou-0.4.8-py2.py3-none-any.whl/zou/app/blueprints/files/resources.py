import datetime

from flask import request, abort
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from zou.app.utils import permissions
from zou.app.services import (
    file_tree,
    files_service,
    persons_service,
    projects_service,
    assets_service,
    tasks_service,
    entities_service,
    user_service
)

from zou.app.services.exception import (
    WorkingFileNotFoundException,
    OutputFileNotFoundException,
    OutputTypeNotFoundException,
    SoftwareNotFoundException,
    PersonNotFoundException,
    ProjectNotFoundException,
    TaskNotFoundException,
    WrongFileTreeFileException,
    WrongPathFormatException,
    MalformedFileTreeException,
    EntryAlreadyExistsException
)


class FolderPathResource(Resource):
    """
    Return folder path corresponding at given task and parameters. Path is built
    from file template.
    """

    @jwt_required
    def post(self, task_id):
        (
            mode,
            software_id,
            output_type_id,
            name,
            separator
        ) = self.get_arguments()

        try:
            task = tasks_service.get_task(task_id)
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(task["project_id"])
            output_type = files_service.get_output_type(output_type_id)
            software = files_service.get_software(software_id)
            path = file_tree.get_folder_path(
                task,
                mode=mode,
                software=software,
                output_type=output_type,
                name=name,
                sep=separator
            )
        except OutputTypeNotFoundException:
            return {
                "error": "Given output type does not exist.",
                "received_data": request.json,
            }, 400
        except SoftwareNotFoundException:
            return {
                "error": "Given software does not exist.",
                "received_data": request.json,
            }, 400
        except MalformedFileTreeException:
            return {
                "error":
                    "Tree is not properly written, check modes and variables",
                "received_data": request.json,
            }, 400

        return {"path": path}, 200

    def get_arguments(self):
        parser = reqparse.RequestParser()
        geometry_type = files_service.get_or_create_output_type("geometry")
        maxsoft = files_service.get_or_create_software("3ds Max", "max", ".max")

        parser.add_argument("mode", default="working")
        parser.add_argument("sep", default="/")
        parser.add_argument("software_id", default=maxsoft["id"])
        parser.add_argument("output_type_id", default=geometry_type["id"])
        parser.add_argument("name", default="name")
        args = parser.parse_args()

        return (
            args["mode"],
            args["software_id"],
            args["output_type_id"],
            args["name"],
            args["sep"],
        )


class FilePathResource(Resource):

    @jwt_required
    def post(self, task_id):
        (
            mode,
            version,
            comment,
            software_id,
            output_type_id,
            name,
            separator
        ) = self.get_arguments()

        try:
            task = tasks_service.get_task(task_id)
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(task["project_id"])

            output_type = files_service.get_output_type(output_type_id)
            software = files_service.get_software(software_id)
            is_version_set_by_user = version == 0
            if is_version_set_by_user and mode == "working":
                version = self.get_next_version(task_id, name)

            file_path = file_tree.get_folder_path(
                task,
                mode=mode,
                software=software,
                output_type=output_type,
                name=name,
                sep=separator
            )
            file_name = file_tree.get_file_name(
                task,
                mode=mode,
                version=version,
                software=software,
                output_type=output_type,
                name=name
            )
        except MalformedFileTreeException:
            return {
                "error":
                    "Tree is not properly written, check modes and variables",
                "received_data": request.json,
            }, 400

        return {"path": file_path, "name": file_name}, 200

    def get_next_version(self, task_id, name):
        last_working_files = \
            files_service.get_last_working_files_for_task(task_id)
        working_file = last_working_files.get(name, None)
        if working_file is not None:
            version = working_file["revision"] + 1
        else:
            version = 1
        return version

    def get_arguments(self):
        geometry_type = files_service.get_or_create_output_type("geometry")
        maxsoft = files_service.get_or_create_software("3ds Max", "max", ".max")

        parser = reqparse.RequestParser()
        parser.add_argument("mode", default="working")
        parser.add_argument("comment", default="")
        parser.add_argument("version", default=0)
        parser.add_argument("software_id", default=maxsoft["id"])
        parser.add_argument("output_type_id", default=geometry_type["id"])
        parser.add_argument("name", default="")
        parser.add_argument("sep", default="/")
        args = parser.parse_args()

        return (
            args["mode"],
            args["version"],
            args["comment"],
            args["software_id"],
            args["output_type_id"],
            args["name"],
            args["sep"]
        )


class InstanceFilePathResource(Resource):

    @jwt_required
    def post(self, instance_id, output_type_id):
        (
            mode,
            version,
            name,
            separator
        ) = self.get_arguments()

        try:
            asset_instance = assets_service.get_asset_instance(instance_id)
            asset = assets_service.get_asset(asset_instance["asset_id"])
            output_type = files_service.get_output_type(output_type_id)
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(asset["project_id"])

            folder_path = file_tree.get_instance_folder_path(
                asset_instance,
                mode=mode,
                output_type=output_type,
                sep=separator
            )
            file_name = file_tree.get_instance_file_name(
                asset_instance,
                mode=mode,
                version=version,
                output_type=output_type,
                name=name
            )
        except MalformedFileTreeException:
            return {
                "error":
                    "Tree is not properly written, check modes and variables",
                "received_data": request.json,
            }, 400

        return {"path": folder_path, "name": file_name}, 200

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mode", default="output")
        parser.add_argument("version", default=1)
        parser.add_argument("name", default="")
        parser.add_argument("sep", default="/")
        args = parser.parse_args()

        return (
            args["mode"],
            args["version"],
            args["name"],
            args["sep"]
        )


class SetTreeResource(Resource):

    @jwt_required
    def post(self, project_id):
        (tree_name) = self.get_arguments()

        try:
            permissions.check_manager_permissions()
            tree = file_tree.get_tree_from_file(tree_name)
            project = projects_service.update_project(
                project_id,
                {"file_tree": tree}
            )
        except WrongFileTreeFileException:
            abort(400, "Selected tree is not available")

        return project

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "tree_name",
            help="The name of the tree to set is required.",
            required=True
        )
        args = parser.parse_args()

        return (
            args.get("tree_name", ""),
        )


class GetTaskFromPathResource(Resource):

    @jwt_required
    def post(self):
        (
            file_path,
            project_id,
            path_type,
            mode,
            sep
        ) = self.get_arguments()

        try:
            project = projects_service.get_project(project_id)
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(project_id)

            if path_type == "shot":
                task = file_tree.get_shot_task_from_path(
                    file_path,
                    project,
                    mode,
                    sep
                )
            else:
                task = file_tree.get_asset_task_from_path(
                    file_path,
                    project,
                    mode,
                    sep
                )

        except ProjectNotFoundException:
            return {
                "error": "Given project does not exist.",
                "received_data": request.json,
            }, 400

        except WrongPathFormatException:
            return {
                "error": "The given path lacks of information..",
                "received_data": request.json
            }, 400
        except TaskNotFoundException:
            return {
                "error": "No task exist for this path.",
                "received_data": request.json
            }, 400

        return task

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "file_path",
            help="The file path is required.",
            required=True
        )
        parser.add_argument(
            "project_id",
            help="The project ID is required.",
            required=True
        )
        parser.add_argument(
            "type",
            help="The type (asset or shot) is required.",
            required=True
        )
        parser.add_argument("mode", "working")
        parser.add_argument("sep", "/")
        args = parser.parse_args()

        return (
            args["file_path"],
            args["project_id"],
            args["type"],
            args["mode"],
            args["sep"]
        )


class CommentWorkingFileResource(Resource):

    @jwt_required
    def put(self, working_file_id):
        comment = self.get_comment_from_args()
        working_file = files_service.get_working_file(working_file_id)
        task = tasks_service.get_task(working_file["task_id"])
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(task["project_id"])
        working_file = self.update_comment(working_file_id, comment)
        return working_file

    def get_comment_from_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "comment",
            required=True,
            help="Comment field expected."
        )
        args = parser.parse_args()
        comment = args["comment"]
        return comment

    def update_comment(self, working_file_id, comment):
        working_file = files_service.update_working_file(
            working_file_id,
            {"comment": comment}
        )
        return working_file


class NewOutputFileResource(Resource):

    @jwt_required
    def post(self, working_file_id):
        (
            comment,
            person_id,
            output_type_id,
            revision,
            separator,
            extension
        ) = self.get_arguments()
        separator = "/"

        try:
            working_file = files_service.get_working_file(working_file_id)
            task = tasks_service.get_task(working_file["task_id"])
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(task["project_id"])
            output_type = files_service.get_output_type(output_type_id)
            person = persons_service.get_person(person_id)

            output_file = files_service.create_new_output_revision(
                task["entity_id"],
                working_file["id"],
                output_type["id"],
                person["id"],
                comment,
                name=working_file["name"],
                revision=revision,
                extension=extension
            )

            output_file_dict = self.add_path_info(
                output_file,
                "output",
                task,
                output_type,
                working_file["name"],
                extension,
                separator
            )
        except OutputTypeNotFoundException:
            return {"error": "Cannot find given output type."}, 400
        except PersonNotFoundException:
            return {"error": "Cannot find given person."}, 400
        except EntryAlreadyExistsException:
            return {"error": "The given output file already exists."}, 400

        return output_file_dict, 201

    def get_arguments(self):
        parser = reqparse.RequestParser()
        output_type = files_service.get_or_create_output_type("Geometry")
        parser.add_argument("output_type_id", default=output_type["id"])
        parser.add_argument("person_id", default="")
        parser.add_argument("comment", default="")
        parser.add_argument("revision", default=0, type=int)
        parser.add_argument("separator", default="/")
        parser.add_argument("extension", default="")
        args = parser.parse_args()

        return (
            args["comment"],
            args["person_id"],
            args["output_type_id"],
            args["revision"],
            args["separator"],
            args["extension"]
        )

    def add_path_info(
        self,
        output_file,
        mode,
        task,
        output_type,
        name,
        extension,
        separator
    ):
        folder_path = file_tree.get_folder_path(
            task,
            mode=mode,
            output_type=output_type,
            name=name,
            sep=separator
        )
        file_name = file_tree.get_file_name(
            task,
            mode=mode,
            version=output_file["revision"],
            output_type=output_type,
            name=name,
        )

        output_file.update({
            "folder_path": folder_path,
            "file_name": file_name
        })

        files_service.update_output_file(
            output_file["id"],
            {
                "path": "%s%s%s%s" % (
                    folder_path,
                    separator,
                    file_name,
                    extension
                )
            }
        )
        return output_file


class GetNextOutputFileResource(Resource):

    @jwt_required
    def post(self, entity_id, output_type_id):
        name = self.get_arguments()
        entity = entities_service.get_entity(entity_id)
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(entity["project_id"])
        output_type = files_service.get_output_type(output_type_id)

        next_revision_number = \
            files_service.get_next_output_file_revision(
                entity["id"],
                output_type["id"],
                name
            )

        return {
            "next_revision": next_revision_number
        }, 200

    def get_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", default="main")
        return parser.parse_args()["name"]


class LastWorkingFilesResource(Resource):

    @jwt_required
    def get(self, task_id):
        result = {}
        task = tasks_service.get_task(task_id)
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(task["project_id"])
        result = files_service.get_last_working_files_for_task(task["id"])

        return result


class LastOutputFilesResource(Resource):

    @jwt_required
    def get(self, entity_id):
        result = {}
        entity = entities_service.get_entity(entity_id)
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(entity["project_id"])
        result = files_service.get_last_output_files_for_entity(entity["id"])

        return result


class TaskWorkingFilesResource(Resource):

    @jwt_required
    def get(self, task_id):
        result = {}
        task = tasks_service.get_task(task_id)
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(task["project_id"])
        result = files_service.get_working_files_for_task(task["id"])

        return result


class NewWorkingFileResource(Resource):

    @jwt_required
    def post(self, task_id):
        (
            name,
            description,
            comment,
            person_id,
            software_id,
            revision,
            sep
        ) = self.get_arguments()

        try:
            task = tasks_service.get_task(task_id)
            if not permissions.has_manager_permissions():
                user_service.check_has_task_related(task["project_id"])
            software = files_service.get_software(software_id)
            tasks_service.assign_task(
                task_id,
                persons_service.get_current_user()["id"]
            )

            if revision == 0:
                revision = files_service.get_next_working_revision(
                    task_id,
                    name
                )

            path = self.build_path(task, name, revision, software, sep)

            working_file = files_service.create_new_working_revision(
                task_id,
                person_id,
                software_id,
                name=name,
                path=path,
                comment=comment,
                revision=revision
            )
        except EntryAlreadyExistsException:
            return {"error": "The given working file already exists."}, 400

        return working_file, 201

    def build_path(self, task, name, revision, software, sep):
        folder_path = file_tree.get_folder_path(
            task,
            name=name,
            software=software
        )
        file_name = file_tree.get_file_name(
            task,
            name=name,
            software=software,
            version=revision
        )
        return "%s%s%s" % (folder_path, sep, file_name)

    def get_arguments(self):
        person = persons_service.get_current_user()
        maxsoft = files_service.get_or_create_software("3ds Max", "max", ".max")

        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            help="The asset name is required.",
            required=True
        )
        parser.add_argument("description", default="")
        parser.add_argument("comment", default="")
        parser.add_argument("person_id", default=person["id"])
        parser.add_argument("software_id", default=maxsoft["id"])
        parser.add_argument("revision", default=0, type=int)
        parser.add_argument("sep", default="/")
        args = parser.parse_args()

        return (
            args["name"],
            args["description"],
            args["comment"],
            args["person_id"],
            args["software_id"],
            args["revision"],
            args["sep"]
        )


class ModifiedFileResource(Resource):

    @jwt_required
    def put(self, working_file_id):
        working_file = files_service.get_working_file(working_file_id)
        task = tasks_service.get_task(working_file["task_id"])
        if not permissions.has_manager_permissions():
            user_service.check_has_task_related(task["project_id"])
        working_file = files_service.update_working_file(
            working_file_id,
            {"updated_at": datetime.datetime.utcnow()}
        )
        return working_file


class FileResource(Resource):

    @jwt_required
    def get(self, file_id):
        try:
            file_dict = files_service.get_working_file(file_id)
        except WorkingFileNotFoundException:
            try:
                file_dict = files_service.get_output_file(file_id)
            except OutputFileNotFoundException:
                abort(404)

        if not permissions.has_manager_permissions():
            task = tasks_service.get_task(file_dict["task_id"])
            user_service.check_has_task_related(task["project_id"])
        return file_dict


class EntityOutputTypesResource(Resource):

    @jwt_required
    def get(self, entity_id):
        entity = entities_service.get_entity(entity_id)
        user_service.check_project_access(entity["project_id"])
        return files_service.get_output_types_for_entity(entity_id)


class EntityOutputTypeOutputFilesResource(Resource):

    @jwt_required
    def get(self, entity_id, output_type_id):
        entity = entities_service.get_entity(entity_id)
        files_service.get_output_type(output_type_id)
        user_service.check_project_access(entity["project_id"])
        return files_service.get_output_files_for_output_types_and_entity(
            entity_id,
            output_type_id
        )
