conda install --yes sip=4.18.1
conda install --yes -c conda-forge/label/cf201901 pyqt
conda install --yes bluesky -c lightsource2-tag
cd ..
python setup.py install
