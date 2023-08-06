#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module is created for data processing framework,
to make rules for data saving, visualization issues, etc.
"""

try:
    import sdds
    SDDS_ = True
except:
    SDDS_ = False

import h5py
import numpy as np
import subprocess
import os


class DataExtracter(object):
    """ Extract required data from a SDDS formated file,
    to put into hdf5 formated file or just dump into RAM
    for post-processing.

    :param sddsfile: filename of SDDS data file
    :param kws: packed tuple/list options, usually sdds column names,
                e.g. ``('s', 'Sx')``

    :Example:

    >>> # *sddsquery -col* shows it has 's', 'Sx' data columns
    >>> sddsfile = 'output.sdds'
    >>> param_list = ('s', 'Sx')
    >>> dh = DataExtracter(sddsfile, *param_list)
    >>> # *dh* is a newly created DataExtracter instance

    ..    Author: Tong Zhang
    ..    Date  : 2016-03-10
    """
    def __init__(self, sddsfile, *kws):
        self.sddsfile = sddsfile
        self.kwslist = kws

        self.precision = '%.16e'
        self.dcmdline = 'sddsprintout {fn} -notitle -nolabel'.format(fn=self.sddsfile)

        self.h5data = ''

        if SDDS_:
            self.sddsobj = sdds.SDDS(1)
            self.sddsobj.load(self.sddsfile)

    def getAllCols(self, sddsfile=None):
        """ get all available column names from sddsfile

        :param sddsfile: sdds file name, if not given, rollback to the one that from ``__init__()``
        :return: all sdds data column names
        :rtype: list

        :Example:

        >>> dh = DataExtracter('test.out')
        >>> print(dh.getAllCols())
        ['x', 'xp', 'y', 'yp', 't', 'p', 'particleID']
        >>> print(dh.getAllCols('test.twi'))
        ['s', 'betax', 'alphax', 'psix', 'etax', 'etaxp', 'xAperture', 'betay', 'alphay', 'psiy', 'etay', 'etayp', 'yAperture', 'pCentral0', 'ElementName', 'ElementOccurence', 'ElementType']
        """
        if SDDS_:
            if sddsfile is not None:
                sddsobj = sdds.SDDS(2)
                sddsobj.load(sddsfile)
            else:
                sddsobj = self.sddsobj
            return sddsobj.columnName
        else:
            if sddsfile is None:
                sddsfile = self.sddsfile
            return subprocess.check_output(['sddsquery', '-col', sddsfile]).split()

    def getAllPars(self, sddsfile=None):
        """ get all available parameter names from sddsfile

        :param sddsfile: sdds file name, if not given, rollback to the one that from ``__init__()``
        :return: all sdds data parameter names
        :rtype: list

        .. warning:: `sdds` needs to be installed as an extra dependency.

        :Example:

        >>> dh = DataExtracter('test.w1')
        >>> print(dh.getAllPars())
        ['Step', 'pCentral', 'Charge', 'Particles', 'IDSlotsPerBunch', 'SVNVersion', 'Pass', 'PassLength', 'PassCentralTime', 'ElapsedCoreTime', 'MemoryUsage', 's', 'Description', 'PreviousElementName']

        :seealso: :func:`getAllCols`
        """
        if SDDS_:
            if sddsfile is not None:
                sddsobj = sdds.SDDS(2)
                sddsobj.load(sddsfile)
            else:
                sddsobj = self.sddsobj
            return sddsobj.parameterName
        else:
            if sddsfile is None:
                sddsfile = self.sddsfile
            return subprocess.check_output(['sddsquery', '-par', sddsfile]).split()

    def extractData(self):
        """ return `self` with extracted data as `numpy array`

        Extract the data of the columns and parameters of `self.kws` and put
        them in a :np:func:`array` with all columns as columns or parameters as
        columns. If columns and parameters are requested at the same then each column
        is one row and all parameters are in the last row. This
        :np:func:`array` is saved in ``h5data``.

        .. note::
            If you mix types (e. g. float and str) then the minimal fitting type is
            taken for all columns.

        .. warning:: Non float types need `sdds` as an extra dependency

        :return: instance of itself

        :Example:

        One column of the watch element
        >>> dh = DataExtracter('test.w1')
        >>> dh.kwslist = ['Step']
        >>> print(dh.extractData().h5data)
        array([[1]])

        Two columns of the watch element
        >>> dh = DataExtracter('test.w1')
        >>> dh.kwslist = ['s', 'betax']
        >>> print(dh.extractData().h5data)
        array([[0, 1], [1, 2], [2, 1]])

        Two columns of the watch element and one parameter.
        The columns transform to rows and the parameter row is at the end.
        Furthermore all elements are strings, because the type of
        `PreviousElementName` is str and not float.
        >>> dh = DataExtracter('test.w1')
        >>> dh.kwslist = ['s', 'PreviousElementName', 'betax']
        >>> print(dh.extractData().h5data)
        array([['0', '1', '2'], ['1', '2', '1'], ['DR01']])
        """
        if SDDS_:
            columns = self.sddsobj.columnName
            parameters = self.sddsobj.parameterName
            data = [self.sddsobj.columnData[columns.index(col)][0]
                    for col in self.kwslist if col in columns]
            data.append([self.sddsobj.parameterData[parameters.index(par)][0]
                        for par in self.kwslist if par in parameters])
            self.h5data = np.array(filter(None, data)).T
        else:
            for k in self.kwslist:
                self.dcmdline += ' -col={kw},format={p}'.format(kw=k, p=self.precision)
            cmdlist = ['bash', self.dscript, self.dpath, self.dcmdline]
            retlist = []
            proc = subprocess.Popen(cmdlist, stdout=subprocess.PIPE)
            for line in proc.stdout:
                retlist.append([float(i) for i in line.split()])
            self.h5data = np.array(retlist)
        return self

    def getH5Data(self):
        """ return extracted data as numpy array

        :return: numpy array after executing ``extractData()``
        """
        return self.h5data

    def getKws(self):
        """ return data column fields that defined in constructor, e.g. ``('s', 'Sx')``

        :return: data columns keyword
        :rtype: tuple
        """
        return self.kwslist

    def setDataScript(self, fullscriptpath='sddsprintdata.sh'):
        """ configure script that should be utilized by DataExtracter,
        to extract data colums from sddsfile.

        :param fullscriptpath: full path of script that handles the data extraction of sddsfile,
                               default value is ``sddsprintdata.sh``, which is a script that distributed
                               with ``beamline`` package.
        :return: None
        """

        self.dscript = os.path.expanduser(fullscriptpath)

    def setDataPath(self, path):
        """ set full dir path of data files

        :param path: data path, usually is the directory where numerical simulation was taken place
        :return: None
        """
        self.dpath = os.path.expanduser(path)

    def setH5file(self, h5filepath):
        """ set h5file full path name

        :param h5filepath: path for hdf5 file
        :return: None
        """
        self.h5file = os.path.expanduser(h5filepath)

    def setKws(self, *kws):
        """ set keyword list, i.e. sdds field names, update ``kwslist`` property

        :param kws: packed tuple of sdds datafile column names
        :return None:
        """
        self.kwslist = kws

    def dump(self):
        """ dump extracted data into a single hdf5file,

        :return: None
        :Example:


        >>> # dump data into an hdf5 formated file
        >>> datafields = ['s', 'Sx', 'Sy', 'enx', 'eny']
        >>> datascript = 'sddsprintdata.sh'
        >>> datapath   = './tests/tracking'
        >>> hdf5file   = './tests/tracking/test.h5'
        >>> A = DataExtracter('test.sig', *datafields)
        >>> A.setDataScript(datascript)
        >>> A.setDataPath  (datapath)
        >>> A.setH5file    (hdf5file)
        >>> A.extractData().dump()
        >>>
        >>> # read dumped file
        >>> fd = h5py.File(hdf5file, 'r')
        >>> d_s  = fd['s'][:]
        >>> d_sx = fd['Sx'][:]
        >>>
        >>> # plot dumped data
        >>> import matplotlib.pyplot as plt
        >>> plt.figure(1)
        >>> plt.plot(d_s, d_sx, 'r-')
        >>> plt.xlabel('$s$')
        >>> plt.ylabel('$\sigma_x$')
        >>> plt.show()

        Just like the following figure shows:

        .. image:: ../../images/test_DataExtracter.png
            :width: 400px

        """
        f = h5py.File(self.h5file, 'w')
        for i, k in enumerate(self.kwslist):
            v = self.h5data[:, i]
            dset = f.create_dataset(k, shape=v.shape, dtype=v.dtype)
            dset[...] = v
        f.close()


class DataVisualizer(object):
    """ for data visualization purposes, to be implemented

    .. Author: Tong Zhang
    .. Date  : 2016-03-14
    """
    def __init__(self, data):
        self.data = data

    def inspectDataFile(self):
        """ inspect hdf5 data file
        """
        pass

    def illustrate(self, xlabel, ylabel):
        """ plot x, y w.r.t. xlabel and ylabel
        :param ylabel: xlabel
        :param xlabel: ylabel
        """
        pass

    def saveArtwork(self, name='image', fmt='jpg'):
        """ save figure by default name of image.jpg
        :param name: image name, 'image' by default
        :param fmt: image format, 'jpg' by default
        """
        pass


class DataStorage(object):
    """ for data storage management, to be implemented.
        communicate with database like mongodb, mysql, sqlite, etc.

    .. Author: Tong Zhang
    .. Date  : 2016-03-14
    """
    def __init__(self, data):
        self.data = data

    def configDatabase(self):
        """ configure database
        """
        pass

    def putData(self):
        """ put data into database
        """
        pass

    def getData(self):
        """ get data from database
        """
        pass

#--------------------------------------------------------------------------------------


def test():
    # workflow
    datafields = ['s', 'Sx', 'Sy', 'enx', 'eny']
    datascript = '~/Programming/projects/beamline/scripts/sddsprintdata.sh'
    datapath   = '~/Programming/projects/beamline/tests/tracking'
    hdf5file   = os.path.join(os.path.expanduser(datapath), 'test.h5')
    A = DataExtracter('test.sig', *datafields)
    A.setDataScript(datascript)
    A.setDataPath  (datapath)
    A.setH5file    (hdf5file)
    A.extractData().dump()

    fd = h5py.File(hdf5file, 'r')
    d_s  = fd['s'][:]
    d_sx = fd['Sx'][:]

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.plot(d_s, d_sx, 'r-')
    plt.xlabel('$s$')
    plt.ylabel('$\sigma_x$')
    plt.show()

if __name__ == '__main__':
    test()


