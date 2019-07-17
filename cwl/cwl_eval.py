#!/usr/bin/env python.
"""
cwl_eval tool for information retrieval evaluation of TREC formated results
"""

__author__ = 'leifos'
__credits__ = ['InProceedings{Azzopardi:2019:cwl,'
               'author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair}, '
               'title = {cwl_eval: An evaluation tool for information retrieval},'
               'booktitle = {Proceedings of the International ACM SIGIR Conference},'
               'year = {2019}}']
__license__ = 'MIT'
__version__ = '1.0.0'

import os
import argparse
import logging
from seeker.trec_qrel_handler import TrecQrelHandler
from ruler.cwl_ruler import CWLRuler
from ruler.ranking import RankingMaker, Ranking


def read_in_cost_file(cost_file):
    """
    Reads in the cost file and stores in a dictionary for looking up the costs.
    The element_type is to be denoted in the TREC Results File using the previously unused field (2nd Column).
    :param cost_file: expects a space/tab seperated file with element_type (string) and cost(float)
    :return: returns a dictionary of element_type/costs
    """
    costs = dict()
    with open(cost_file, "r") as cf:
        while cf:
            line = cf.readline()
            if not line:
                break
            (element_type, cost) = line.split()
            element_type = element_type.strip()
            costs[element_type] = float(cost)
    return costs


def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)



def parse_args():

    arg_parser = argparse.ArgumentParser(description="CWL Evaluation Metrics")
    arg_parser.add_argument("gain_file", help="A TREC Formatted Qrel File with relevance scores used as gains. "
                                              "Gain values should be between zero and one. "
                                              "Four column tab/space sep file with fields: topic_id unused doc_id gain")
    arg_parser.add_argument("result_file",
                            help="TREC formatted results file. Six column tab/space sep file with fields:"
                                 " topic_id element_type doc_id rank score run_id.")
    arg_parser.add_argument("-c", "--cost_file",
                            help="Costs associated with each element type specified in result file.",
                            required=False, default=None)
    arg_parser.add_argument("-m", "--metrics_file", help="The list of metrics that are to be reported. "
                                                         "If not specified, a set of default metrics will be reported."
                                                         " Tab/space sep file with fields: metric_name params",
                            required=False, default=None)
    arg_parser.add_argument("-b", "--bib_file", help="If specified, then the BibTeX for the measures used"
                                                     " will be saved to the filename given.", required=False,
                            default=None)
    arg_parser.add_argument("-n", "--colnames", help="Includes headings in the output.",
                            required=False, action="store_true")
    arg_parser.add_argument("-r", "--residuals", help="Include residual calculations.",
                            required=False, action="store_true")
    arg_parser.add_argument("--max_gain", help="Maximum gain associated with an item. Used for computing residuals. "
                                               "(default=1.0)", required=False, default=1.0)
    arg_parser.add_argument("--max_cost", help="Maximum cost associated with an item. Used for computing residuals. "
                                               "(default=1.0)", required=False, default=1.0)
    arg_parser.add_argument("--min_cost", help="Maximum cost associated with an item. Used for computing residuals. "
                                               "(default=1.0)", required=False, default=1.0)

    args = arg_parser.parse_args()
    if args.colnames:
        args.colnames = True
    else:
        args.colnames = False

    if args.residuals:
        args.residuals = True
    else:
        args.residuals = False

    return args


def main(results_file, gain_file, cost_file=None, metrics_file=None, bib_file=None, colnames=False,
         residuals=False, max_gain=1.0, max_cost=1.0, min_cost=1.0):

    logging.basicConfig(filename='cwl.log', level=logging.DEBUG)
    logging.info("Processing: {} using gain: {} and costs: {}".format(results_file, gain_file, cost_file))
    logging.info("Max Gain: {} Max Cost: {} Min Cost: {}".format(max_gain, max_cost, min_cost))
    qrh = TrecQrelHandler(gain_file)
    costs = None
    # read in cost file - if cost file exists
    if cost_file:
        costs = read_in_cost_file(cost_file)
    cwl_ruler = CWLRuler(metrics_file, residuals)

    curr_topic_id = None
    ranking_maker = None

    if colnames:
        if residuals:
            print("Topic\tMetric\tEU\tETU\tEC\tETC\tED\tResEU\tResETU\tResEC\tResETC\tResED")
        else:
            print("Topic\tMetric\tEU\tETU\tEC\tETC\tED")

    with open(results_file, "r") as rf:
        while rf:
            line = rf.readline()
            if not line:
                break
            (topic_id, element_type, doc_id, rank, score, run_id) = line.split()
            doc_id = doc_id.strip()

            if topic_id == curr_topic_id:
                # build vectors
                ranking_maker.add(doc_id, element_type)
            else:
                if curr_topic_id is not None:
                    # Perform the measurements
                    ranking = ranking_maker.get_ranking()
                    # print(ranking._gains[0:10])
                    cwl_ruler.measure(ranking)
                    cwl_ruler.report()

                # new topic
                curr_topic_id = topic_id

                # reset seen list
                ranking_maker = RankingMaker(curr_topic_id, qrh, costs,
                                             max_gain=max_gain, max_cost=max_cost, min_cost=min_cost)
                ranking_maker.add(doc_id, element_type)

        # Perform the Measurements on the last topic
        ranking = ranking_maker.get_ranking()
        # print(ranking._gains[0:10])
        cwl_ruler.measure(ranking)
        cwl_ruler.report()

    if bib_file:
        cwl_ruler.save_bibtex(bib_file)


if __name__ == "__main__":
    args = parse_args()

    check_file_exists(args.result_file)
    check_file_exists(args.gain_file)
    check_file_exists(args.cost_file)
    check_file_exists(args.metrics_file)

    main(args.result_file, args.gain_file, args.cost_file, args.metrics_file, args.bib_file,
         args.colnames, args.residuals, args.max_gain, args.max_cost, args.min_cost)
