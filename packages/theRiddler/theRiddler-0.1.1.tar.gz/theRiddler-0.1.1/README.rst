The Riddler
===========

The Riddler is a project for learning purposes. 

It is a sample project made for
the upcoming lecture *Einfuehrung in Python* of the university *HTWG
Konstanz* at Constance, Germany.

It consists of riddles the solution of which preferably require learning Python
basics.
The riddles are intended to be solved programmatically, and most of them can
be solved by straightforward and short scripts.
The solution sometimes will require the use of extra modules, which can
all be downloaded from the internet.

The Riddler is designated to accompany the lecture and make the
students apply and consolidate their theoretical knowledge without
greater guidance and by play.
After mastering the first few riddles, the application leads to the
project itself and its distribution here on PyPI, and is then intended
to encourage the students to revise and modify, and finally republish it
for the following ones.

With this approach, the project is expected to result in the making of a sophisticated 
learning project, geared to the needs of the learners, and well tried and tested. 

Getting Started
---------------

At the beginning, the project is handed out to the students in the form
of an installer package (".msi"-file), for "mysterious" intentions.

Once they have solved the first riddles and end up here,
The Riddler shall be downloaded over its PyPI-Homepage and the downloaded File
has to be extracted. Subsequently it can be run by moving to the
extracted folder and typing ``python theriddler`` in the shell.

Installing with Pip
^^^^^^^^^^^^^^^^^^^

It is also possible to install this project with "Pip" from the shell by
typing ``pip install TheRiddler``, but it is not meant to be installed
this way for testing and development purposes.

Anyway, it could be started then by going into the directory where pip
installed it in, and by directly running the "__main__.py" script from
there.

Prerequisites
~~~~~~~~~~~~~

-	The "setup.py" script is yet built with `Setuptools <http://pypi.python.org/pypi/setuptools/>`_.

-	The `Pillow <http://pypi.python.org/pypi/Pillow/5.0.0/>`_ or "PIL" (Python Imaging Library) 
	module is used to display pictures, as the "PhotoImage" class from the built-in
	"Tkinter" module provides comparably lean functionalities.
	
-	To run tests, `Nose <http://pypi.python.org/pypi/nose/1.3.7/>`_ is required.

-	The  installer package handed out at the beginning is made with 
	`cx_Freeze <http://pypi.python.org/pypi/cx_Freeze/6.0b1>`_.
	Therefore, another "setup.py" script is used. 
	More information is provided in the attachment folder "misc" within the package.

- 	Some riddles require a valid connection to the internet. 
	The connection is accomplished with `certifi <http://pypi.python.org/pypi/certifi/2018.1.18>`_, 
	`beautifulsoup4 <http://pypi.python.org/pypi/beautifulsoup4/4.6.0>`_ and 
	`urllib3 <http://pypi.python.org/pypi/urllib3/1.22>`_.
	

Contributing
~~~~~~~~~~~~

Please read the **CONTRIBUTING** file from the "misc" folder for
details.

Versioning
~~~~~~~~~~

The versioning is intended to be made after "Semver". 
Check https://semver.org/.

The initial release was "theRiddler 0.1.0", 21th February 2018.

License
~~~~~~~

The entire content of this project is "self-made", pictures included.

The icon was created with a freeware version of "IcoFX" (v1.64).


The author waives any copyright for the content.

This project is licensed under the MIT License - see the **LICENSE**
file for details.

Author
~~~~~~

Etienne Martin,

student of the *HTWG Konstanz*, at the department of electrical
engineering.

This project is part of the bachelor thesis created to achieve the
bachelor of science degree.


Acknowledgments
~~~~~~~~~~~~~~~

-	The conception of this project was inspired by
	http://www.pythonchallenge.com/. Some riddles resemble an adaptation of the ones found 
	in the python challenge.

	Thanks to *Nadav Samet*, you can go visit his `blog <http://www.thesamet.com/>`_.
	"Because everyone needs a blog".

-	The "Gothon Trash Game" is an adaption and inspired by "Gothons from
	Planet Percal#25" from Zed Shaw's book "Learn Python the Hard Way",
	exercise 43.
	
