import os
import json
import base64
import binascii

try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from azure.storage.blob import BlockBlobService
from azure.common import AzureMissingResourceHttpError, AzureHttpError

from dtoolcore.utils import (
    generate_identifier,
    get_config_value,
    mkdir_parents,
    generous_parse_uri,
)

from dtoolcore.filehasher import FileHasher, md5sum_hexdigest

def base64_to_hex(input_string):
    """Retun the hex encoded version of the base64 encoded input string."""

    return binascii.hexlify(base64.b64decode(input_string)).decode()

_STRUCTURE_PARAMETERS = {
    "fragments_key_prefix": "fragments/",
    "overlays_key_prefix": "overlays/",
    "dataset_readme_key": "README.yml",
    "manifest_key": "manifest.json",
    "structure_dict_key": "structure.json",
    "dtool_readme_key": "README.txt"

}

_DTOOL_README_TXT = """README
======
This is a Dtool dataset stored in Azure storage.

Content provided during the dataset creation process
----------------------------------------------------

Azure container named $UUID, where UUID is the unique identifier for the
dataset.

Dataset descriptive metadata: README.yml

Dataset items. The keys for these blobs are item identifiers. An item identifier
is the sha1sum hexdigest of the relative path used to represent the file on
traditional file system disk.

Administrative metadata describing the dataset is encoded as metadata on the
container.


Automatically generated blobs
-----------------------------

This file: README.txt
Structural metadata describing the dataset: structure.json
Structural metadata describing the data items: manifest.json
Per item descriptive metadata prefixed by: overlays/
"""


