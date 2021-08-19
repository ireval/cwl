import math
import numpy as np
import logging

logger = logging.getLogger('cwl')

class CWLMetric(object):

    def __init__(self):
        self.expected_utility = 0.0
        self.expected_cost = 0.0
        self.expected_total_utility = 0.0
        self.expected_total_cost = 0.0
        self.expected_items = 0.0
        self.residual_expected_utility = None
        self.residual_expected_cost = None
        self.residual_expected_total_utility = None
        self.residual_expected_total_cost = None
        self.residual_expected_items = None
        self.residuals = False
        self.metric_name = "Undefined"
        self.ranking = None
        self.bibtex = ""

    def name(self):
        return self.metric_name

    def c_vector(self, ranking, worse_case=True):
        """
        Create a vector of C probabilities (i.e. probability of continuing from position i to position i+1)
        Note: when defining a metric is best/easiest to re-implement this function.
        :param ranking: CWL Ranking object
        :param worse_case: Boolean, to denote whether to estimate based on assuming the
            worse case i.e. unjudged are considered to be zero gain, and max cost or
            best case i.e. worse_case=False, and unjudged are considered to be max gain, and min cost
            Note that the Ranking object handles what is returned in the gain and cost vectors.
        :return: returns the C vector probabilities
        """
        cvec = np.ones(len(ranking.get_gain_vector(worse_case)))
        return cvec

    def l_vector(self, ranking, worse_case=True):
        """
        Create a vector of L probabilities (i.e. the Likelihoods of stopping at position i given the C vector)
        :param ranking: CWL Ranking object
        :param worse_case: Boolean, to denote whether to estimate based on assuming the
        :return: returns the L vector probabilities
        """
        cvec = self.c_vector(ranking, worse_case)
        logger.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "cvec", cvec[0:11]))
        cshift = np.append(np.array([1.0]), cvec[0:-1])
        lvec = np.cumprod(cshift)
        lvec = np.multiply(lvec, (np.subtract(np.ones(len(cvec)), cvec)))
        logger.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "lvec", lvec[0:11]))
        return lvec

    def w_vector(self, ranking, worse_case=True):
        """
        Create a vector of E probabilities (i.e. probability of examining item i)
        Note: when defining a metric is best/easiest to re-implement this function.
        :param ranking: CWL Ranking object
        :param worse_case: Boolean, to denote whether to estimate based on assuming the
        :return: returns the W vector probabilities
        """
        cvec = self.c_vector(ranking, worse_case)
        cvec = cvec[0:-1]
        cvec_prod = np.cumprod(cvec)
        cvec_prod = np.pad(cvec_prod, (1, 0), 'constant', constant_values=1.0)
        w1 = np.divide(1.0, np.sum(cvec_prod))
        w_tail = np.multiply(cvec_prod[1:len(cvec_prod)], w1)
        wvec = np.append(w1, w_tail)
        logger.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "wvec", wvec[0:11]))
        return wvec

    def measure(self, ranking):
        """
        Given the ranking, measure estimates the various measurements given the CWL framework
        if residuals are required, these are also computed.
        :param ranking: CWL Ranking object
        :return: the expected utility per item
        """
        self.ranking = ranking
        # score based on worse case - lower bounds
        (eu, etu, ec, etc, ei) = self._do_score(ranking, True)

        self.expected_utility = eu
        self.expected_total_utility = etu
        self.expected_cost = ec
        self.expected_total_cost = etc
        self.expected_items = ei

        if self.residuals:
            # score based on best case - upper bounds
            (eu, etu, ec, etc, ei) = self._do_score(ranking, False)

            # compute the residual i.e. the difference between the upper and lower bounds
            self.residual_expected_utility = eu - self.expected_utility
            self.residual_expected_total_utility = etu - self.expected_total_utility
            self.residual_expected_cost = ec - self.expected_cost
            self.residual_expected_total_cost = etc - self.expected_total_cost
            self.residual_expected_items = ei - self.expected_items

        # return the rate of gain per document
        return self.expected_utility

    def _do_score(self, ranking, worse_case=True):
        """
        An internal function that handles the scoring of a ranking given the CWL machinery.
        :param ranking: CWL Ranking object
        :return: the expected utility per item
        :return: returns the expected utility per item, etc..
        """
        wvec = self.w_vector(ranking, worse_case)
        lvec = self.l_vector(ranking, worse_case)
        gain_vec = ranking.get_gain_vector(worse_case)
        cost_vec = ranking.get_cost_vector(worse_case)
        cum_gains = np.cumsum(gain_vec)
        cum_costs = np.cumsum(cost_vec)
        expected_utility = np.sum(np.dot(wvec, gain_vec))
        expected_total_utility = np.sum(np.dot(lvec, cum_gains))
        expected_cost = np.sum(np.dot(wvec, cost_vec))
        expected_total_cost = np.sum(np.dot(lvec, cum_costs))
        expected_items = 1.0 / wvec[0]
        return expected_utility, expected_total_utility, expected_cost, expected_total_cost, expected_items

    def report(self):
        if self.residuals:
            print("{0}\t{1}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}\t{7:.4f}\t{8:.4f}\t{9:.4f}\t{10:.4f}\t{11:.4f}".format(
                self.ranking.topic_id, self.name(), self.expected_utility, self.expected_total_utility,
                self.expected_cost, self.expected_total_cost, self.expected_items,
                self.residual_expected_utility, self.residual_expected_total_utility,
                self.residual_expected_cost, self.residual_expected_total_cost, self.residual_expected_items
            ))
        else:
            print("{0}\t{1}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}".format(
                self.ranking.topic_id, self.name(), self.expected_utility, self.expected_total_utility,
                self.expected_cost, self.expected_total_cost, self.expected_items,
            ))

    def csv(self):
        return ("{0},{1:.3f},{2:.3f},{3:.3f},{4:.3f},{5:.3f}".format(
            self.name(), self.expected_utility, self.expected_total_utility, self.expected_cost,
            self.expected_total_cost, self.expected_items))

    def get_scores(self):
        """
        :return: list with values of each measurement for the previously measured ranking
        """
        scores = [
         self.expected_utility,
         self.expected_total_utility,
         self.expected_cost,
         self.expected_total_cost,
         self.expected_items]
        return scores

    def _pad_vector(self, vec1, n, val):
        """
        Pads vector 1 up to size n, with the value val
        :param vec1: np array
        :param n: size of the desired array
        :param val: the value to be inserted if padding is required
        :return: the padded vector
        """
        if len(vec1) < n:
            vec1 = np.pad(vec1, (0, n-len(vec1)), 'constant', constant_values=val)
        return vec1

    def validate_gain_range(self, min_allowed_gain, max_allowed_gain, gain_vec):
        """
        Checks that the gain vector does not violate any metric assumptions
        These assumptions (about the min or max gain) should be provided by
        the calling metric class.
        """
        if np.min(gain_vec) < min_allowed_gain:
            raise ValueError("Supplied gain values violate metric assumptions: Metric = {}.\n "
                             "The minimum allowable gain for this metric is: {}.".format(self.name(), min_allowed_gain))
        if np.max(gain_vec) > max_allowed_gain:
            raise ValueError("Supplied gain values ({}) violate metric assumptions: Metric = {}.\n "
                             "The maximum allowable gain for this "
                             "metric is: {}.".format(np.max(gain_vec), self.name(), max_allowed_gain))


