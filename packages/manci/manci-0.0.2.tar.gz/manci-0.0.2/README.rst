
.. code-block:: bash
    lb-run LHCbDIRAC/prod bash --norc
    lhcb-proxy-init
    python -m pip install --user manci
    python -m manci mirror --ganga-jid 5 --mirror-dir root://eoslhcb.cern.ch//eos/lhcb/user/c/cburr/test/
    python -m manci merge --ganga-jid 5 --merged-fn root://eoslhcb.cern.ch//eos/lhcb/user/c/cburr/test.root
    python -m manci merge --merged-fn root://eoslhcb.cern.ch//eos/lhcb/user/c/cburr/test.root --lfns \
        /lhcb/user/c/cburr/d2hll/v7/2016-MC-MagDown-23722012/5_1/2018_02/198894/198894673/Charm_D2hll_DVntuple.root \
        /lhcb/user/c/cburr/d2hll/v7/2016-MC-MagDown-23722012/5_0/2018_02/198894/198894670/Charm_D2hll_DVntuple.root
