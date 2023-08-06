=========
imagecrop
=========
Image extraction using a template. Uses homography and feature matching,
storing results in a SQLite database in the user's home directory for faster reprocessing.

Usage
=====


.. code-block:: python

    from image_extract.extract import Extracter
    ex = Extracter()
    ex.crop_images(image_directory, crop_template, file_extension[, match_points])

Successful crops are extracted to a directory called ``successful_crops``,
directly underneath ``image_directory``. Each template used creates a subdirectory, named after its
md5 hash:

.. code::

    image_directory
        - img1.jpg
        - …
        - imgn.jpg
        - successful_crops
            - 2a1bdab44c5e81af34f47f3395a3da7e
                - img1_cropped.jpg

The optional ``match_points`` argument controls the number of matching points which must
be detected in order for a template match to be deemed successful. It's set to 30 by default.

Summaries
---------
Call ``ex.summary(path)`` to see information on extracted crops for a given directory.

Deleting Extracted Crops
------------------------
Call ``ex.delete(path[, template_md5])`` to delete extracted crops for a given template.
If no template md5 value is given, all extracted crops in that directory are removed.


Accuracy
========
For best results, the template image should be of the same (or similar) resolution
as the image from which the crop is to be extracted.


