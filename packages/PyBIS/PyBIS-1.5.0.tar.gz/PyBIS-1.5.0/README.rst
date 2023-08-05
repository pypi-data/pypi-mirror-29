Welcome to pyBIS!
=================

pyBIS is a Python module for interacting with openBIS, designed to be
used in Jupyter. It offers a sort of IDE for openBIS, supporting TAB
completition and input checks, making the life of a researcher hopefully
easier.

SYNOPSIS
========

connecting to OpenBIS
---------------------

::

    from pybis import Openbis
    o = Openbis('https://example.com:8443', verify_certificates=False)
    o.login('username', 'password', save_token=True)   # saves the session token in ~/.pybis/example.com.token
    o.token
    o.is_session_active()
    o.get_datastores()
    o.logout()

Masterdata
----------

::

    o.get_experiment_types()
    o.get_sample_types()
    o.get_sample_type('YEAST')
    o.get_material_types()
    o.get_dataset_types()
    o.get_dataset_types()[0]
    o.get_dataset_type('RAW_DATA')
    o.get_terms()
    o.get_terms('MATING_TYPE')
    o.get_tags()

Spaces
------

::

    space = o.new_space(code='space_name', description='')
    space.save()
    space.delete('reason for deletion')
    o.get_spaces()
    o.get_space('MY_SPACE')

Projects
--------

::

    project = o.new_project(
        space=space, 
        code='project_name',
        description='some project description'
    )
    project = space.new_project( code='project_code', description='project description')
    project.save()

    o.get_projects()
    o.get_projects(space='MY_SPACE')
    space.get_projects()

    project.get_experiments()
    project.get_attachments()
    p.add_attachment(fileName='testfile', description= 'another file', title= 'one more attachment')
    project.download_attachments()

Samples
-------

Samples are nowadays called **Objects** in openBIS. pyBIS is not yet
thoroughly supporting this term in all methods where «sample» occurs.

::

    sample = o.new_sample(
        type='YEAST', 
        space='MY_SPACE', 
        parents=[parent_sample, '/MY_SPACE/YEA66'], 
        children=[child_sample]
    )
    sample = space.new_sample( type='YEAST' )
    sample.save()

    sample = o.get_sample('/MY_SPACE/MY_SAMPLE_CODE')
    sample = o.get_sample('20170518112808649-52')

    sample.space
    sample.code
    sample.permId
    sample.identifier
    sample.type  # once the sample type is defined, you cannot modify it
    sample.space
    sample.space = 'MY_OTHER_SPACE'
    sample.experiment    # a sample can belong to one experiment only
    sample.experiment = 'MY_SPACE/MY_PROJECT/MY_EXPERIMENT'
    sample.tags
    sample.tags = ['guten_tag', 'zahl_tag' ]
    sample.get_parents()
    sample.parents = ['/MY_SPACE/PARENT_SAMPLE_NAME']
    sample.add_parents('/MY_SPACE/PARENT_SAMPLE_NAME')
    sample.del_parents('/MY_SPACE/PARENT_SAMPLE_NAME')

    sample.get_childeren()
    sample.children = ['/MY_SPACE/CHILD_SAMPLE_NAME']
    sample.add_children('/MY_SPACE/CHILD_SAMPLE_NAME')
    sample.del_children('/MY_SPACE/CHILD_SAMPLE_NAME')
    sample.get_childeren()

    sample.props
    sample.p                              # same thing as .props
    sample.p.my_property = "some value"   # set the value of a property (value is checked)
    sample.p + TAB                        # in IPython or Jupyter: show list of available properties
    sample.p.my_property_ + TAB           # in IPython or Jupyter: show datatype or controlled vocabulary

    sample.get_attachments()
    sample.download_attachments()
    sample.add_attachment('testfile.xls')

    samples = o.get_samples(
        space='MY_SPACE',
        type='YEAST',
        tags=['*'],                          # tags must be present
        NAME = 'some name',                  # properties are always uppercase to distinguish them from attributes
        **{ "SOME.WEIRD:PROPERTY": "value"}  # in case your property name contains a dot or a colon which cannot be passed as an argument name 
        props=['NAME', 'MATING_TYPE','SHOW_IN_PROJECT_OVERVIEW'] # show these properties in the results
    )
    samples.df                            # returns a pandas dataframe object
    samples.get_datasets(type='ANALYZED_DATA')

Note: Project samples are not implemented yet.

Experiments
-----------

::

    o.new_experiment
        type='DEFAULT_EXPERIMENT',
        space='MY_SPACE',
        project='YEASTS'
    )
    o.get_experiments(
        project='YEASTS',
        space='MY_SPACE', 
        type='DEFAULT_EXPERIMENT',
        tags='*', 
        finished_flag=False,
        props=['name', 'finished_flag']
    )
    exp = o.get_experiment('/MY_SPACE/MY_PROJECT/MY_EXPERIMENT')

    exp.props
    exp.p                              # same thing as .props
    exp.p.finished_flag=True
    exp.p.my_property = "some value"   # set the value of a property (value is checked)
    exp.p + TAB                        # in IPython or Jupyter: show list of available properties
    exp.p.my_property_ + TAB           # in IPython or Jupyter: show datatype or controlled vocabulary

    exp.attrs
    exp.a     # same as exp.attrs
    exp.attrs.tags = ['some', 'extra', 'tags']
    exp.tags = ['some', 'extra', 'tags']          # same thing
    exp.save()

