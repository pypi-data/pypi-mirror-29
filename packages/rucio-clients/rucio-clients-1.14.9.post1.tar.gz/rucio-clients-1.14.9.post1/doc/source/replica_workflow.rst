Typical replica workflow
========================

This section gives an overview of what happens within Rucio, for a typical replica workflow. Two workflows are described:
When a replica is uploaded to Rucio via a client and when a replica is created by a
site to site transfer due to the creation of a `replication rule`_.


Replica pathes on storage
^^^^^^^^^^^^^^^^^^^^^^^^^

Rucio has two basic paradigms in deciding the path for a replica on a specific storage system. **Deterministic** and **Non-deterministic** pathes. If we assume
a file whose data identifier is ``user.jdoe:test.file.1``, thus the scope is ``user.jdoe`` and the name is ``test.file.1``. In Rucio a deterministcally created path is a path
which can be generated soley knowing the scope and name of a data identifier (Ignoring the static prefix of the storage endpoint). For a non-deterministic path
additional information describing the file is necessary, such as meta-data, the dataset the file belongs to, etc.

Rucio supports plugable algorithms for both deterministic and non-deterministic algorithms. This section explains a few of them.

Deterministc algorithm based on hashes
--------------------------------------

The hash deterministc algorithm is an algorithm commonly used in Rucio. The advantage of this algorithm is that, due to the characteristics of cryptographic hash functions,
that the files are evenly distributed to directories. This can be an important characteristic for storage systems whose access performance degrades based on the number
of files in a directory.

Based on the data identifier, e.g. ``user.jdoe:test.file.1`` a md5-hashsum is calculated ``077c8119053bebb168d125034bff64ac``. The generated path is then based on the first four
characters of the hashsum. e.g. ``/07/7c/user.jdoe/test.file.1``.


Deterministic algorithm based on naming convention
--------------------------------------------------

If a specific naming convention is enforced on the filenames, a possible deterministic algorithm can be based on it.

E.g. based on the data identifier ``user.jdoe:test.file.1`` the first part of the filename (``test``) is exctracted and used to generate the path: ``/test/user.jdoe/file.1``


Non-Deterministc algorithm based on parent dataset
--------------------------------------------------

If the file is part of a datasets, e.g. ``data:dataset1234`` the dataset can be used in the path of the filename. This is useful for e.g. tape storage systems, to keep the files belonging to the same dataset on the same tape.

E.g. based on the data identifier ``user.jdoe:test.file.1`` which is part of the datset ``data:dataset1234`` the generated path is: ``/data/dataset1234/user.jdoe/test.file.1``


Replica is uploaded with the command line client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a typical workflow when a user uploads multiple files, which are part of a dataset, via the command line client.

1. The dataset ``test.dataset`` is being registered at the server.
   All files, or datasets are being put in a `scope`_, if not specifically mentioned the client will assume the default scope of the user,
   such as ``user.jdoe``. Thus the full data identifier for the dataset is ``user.jdoe:test.dataset``.

2. The client queries the RSE information from the server. This not only gives a list of prioritized write protocols to use but also the information
   if the RSE is a deterministic or non-deterministic one.

3. The file replica is registered as ``COPYING`` on the RSE.
   
4. Based on the identified naming algorithm of the RSE and the list of prioritized write protocols, the file URL is calculated.
   ``https://storageserver.organization.org/VO/data/07/7c/user.jdoe/test.file.1``

5. The file upload is done with the first priritized protocol. If the upload fails, step 4 is repeated with the second prioritized protocol, etc.

6. Once the upload is successfully finished, the replica state is changed to ``OK``.

7. Step 3-6 are repeated (done in parallel) with all other files part of the uploaded dataset.


Replica is created by a replication rule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^





.. _replication rule: overview_Replica_management.html
.. _scope: overview_File_Dataset_Container.html
