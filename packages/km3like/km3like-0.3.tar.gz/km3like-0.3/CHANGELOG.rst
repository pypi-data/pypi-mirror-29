Change Log
==========

Unreleased Changes
------------------

0.3 / 08/03/2018
----------------
* add pdf sampler
* namechange ``km3like.pseudo`` -> ``km3like.sample``
* Angular Resolution -> fits a parametric dist/nonparam histo in each 
  coszen, energy bin -> estimate uncertainty of an event, -> get random samples
  from the PSF to smear an event.

0.2.1 - 20/07/2017
------------------
* add BaseLLHNoExog and derive other pointsource classes from it
* add ScrambledBootstrap sampler (bootstrapped events + random azimuth/time)