class AzureStorageBroker(object):

    #: Attribute used to define the type of storage broker.
    key = "azure"

    #: Attribute used by :class:`dtoolcore.ProtoDataSet` to write the hash
    #: function name to the manifest.
    hasher = FileHasher(md5sum_hexdigest)

    def __init__(self, uri, config_path=None):

        parse_result = generous_parse_uri(uri)

        self.storage_account = parse_result.netloc

        uuid = parse_result.path[1:]

        self.uuid = uuid


        self._azure_cache_abspath = get_config_value(
            "DTOOL_AZURE_CACHE_DIRECTORY",
            config_path=config_path,
            default=os.path.expanduser("~/.cache/dtool/azure")
        )

        account_name=get_config_value(
            "DTOOL_AZURE_ACCOUNT_NAME",
            config_path=os.path.expanduser("~/.config/dtoolazure/config.json")
        )

        account_key=get_config_value(
            "DTOOL_AZURE_ACCOUNT_KEY",
            config_path=os.path.expanduser("~/.config/dtoolazure/config.json")
        )

        self._blobservice = BlockBlobService(
            account_name=account_name,
            account_key=account_key
        )

        self._set_prefixes()

    def _set_prefixes(self):

        def generate_key(structure_dict_key):
            return _STRUCTURE_PARAMETERS[structure_dict_key]

        self.fragments_key_prefix = generate_key('fragments_key_prefix')
        self.overlays_key_prefix = generate_key('overlays_key_prefix')

        self.dtool_readme_key = generate_key("dtool_readme_key")
        self.dataset_readme_key = generate_key("dataset_readme_key")
        self.manifest_key = generate_key("manifest_key")
        self.structure_dict_key = generate_key("structure_dict_key")

    @classmethod
    def generate_uri(cls, name, uuid, base_uri):

        scheme, netloc, path, _, _, _ = generous_parse_uri(base_uri)
        assert scheme == 'azure'

        # Force path (third component of tuple) to be the dataset UUID
        uri = urlunparse((scheme, netloc, uuid, _, _, _))

        return uri

    @classmethod
    def list_dataset_uris(cls, base_uri, config_path):
        """Return list containing URIs with base URI."""

        account_name=get_config_value(
            "DTOOL_AZURE_ACCOUNT_NAME",
            config_path=os.path.expanduser("~/.config/dtoolazure/config.json")
        )

        account_key=get_config_value(
            "DTOOL_AZURE_ACCOUNT_KEY",
            config_path=os.path.expanduser("~/.config/dtoolazure/config.json")
        )

        blobservice = BlockBlobService(
            account_name=account_name,
            account_key=account_key
        )

        containers = blobservice.list_containers(include_metadata=True)

        uri_list = []
        for c in containers:
            admin_metadata = c.metadata
            uri = cls.generate_uri(
                admin_metadata['name'],
                admin_metadata['uuid'],
                base_uri
            )
            uri_list.append(uri)

        return uri_list

    def create_structure(self):

        self._blobservice.create_container(self.uuid)

        self.store_text(
            self.structure_dict_key,
            json.dumps(_STRUCTURE_PARAMETERS)
        )

        self.store_text(
            self.dtool_readme_key,
            _DTOOL_README_TXT
        )

    def put_admin_metadata(self, admin_metadata):

        for k, v in admin_metadata.items():
            admin_metadata[k] = str(v)

        self._blobservice.set_container_metadata(
            self.uuid,
            admin_metadata
        )

    def get_admin_metadata(self):

        return self._blobservice.get_container_metadata(
            self.uuid
        )


    def get_readme_content(self):

        return self.get_text(self.dataset_readme_key)

    def has_admin_metadata(self):
        """Return True if the administrative metadata exists.

        This is the definition of being a "dataset".
        """

        try:
            self.get_admin_metadata()
            return True
        except (AzureMissingResourceHttpError, AzureHttpError):
            return False

    def get_manifest(self):

        manifest_as_text = self.get_text('manifest.json')

        return json.loads(manifest_as_text)

    def get_overlay(self, overlay_name):
        """Return overlay as a dictionary.

        :param overlay_name: name of the overlay
        :returns: overlay as a dictionary
        """

        overlay_fpath = self.overlays_key_prefix + overlay_name + '.json'

        overlay_as_string = self.get_text(overlay_fpath)

        return json.loads(overlay_as_string)

    def list_overlay_names(self):
        """Return list of overlay names."""

        overlay_names = []
        for blob in self._blobservice.list_blobs(
            self.uuid,
            prefix=self.overlays_key_prefix
        ):
            overlay_file = blob.name.rsplit('/', 1)[-1]
            overlay_name, ext = overlay_file.split('.')
            overlay_names.append(overlay_name)

        return overlay_names

    def put_overlay(self, overlay_name, overlay):
        """Store the overlay by writing it to Azure.

        It is the client's responsibility to ensure that the overlay provided
        is a dictionary with valid contents.

        :param overlay_name: name of the overlay
        :overlay: overlay dictionary
        """
        blob_fpath = os.path.join(
            self.overlays_key_prefix,
            overlay_name + '.json'
        )
        self.store_text(blob_fpath, json.dumps(overlay))

    # Protodataset methods

    def put_readme(self, content):

        self.store_text(self.dataset_readme_key, content)

    def put_item(self, fpath, relpath):

        identifier = generate_identifier(relpath)

        self._blobservice.create_blob_from_path(
            self.uuid,
            identifier,
            fpath
        )

        self._blobservice.set_blob_metadata(
            container_name=self.uuid,
            blob_name=identifier,
            metadata={
                "relpath": relpath,
                "type": "item"
            }
        )

        return relpath

    def add_item_metadata(self, handle, key, value):
        """Store the given key:value pair for the item associated with handle.

        :param handle: handle for accessing an item before the dataset is
                       frozen
        :param key: metadata key
        :param value: metadata value
        """

        identifier = generate_identifier(handle)


        metadata_blob_suffix = "{}.{}.json".format(identifier, key)
        metadata_blob_name = self.fragments_key_prefix + metadata_blob_suffix

        self._blobservice.create_blob_from_text(
            self.uuid,
            metadata_blob_name,
            json.dumps(value)
        )

        self._blobservice.set_blob_metadata(
            container_name=self.uuid,
            blob_name=metadata_blob_name,
            metadata={
                "type": "item_metadata"
            }
        )

    def get_text(self, name):

        try:
            text_blob = self._blobservice.get_blob_to_text(
                self.uuid,
                name
            )
        except AzureMissingResourceHttpError:
            raise NameError("Can't retrieve text with name {}".format(name))

        return text_blob.content

    def store_text(self, name, contents):
        """Store the given text contents so that they are later retrievable by
        the given name."""

        self._blobservice.create_blob_from_text(
            self.uuid,
            name,
            contents
        )


    def get_item_abspath(self, identifier):
        """Return absolute path at which item content can be accessed.

        :param identifier: item identifier
        :returns: absolute path from which the item content can be accessed
        """
        admin_metadata = self.get_admin_metadata()
        uuid = admin_metadata["uuid"]
        # Create directory for the specific dataset.
        dataset_cache_abspath = os.path.join(self._azure_cache_abspath, uuid)
        mkdir_parents(dataset_cache_abspath)

        metadata = self._blobservice.get_blob_metadata(
            self.uuid,
            identifier
        )

        relpath = metadata['relpath']
        _, ext = os.path.splitext(relpath)

        local_item_abspath = os.path.join(
            dataset_cache_abspath,
            identifier + ext
        )
        if not os.path.isfile(local_item_abspath):

            self._blobservice.get_blob_to_path(
                self.uuid,
                identifier,
                local_item_abspath
            )

        return local_item_abspath
        # original_path = self.item_properties(identifier)['path']


    def put_manifest(self, manifest):
        """Store the manifest by writing it to Azure.

        It is the client's responsibility to ensure that the manifest provided
        is a dictionary with valid contents.

        :param manifest: dictionary with manifest structural metadata
        """
        self.store_text('manifest.json', json.dumps(manifest))

    def iter_item_handles(self):
        """Return iterator over item handles."""

        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            include='metadata'
        )

        for blob in blob_generator:
            if 'type' in blob.metadata:
                if blob.metadata['type'] == 'item':
                    handle = blob.metadata['relpath']
                    yield handle

    def item_properties(self, handle):
        """Return properties of the item with the given handle."""

        identifier = generate_identifier(handle)
        blob = self._blobservice.get_blob_properties(
            self.uuid,
            identifier
        )

        md5_base64 = blob.properties.content_settings.content_md5
        if md5_base64 is None:
            md5_hexdigest = None
        else:
            md5_hexdigest = base64_to_hex(md5_base64)

        properties = {
            'relpath': blob.metadata['relpath'],
            'size_in_bytes': blob.properties.content_length,
            # NOTE - timezones are horrible and this doesn't take account of
            # them
            'utc_timestamp': blob.properties.last_modified.strftime("%s"),
            'hash': md5_hexdigest
        }

        return properties

    def pre_freeze_hook(self):
        pass

    def post_freeze_hook(self):

        self.fragments_key_prefix
        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            prefix=self.fragments_key_prefix
        )

        # Delete the temporary fragment metadata objects from the bucket.
        for blob in blob_generator:
            self._blobservice.delete_blob(self.uuid, blob.name)

    def get_item_metadata(self, handle):
        """Return dictionary containing all metadata associated with handle.

        In other words all the metadata added using the ``add_item_metadata``
        method.

        :param handle: handle for accessing an item before the dataset is
                       frozen
        :returns: dictionary containing item metadata
        """

        metadata = {}

        identifier = generate_identifier(handle)
        prefix = self.fragments_key_prefix + '{}'.format(identifier)

        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            include='metadata',
            prefix=prefix
        )

        for blob in blob_generator:
            metadata_key = blob.name.split('.')[-2]
            value_as_string = self.get_text(blob.name)
            value = json.loads(value_as_string)

            metadata[metadata_key] = value

        return metadata
