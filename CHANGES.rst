Change Log SenSE
====================

[1.0.0] - 2026-04-01
--------------------

Added
~~~~~~
* **CI/CD Improvements:** Added GitHub workflows specifically designed for updating
  the JOSS (Journal of Open Source Software) paper version.

Changed
~~~~~~~
* **Containerization:** Improved and updated the Docker container installation process.
* **Documentation:** Refactored user notebooks to better showcase specific use cases
  and practical applications.
* **Dependency Management:**
     * Split requirements files between core dependencies (for the Python package) 
       and additional dependencies (for Jupyter notebooks and ReadTheDocs).
     * Swapped the ``matplotlib`` Conda dependency for the lighter ``matplotlib-base``.
* **Code Architecture:** 
     * Major internal refactor: Rewrote core object classes to utilize 
       Python ``DataClasses`` for better efficiency and readability.
     * General code maintenance using Ruff rules.


Updated
~~~~~~~~
* **JOSS Paper:** Updated the initial JOSS paper version.
* **ReadTheDocs:** Updated the ReadTheDocs documentation.

Removed
~~~~~~~~
* **Cleanup:** Removed obsolete Python packages that are no longer required 
  (e.g., ``anyio``, ``future``).



[0.2] - 2024-10-12
-------------------

Added
~~~~~~~
* Docker installation option
* Jupyter Notebooks
* Github Workflows

Changed
~~~~~~~~
* Installation process (python setup.py install deprecated)
* Documentation
     * update installation
     * update Usage
     * update Theory

[0.1] - 2023-02-13
-------------------
initial version

