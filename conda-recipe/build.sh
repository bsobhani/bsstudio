echo "hello"
conda install --yes -c conda-forge/label/cf201901 pyqt
conda install --yes bluesky -c lightsource2-tag
$PYTHON setup.py install
