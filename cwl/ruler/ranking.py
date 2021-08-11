import numpy as np


class Ranking(object):

    def __init__(self, topic_id, gains, costs, max_gain=1.0, min_gain=0.0, max_cost=1.0, min_cost=1.0, max_n=1000):
        """
        The ranking object encapsulates the data about the items in the ranked list.
        The gains and costs vectors should only be accessed through the two getter methods
        as these will construct the list of gains and costs upto MAX_N and handle any unjudged items
        :param topic_id: a string to denote the topic
        :param gains: a vector of floats to represent the gain associated with each item in the list
        :param costs: a vector of floats to represent the cost of each item in the list
        :param max_gain: float that is greater than zero
        :param min_gain: float that is greater than zero
        :param max_cost: float that is greater than zero (and greater to or equal to min_cost)
        :param min_cost: float that is greater than zero (no free lunches)
        """
        self.topic_id = topic_id
        self._gains = gains
        self._costs = costs
        self.total_qrel_gain = 0.0
        self.total_qrel_rels = 0.0
        self.max_gain = max_gain
        self.min_gain = min_gain
        self.max_cost = max_cost
        self.min_cost = min_cost
        self.n = max_n
        # Calculates a lower bound on the total gain and total relevant items
        # For metrics like AP to be computed accurately, these values need to be
        # manually set after creating the ranking i.e. set w.r.t the QRELs file
        # As the QRELs file has all the KNOWN relevant items.
        for g in gains:
            if g > 0.0:
                self.total_qrel_gain += g
                self.total_qrel_rels += 1.0

    def get_gain_vector(self, worse_case=True):
        # pad out the vector to size n
        # convert all NaNs to min (worse case) or max (best case)
        if worse_case:
            gains = self._pad_trunc_vector(self._gains, self.n, self.min_gain)
            gains[np.isnan(gains)] = self.min_gain
            return gains
        else:
            gains = self._pad_trunc_vector(self._gains, self.n, self.max_gain)
            gains[np.isnan(gains)] = self.max_gain
            return gains

    def get_cost_vector(self, worse_case=True):
        # pad out the vector to size n
        # convert all NaNs to max (worse case) or min (best case)
        if worse_case:
            costs = self._pad_trunc_vector(self._costs, self.n, self.max_cost)
            costs[np.isnan(costs)] = self.max_cost
            return costs
        else:
            costs = self._pad_trunc_vector(self._costs, self.n, self.min_cost)
            costs[np.isnan(costs)] = self.min_cost
            return costs

    def get_total_gain(self, worse_case=True):
        if worse_case:
            return self.total_qrel_gain
        else:
            # return the max of self.total_qrel_gain
            return max(np.sum(self.get_gain_vector(worse_case)), self.total_qrel_gain)

    def get_total_cost(self, worse_case=True):
        return np.sum(self.get_cost_vector(worse_case))

    def get_total_rels(self, worse_case=True):
        if worse_case:
            return self.total_qrel_rels
        else:
            # return the max of self.total_qrel_rels
            gains = np.array(self.get_gain_vector(worse_case))
            # convert gain values to rel values
            gains[gains > 0.0] = 1.0
            return max(np.sum(gains), self.total_qrel_rels)

    def _pad_trunc_vector(self, vec1, n, val):
        """
        Pads vector 1 up to size n, with the value val
        :param vec1: np array
        :param n: size of the desired array
        :param val: the value to be inserted if padding is required
        :return: the padded vector
        """
        if len(vec1) < n:
            vec1 = np.pad(vec1, (0, n-len(vec1)), 'constant', constant_values=val)
        else:
            vec1 = vec1[0:n]
        return np.array(vec1)

    def report(self):
        if self.show_report:
            print("Topic: {0}".format(self.topic_id))
            print(self.topic_id, self.gains[:10])
            print(self.topic_id, self.costs[:10])


class RankingMaker(object):
    """
    This helper class builds Rankings
    """
    def __init__(self, topic_id, gain_handler, cost_dict=None, max_gain=1.0, min_gain=0.0, max_cost=1.0, min_cost=1.0, max_n=1000):
        """
        Iteratively builds up the ranked list of items (via the add function) then returns the final ranking
        by calling get_ranking
        :param topic_id: (string) represents the topic id - should match the topic id in the results file
        :param gain_handler: seeker.trec_qrel_handler.TrecQrelHandler
        :param cost_dict: a dictionary containing the element_type (key) and cost (float, value).
        :param max_gain: if an item is unjudged, when worse_case=False, then set gain to max_gain
        :param max_cost: if an item is unjudged, when worse_case=True, then set cost to max_cost
        :param min_cost: if an item is unjudged, when worse_case=False, then set the cost to min_cost
        """
        self.topic_id = topic_id
        self.gain_handler = gain_handler
        self.cost_lookup = cost_dict
        self.total_qrel_gain = 0.0
        self.total_qrel_rels = 0.0
        self._gains = []
        self._costs = []
        self.max_gain = max_gain
        self.min_gain = min_gain
        self.max_cost = max_cost
        self.min_cost = min_cost
        self.show_report = False
        self.max_n = max_n

    def add(self, doc_id, element_type):
        gain = self.gain_handler.get_value_if_exists(self.topic_id, doc_id)
        # if the item is not judged, then insert a NaN value for the gain
        # the Ranking object will resolve the NaN value as a min or max gain
        if gain is None:
            self._gains.append(np.nan)
        else:
            self._gains.append(gain)

        cost = self._get_cost(doc_id, element_type)
        self._costs.append(cost)

    def _get_cost(self, doc_id, element_type):
        """
        For a given document and element type returns the cost given the cost dictionary (cost_lookup)
        if no cost lookup exists or if the element is not in the dictionary, a nan value is assigned.
        :param doc_id: string
        :param element_type: string
        :return: return a float or nan value
        """
        if self.cost_lookup is None:
            return np.nan
        else:
            if element_type in self.cost_lookup:
                return self.cost_lookup[element_type]
            else:
                return np.nan

    def get_ranking(self):
        """
        Creates and returns a Ranking given the gains and costs added to the ranked lists.
        :return: ruler.ranking.Ranking
        """
        ranking = Ranking(self.topic_id, self._gains, self._costs, self.max_gain, self.min_gain, self.max_cost, self.min_cost, self.max_n)
        ranking.total_qrel_rels = self.gain_handler.get_total_rels(self.topic_id)
        ranking.total_qrel_gain = self.gain_handler.get_total_gains(self.topic_id)
        return ranking

    def report(self):
        if self.show_report:
            print("Topic: {0}".format(self.topic_id))
            print(self.topic_id, self.gains[:10])
            print(self.topic_id, self.costs[:10])
