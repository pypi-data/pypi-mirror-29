
Perseus Exercise Renderer for Kolibri
=====================================

What is Kolibri?
----------------

Kolibri is a Learning Management System / Learning App designed to run on low-power devices, targeting the needs of
learners and teachers in contexts with limited infrastructure. A user can install Kolibri and serve the app on a local
network, without an internet connection. Kolibri installations can be linked to one another, so that user data and
content can be shared. Users can create content for Kolibri and share it when there is network access to another
Kolibri installation or the internet.

See https://learningequality.org/kolibri/ for more info.

What is Perseus?
----------------

Khan Academy's exercise question editor and renderer.

See https://github.com/Khan/perseus for more info.

What is this plugin?
--------------------

A Perseus renderer wrapper for Kolibri that can track learning progress and save to the database.

How can I install this plugin?
------------------------------

1. Inside your Kolibri virtual environment:
    ``pip install kolibri-perseus-exercise-plugin``

2. Activate the plugin:

    ``kolibri plugin exercise_perseus_renderer enable``

3. Restart Kolibri.

How can I install this plugin for development?
------------------------------

1. Download this repo.

2. Open terminal in your Kolibri repo.

3. run the following commands:

    ``pip install -e <KOLIBRI-PERSEUS-PLUGIN-LOCAL-PATH>``

    ``kolibri plugin kolibri_exercise_perseus_plugin enable``

4. Then run the commands to install frontend packages in Kolibri, this plugin will have its dependencies recursively installed:

    ``yarn install``

5. Finally, to copy over Mathjax into the static folder, run the following command (you will need to do this if you update the version of Perseus in the repo also):

    ``./update_perseus.sh``

Updating translation strings
----------------------------

To download the latest translation strings for this plugin, make a `crowdinSecrets.js` file from the template in the repo root, and put your kolibri project API key in there. The KA API key can be set to null. Then execute the following commands:
    ``cd kolibri_exercise_perseus_plugin``
    ``yarn run download-translations``

Known issues
------------

If you ran `make dist` or `make pex` on Kolibri with `kolibri-exercise-perseus-plugin==x.x.x` present in `kolibri/requirements/base.txt`, Kolibri will generate a exercise_perseus_renderer instance inside its `dist` folder and use it afterwards. That means manually installing exercise_perseus_renderer for development won't take any effects. One way to fix this issue is to restore the `dist` folder.

How to publish to PyPi?
------------------------------

1. Follow the instructions above to installing the plugin for development.
2. From the Kolibri directory run the frontend build command.
3. update `setup.py` to a newer version.
4. Terminal move to the root level of repo dir and run the following command to publish to PyPi:

    ``make release``


How can I contribute?
---------------------

 * `Documentation <http://kolibri.readthedocs.org/en/latest/>`_ is available online, and in the ``docs/`` directory.
 * Mailing list: `Google groups <https://groups.google.com/a/learningequality.org/forum/#!forum/dev>`_.
 * IRC: #kolibri on Freenode