Datasets
--------

::

    sample.get_datasets()
    ds = o.get_dataset('20160719143426517-259')
    ds.get_parents()
    ds.get_children()
    sample = ds.sample
    experiment = ds.experiment
    ds.physicalData
    ds.status        # AVAILABLE LOCKED ARCHIVED UNARCHIVE_PENDING ARCHIVE_PENDING BACKUP_PENDING
    ds.archive()
    ds.unarchive()
    ds.get_files(start_folder="/")
    ds.file_list
    ds.add_attachment()
    ds.get_attachments()
    ds.download_attachments()
    ds.download(destination='/tmp', wait_until_finished=False)

    ds_new = o.new_dataset(
        type='ANALYZED_DATA', 
        experiment=exp, 
        sample= samp,
        files = ['my_analyzed_data.dat'], 
        props={'name': 'we give this dataset a name', 'notes': 'and we might need some notes, too'})
    )
    ds_new.save()

    ds.props
    ds.p                              # same thing as .props
    ds.p.my_property = "some value"   # set the value of a property (value is checked)
    ds.p + TAB                        # in IPython or Jupyter: show list of available properties
    ds.p.my_property_ + TAB           # in IPython or Jupyter: show datatype or controlled vocabulary

    # complex query with chaining. props adds a "name" column. To filter for some property, the name of the property must be in UPPERCASE
    datasets = o.get_experiments(project='YEASTS').get_samples(type='FLY').get_datasets(type='ANALYZED_DATA', props=['MY_PROPERTY'],MY_PROPERTY='some analyzed data')

    # another example
    datasets = o.get_experiment('/MY_NEW_SPACE/VERMEUL_PROJECT/MY_EXPERIMENT4').get_samples(type='UNKNOWN').get_parents().get_datasets(type='RAW_DATA')

    # get a pandas dataFrame object
    datasets.df

    # use it in a for-loop:
    for dataset in datasets:
        print(ds.permID)

Semantic Annotations
--------------------

::

    # create semantic annotation for sample type (predicate and descriptor values omitted for brevity)
    sa = o.new_semantic_annotation(entityType = 'UNKNOWN')
    sa.save()

    # create semantic annotation for property type (predicate and descriptor values omitted for brevity)
    sa = o.new_semantic_annotation(propertyType = 'DESCRIPTION')
    sa.save()

    # create semantic annotation for sample property assignment (predicate and descriptor values omitted for brevity)
    sa = o.new_semantic_annotation(entityType = 'UNKNOWN', propertyType = 'DESCRIPTION')
    sa.save()

    # create semantic annotation with additional fields
    sa = o.new_semantic_annotation(entityType = 'UNKNOWN',
                          predicateOntologyId = 'po_id',
                          predicateOntologyVersion = 'po_version',
                          predicateAccessionId = 'pa_id',
                          descriptorOntologyId = 'do_id',
                          descriptorOntologyVersion = 'do_version',
                          descriptorAccessionId = 'da_id')
    sa.save()

    # get all semantic annotations
    o.get_semantic_annotations()

    # get semantic annotation by perm id
    sa = o.get_semantic_annotation("20171015135637955-30")

    # update semantic annotation
    sa.predicateOntologyId = 'new_po_id'
    sa.descriptorOntologyId = 'new_do_id'
    sa.save()

    # delete semantic annotation
    sa.delete('reason')

Requirements and organization
=============================

Dependencies and Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  pyBIS relies the openBIS API v3; openBIS version 16.05.2 or newer
-  pyBIS uses Python 3.3 and pandas
-  pyBIS needs the jupyter-api to be installed, in order to register new
   datasets

Installation
~~~~~~~~~~~~

-  locate the ``jupyter-api`` folder found in ``pybis/src/coreplugins``
-  copy this folder to ``openbis/servers/core-plugins`` in your openBIS
   installation
-  register the plugin by editing
   ``openbis/servers/core-plugins/core-plugins.properties`` :
-  ``enabled-modules = jupyter-api`` (separate multiple plugins with
   comma)
-  restart your DSS to activate the plugin

Project Organization
~~~~~~~~~~~~~~~~~~~~

This project is devided in several parts:

-  src/python/\ **PyBis** Python module which holds all the method to
   interact with OpenBIS
-  src/python/\ **OBis** a command-line tool to register large datasets
   in OpenBIS without actually copying the data. Uses git annex for
   version control and OpenBIS linkedDataSet objects to register the
   metadata.
-  src/python/\ **JupyterBis** a JupyterHub authenticator module which
   uses pyBIS for authenticating against openBIS, validating and storing
   the session token
-  src/core-plugins/\ **jupyter-api**, an ingestion plug-in for openBIS,
   allowing people to upload new datasets
-  src/vagrant/\ **jupyter-bis/Vagrantfile** to set up JupyterHub on a
   virtual machine (CentOS 7), which uses the JupyterBis authenticator
   module
-  src/vagrant/\ **obis/Vagrantfile** to set up a complete OpenBIS
   instance on a virtual machine (CentOS 7)
-  
