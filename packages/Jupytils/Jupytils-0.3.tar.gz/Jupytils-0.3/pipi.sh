PWD=`pwd`
export CPKG=`basename $PWD`
export CPKG=Jupytils
echo "NAME $CPKG ..."
pip uninstall --yes $CPKG
pip install .
