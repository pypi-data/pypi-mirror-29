#!/usr/bin/env python
"""Data loading utilities, e.g. DM spectra, Source morphologies.
"""

import os.path

import h5py
import pandas as pd

import km3pipe as kp
import km3like
from km3flux.data import dm_gc_spectrum     # noqa


DATADIR = os.path.dirname(km3like.__file__) + '/data/'
MORPHDIR = DATADIR + 'morph'
MASSES = {'100000', '260', '100', '5000', '360', '200', '10', '1000', '750',
          '30000', '2000', '50', '10000', '180', '500', '150', '3000', '25',
          '90', '1500'}
FLAVORS = {'anu_mu', 'nu_mu'}
CHANNELS = {'b', 'mu', 'tau', 'w'}


def gc_morph(morph='nfw_new', full_lims=False):
    if morph not in {'nfw_new', 'burkert', 'einasto'}:
        raise KeyError("Unkown moprphology '{}'".format(morph))
    fname = MORPHDIR + '/' + morph + '.h5'
    with h5py.File(fname, 'r') as h5:
        counts = h5['bincontent'][:]
        bins = h5['binlims'][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins


def add_flavor(df):
    def t2f(row):
        return kp.mc.pdg2name(row['type'])

    flavor = df.apply(t2f, axis=1).astype('str')
    return flavor


def load_data(fname='track_sample.h5'):
    with pd.HDFStore(fname, 'r') as h5:
        #X = h5['reco']
        X = h5['rec']
        mc = h5['mc']
    return X, mc


def load_and_cut_sample(fname='/home/moritz/ya/jupy/km3/track_sample.h5',
                        cut=False, qualcut=None, bjymax=0.5, qualmin=-5, maxbeta=3,):
    X, mc = load_data(fname)
    if qualcut is None:
        qualcut = '(recolns_bjorken_y < @bjymax) & (recolns_quality > @qualmin) & (recolns_energy_neutrino > 0) & (recolns_beta < @maxbeta)'
    if cut:
        mask = X.eval(qualcut)
        X = X[mask]
        mc = mc[mask]
    return X, mc
