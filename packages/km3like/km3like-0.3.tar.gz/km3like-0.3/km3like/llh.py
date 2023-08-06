"""Common Likelihoods.

All the heavy lifting is done by ``statsmodels`` + ``scipy.optimize``.
"""
import numpy as np
from statsmodels.base.model import GenericLikelihoodModel

# n_sig: param to be fitted
# variables which span llh space: alpha, energy
# additional params: n_bkg, signal_pdf, background_pdf


class BaseLLHNoExog(GenericLikelihoodModel):
    """Likelihood base class.

    The signal and background distributions need to be specified yet.

    Parameters:
        endog: list[arrays]
            collection of your data vectors on which the
            likelihood is evaluated (i.e. energy, distance to source),
        signal: callable
            Signal distribution
        background: callable
            Background distribution
    """
    def __init__(self, endog, exog=None, signal=None,
                 background=None, **kwds):
        """Don't care about exogenous variables, don't have them.

        ``endog`` is a collection of your data vectors on which the
        likelihood is evaluated (i.e. energy, distance to source),
        but not the parameter we would like to fit! (e.g. number of
        signal events).
        """
        if signal is not None:
            self.signal = signal
        if background is not None:
            self.background = background
        exog = np.zeros_like(endog)
        super(BaseLLHNoExog, self).__init__(endog=endog, exog=exog, **kwds)

    @classmethod
    def signal(cls, *args):
        """Signal distribution"""
        raise NotImplementedError

    @classmethod
    def background(cls, *args):
        """Background distribution"""
        raise NotImplementedError

    def nloglikeobs(self, params):
        endog = self.endog
        ll = self.nlnlike(params, endog)
        return ll

    def nlnlike(self, params, endog):
        """The actual likelihood, with parameter + data vectors.

        Implement this in your subclass.
        """
        raise NotImplementedError


class PointSourceStandardLLH(BaseLLHNoExog):
    """Point Source Standard Likelihood.

    The signal and background distributions need to be specified yet.

    Parameters:
        endog: list[arrays]
            collection of your data vectors on which the
            likelihood is evaluated (i.e. energy, distance to source),
        signal: callable
            Signal distribution
        background: callable
            Background distribution
    """
    def nlnlike(self, params, endog):
        """The standard Negative Log Likelihood."""
        n_sig = params[0]
        alpha, energy = endog

        n_tot = alpha.shape[0]

        sig = self.signal(alpha, energy)
        bkg = self.background(alpha, energy)
        nsumlogl = -np.sum(
            np.log(
                (n_sig / n_tot) * sig + ((n_tot - n_sig) / n_tot) * bkg
            )
        )
        return nsumlogl


class PointSourceExtendedLLH(BaseLLHNoExog):
    """Point Source Extended Likelihood.

    The signal and background distributions need to be specified yet.

    Parameters:
        endog: list[arrays]
            collection of your data vectors on which the
            likelihood is evaluated (i.e. energy, distance to source),
        n_bkg: integer, optional [default: 10000]
            Number of expected background events in sample.
        signal: callable
            Signal distribution
        background: callable
            Background distribution
    """
    def __init__(self, endog, n_bkg=10000, **kwds):
        """We need 1 additional parameter, the number of background events.
        """
        self.n_bkg = n_bkg
        super(PointSourceExtendedLLH, self).__init__(endog=endog, **kwds)

    def nlnlike(self, params, endog):
        """The extended Negative Log Likelihood."""
        n_sig = params[0]
        alpha, energy = endog
        n_tot = n_sig + self.n_bkg
        sig = self.signal(alpha, energy)
        bkg = self.background(alpha, energy)
        nsumlogl = -np.sum(
            np.log(
                n_sig * sig + self.n_bkg * bkg
            ) - n_tot - n_sig
        )
        return nsumlogl
