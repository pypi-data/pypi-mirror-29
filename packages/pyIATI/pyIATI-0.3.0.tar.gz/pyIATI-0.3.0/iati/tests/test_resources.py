"""A module containing tests for the library implementation of accessing resources."""
from lxml import etree
import pytest
import iati.constants
import iati.resources
import iati.tests.resources
import iati.validator


class TestResources(object):
    """A container for tests relating to resources in general."""

    def test_resource_filesystem_path(self):
        """Check that resource file names are found correctly.

        Todo:
            Implement better assertions.

        """
        path = iati.resources.PATH_SCHEMAS
        filename = iati.resources.resource_filesystem_path(path)

        assert len(filename) > len(path)
        assert filename.endswith(path)


class TestResourceFolders(object):
    """A container for tests relating to resource folders."""

    @pytest.mark.parametrize('version, expected_version_foldername', [
        ('2.03', '2-03'),
        ('2.02', '2-02'),
        ('2.01', '2-01'),
        ('1.05', '1-05'),
        ('1.04', '1-04')
    ])
    def test_folder_name_for_version(self, version, expected_version_foldername):
        """Check that expected components are present within folder paths."""
        path = iati.resources.folder_name_for_version(version)
        assert expected_version_foldername == path

    @pytest.mark.parametrize('version', [
        '1.00',
        '1',
        1,
        1.01,  # A version must be specified as a string
        'string'
    ])
    def test_folder_name_for_version_invalid_version(self, version):
        """Check that an invalid version of the Standard raises a ValueError exception."""
        with pytest.raises(ValueError):
            iati.resources.folder_name_for_version(version)

    @pytest.mark.parametrize('path_component', [
        'resources',
        'standard'
    ])
    def test_folder_path_for_version(self, standard_version_optional, path_component):
        """Check that expected components are present within folder paths."""
        path = iati.resources.folder_path_for_version(*standard_version_optional)
        assert path_component in path

    def test_get_test_data_paths_in_folder(self):
        """Check that test data is being found in specified subfolders.

        Todo:
            Deal with multiple versions.

            Make independent of version 2.02.

        """
        paths = iati.tests.resources.get_test_data_paths_in_folder('ssot-activity-xml-fail', '2.02')

        assert len(paths) == 237


class TestResourceLibraryData(object):
    """A container for tests relating to pyIATI resources."""

    @pytest.mark.parametrize('file_name', [
        'name',
        'Name.xml',
    ])
    def test_create_lib_data_path(self, file_name):
        """Check that library data can be located."""
        path = iati.resources.create_lib_data_path(file_name)

        assert iati.resources.BASE_PATH_LIB_DATA != ''
        assert iati.resources.BASE_PATH_LIB_DATA in path
        assert file_name == path[-len(file_name):]


class TestResourceCodelists(object):
    """A container for tests relating to Codelist resources."""

    def test_codelist_flow_type(self, standard_version_optional):
        """Check that the FlowType codelist is loaded as a string and contains content."""
        path = iati.resources.create_codelist_path('FlowType', *standard_version_optional)

        content = iati.utilities.load_as_string(path)

        assert len(content) > 3200
        assert iati.validator.is_xml(content)

    def test_find_codelist_paths(self, codelist_lengths_by_version):
        """Check that all codelist paths are being found."""
        paths = iati.resources.get_codelist_paths(codelist_lengths_by_version[0])

        assert len(paths) == codelist_lengths_by_version[1]
        for path in paths:
            assert path[-4:] == iati.resources.FILE_CODELIST_EXTENSION
            assert iati.resources.PATH_CODELISTS in path

    @pytest.mark.parametrize('codelist', [
        'Name',
        'Name.xml',
    ])
    def test_get_codelist_path_name(self, standard_version_optional, codelist):
        """Check that a codelist path is found from just a name."""
        path = iati.resources.create_codelist_path(codelist, *standard_version_optional)

        assert path[-4:] == iati.resources.FILE_CODELIST_EXTENSION
        assert path.count(iati.resources.FILE_CODELIST_EXTENSION) == 1
        assert iati.resources.PATH_CODELISTS in path

    def test_get_codelist_mapping_paths(self, standard_version_optional):
        """Check that all codelist mapping paths are found."""
        codelist_mapping_paths = iati.resources.get_codelist_mapping_paths(*standard_version_optional)

        assert len(codelist_mapping_paths) == 1

    def test_create_codelist_mapping_path(self, standard_version_optional):
        """Check that the Codelist Mapping File path points to a valid XML file."""
        path = iati.resources.create_codelist_mapping_path(*standard_version_optional)

        content = iati.utilities.load_as_string(path)

        assert len(content) > 5000
        assert iati.validator.is_xml(content)


class TestResourceRulesets(object):
    """A container for tests relating to Ruleset resources."""

    def test_get_ruleset_paths(self, standard_version_optional):
        """Check that all ruleset paths are found."""
        ruleset_paths = iati.resources.get_ruleset_paths(*standard_version_optional)

        assert len(ruleset_paths) == 1


class TestResourceSchemas(object):
    """A container for tests relating to Schema resources."""

    def test_get_activity_schema_paths(self, standard_version_optional):
        """Check that all activity schema paths are found.

        Todo:
            Handle all paths to schemas being found correctly.

        """
        activity_paths = iati.resources.get_activity_schema_paths(*standard_version_optional)

        assert len(activity_paths) == 1

    def test_get_organisation_schema_paths(self, standard_version_optional):
        """Check that all organisation schema paths are found.

        Todo:
            Handle all paths to schemas being found correctly.

        """
        organisation_paths = iati.resources.get_organisation_schema_paths(*standard_version_optional)

        assert len(organisation_paths) == 1

    def test_find_schema_paths(self, standard_version_optional):
        """Check that both the activity and organisation schema paths are being found.

        Todo:
            Handle all paths to schemas being found correctly.

        """
        paths = iati.resources.get_all_schema_paths(*standard_version_optional)

        assert len(paths) == 2

    @pytest.mark.parametrize('create_schema_path_function', [
        iati.resources.get_all_schema_paths,
        iati.resources.get_activity_schema_paths,
        iati.resources.get_organisation_schema_paths
    ])
    def test_find_schema_paths_file_extension(self, standard_version_optional, create_schema_path_function):
        """Check that the correct file extension is present within file paths returned by get_all_*schema_paths functions."""
        paths = create_schema_path_function(*standard_version_optional)

        for path in paths:
            assert path[-4:] == iati.resources.FILE_SCHEMA_EXTENSION

    def test_schema_activity_string(self):
        """Check that the Activity schema file contains content."""
        path = iati.resources.create_schema_path('iati-activities-schema')

        content = iati.utilities.load_as_string(path)

        assert len(content) > 125000

    def test_schema_activity_tree(self):
        """Check that the Activity schema loads into an XML Tree.

        This additionally involves checking that imported schemas also work.

        """
        path = iati.resources.create_schema_path('iati-activities-schema')
        schema = iati.utilities.load_as_tree(path)

        assert isinstance(schema, etree._ElementTree)  # pylint: disable=protected-access
