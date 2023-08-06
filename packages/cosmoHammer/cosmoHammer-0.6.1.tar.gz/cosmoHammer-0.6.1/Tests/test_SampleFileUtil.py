"""
Test the TestSampleFileUtil module.

Execute with py.test -v

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import tempfile
import os
import numpy

import pytest

import cosmoHammer.Constants as c
from cosmoHammer.util.SampleFileUtil import SampleFileUtil


@pytest.yield_fixture
def createFileUtil(tmpdir):
    tempPath = tmpdir.join("test").strpath
    fileUtil = SampleFileUtil(tempPath, True)
    yield fileUtil, tempPath
    fileUtil.finalize()


def test_not_master(tmpdir):
    fu = SampleFileUtil(tmpdir.strpath, False)
    fileList = tmpdir.listdir()  # os.listdir(tempPath)
    assert len(fileList) == 0
    fu.finalize()


def test_persistBurninValues(createFileUtil):
    fileUtil, tempPath = createFileUtil

    pos = numpy.ones((10, 5))
    prob = numpy.zeros(10)

    fileUtil.persistBurninValues(pos, prob, None)

    cPos = numpy.loadtxt(tempPath + c.BURNIN_SUFFIX)
    cProb = numpy.loadtxt(tempPath + c.BURNIN_PROB_SUFFIX)

    assert (pos == cPos).all()
    assert (prob == cProb).all()


def test_persistSamplingValues(createFileUtil):
    fileUtil, tempPath = createFileUtil

    pos = numpy.ones((10, 5))
    prob = numpy.zeros(10)

    fileUtil.persistSamplingValues(pos, prob, None)

    cPos = numpy.loadtxt(tempPath + c.FILE_SUFFIX)
    cProb = numpy.loadtxt(tempPath + c.PROB_SUFFIX)

    assert (pos == cPos).all()
    assert (prob == cProb).all()


def test_importFromFile(createFileUtil):
    fileUtil, tempPath = createFileUtil

    pos = numpy.ones((10, 5))
    prob = numpy.zeros(10)

    fileUtil.persistSamplingValues(pos, prob, None)

    cPos = fileUtil.importFromFile(tempPath + c.FILE_SUFFIX)
    cProb = fileUtil.importFromFile(tempPath + c.PROB_SUFFIX)

    assert (pos == cPos).all()
    assert (prob == cProb).all()


def test_storeRandomState(createFileUtil):
    fileUtil, tempPath = createFileUtil

    rstate = numpy.random.mtrand.RandomState()
    fileUtil.storeRandomState(tempPath + c.BURNIN_STATE_SUFFIX, rstate)

    cRstate = fileUtil.importRandomState(tempPath + c.BURNIN_STATE_SUFFIX)

    oState = rstate.get_state()
    nState = cRstate.get_state()

    assert oState[0] == nState[0]
    assert all(oState[1] == nState[1])
    assert oState[2] == nState[2]
    assert oState[3] == nState[3]
    assert oState[4] == nState[4]
