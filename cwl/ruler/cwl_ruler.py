import os
import inspect
import importlib

from cwl.ruler.measures.cwl_metrics import *
from cwl.ruler.measures.cwl_precision import *
from cwl.ruler.measures.cwl_rbp import *
from cwl.ruler.measures.cwl_rr import *
from cwl.ruler.measures.cwl_ap import *
from cwl.ruler.measures.cwl_dcg import *
from cwl.ruler.measures.cwl_inst import *
from cwl.ruler.measures.cwl_insq import *
from cwl.ruler.measures.cwl_tbg import *
from cwl.ruler.measures.cwl_bpm import *
from cwl.ruler.measures.cwl_umeasure import *
from cwl.ruler.measures.cwl_ift import *
from cwl.ruler.measures.cwl_nerr import *
from cwl.ruler.ranking import Ranking

class CWLRuler(object):

    def __init__(self, metrics_file=None, residuals=False):
        self.metrics = []
        #add the metrics to the list
        if metrics_file:
            # load up the metrics specified
            self.populate_list(metrics_file)
        else:
            # use the default set of metrics
            # ideally we will tune these to create a set of baselines.
            # however, depending on the costs used... the tuning will be different
            # for instance, U-measure costs are in characters, while TBG costs are in seconds
            # if costs are not specified, then the cost of each item is 1.0
            self.metrics = [
                PrecisionCWLMetric(1),
                PrecisionCWLMetric(2),
                PrecisionCWLMetric(3),
                PrecisionCWLMetric(4),
                PrecisionCWLMetric(5),
                PrecisionCWLMetric(10),
                RBPCWLMetric(0.2),
                RBPCWLMetric(0.4),
                RBPCWLMetric(0.8),
                NDCGCWLMetric(5),
                NDCGCWLMetric(10),
                RRCWLMetric(),
                APCWLMetric(),
                INSTCWLMetric(1.0),
                INSTCWLMetric(2.0),
                INSTCWLMetric(3.0),
            ]

        for m in self.metrics:
            m.residuals = residuals

    def measure(self, ranking):
        for metric in self.metrics:
            metric.measure(ranking)

    def report(self):
        for metric in self.metrics:
            metric.report()

    def csv(self):
        out = ""
        for metric in self.metrics:
            out += (metric.csv() + ";")
        return out

    def populate_list(self, input_filename):
        """
        Reads from the input filename -- should be like
            ClassName(param1, param2, ...)
        Then once each class has been instantiated, adds to the self.metrics list
        Thanks @maxwelld90
        """
        f = open(input_filename, 'r')

        for line in f:
            # Process the input line
            line_split = line.strip().split('(')
            line_split[-1] = line_split[-1][:-1]  # Removes the extra bracket at the end

            class_name = line_split[0]
            parameters = line_split[1].split(',')
            self.metrics.append(self.instantiate_class(class_name, *parameters))

        f.close()

    def instantiate_class(self, requested_class_name, *args, **kwargs):
        """
        Given a class name and one or more parameters, attempts to instantiate the requested class with the provided parameters.
        If successful, the instantiated class is returned.
        """
        classes = self.get_class_list()
        ref = None
        casted_args = []
        
        # Change the args to ints/floats. Assuming that that is all that is required.
        for i in range(0, len(args)):
            val = args[i]
            
            if val == '':
                continue
            
            if '.' in val:
                casted_args.append(float(val))
            else:
                casted_args.append(int(val))
        
        for class_tuple in classes:
            class_name = class_tuple[0]
            class_ref = class_tuple[1]

            if class_name == requested_class_name:
                ref = class_ref(*casted_args)  # Instantiate the class with parameters!
                # If you want to use parameter names, try kwargs instead.

        # If ref is not set, the class was not located!
        if ref is None:
            raise NameError("The class {0} could not be found.".format(requested_class_name))

        return ref

    def get_class_list(self):
        """
        Looking inside the measures_package package, returns a list of all the classes that are available for instantiating.
        This means that any class inside any .py file in the measures directory is returned in the list from this method.
        """
        modules = []
        classes = []
        path = os.path.dirname(os.path.abspath(__file__))
        measures_path = os.path.join(path, 'measures')
        package_path = 'ruler.measures'

        # List through the modules in the specified package, ignoring __init__.py, and append them to a list.
        for f in os.listdir(measures_path):
            if f.endswith('.py') and not f.startswith('__init__'):
                modules.append('{0}.{1}'.format(package_path, os.path.splitext(f)[0]))

        module_references = []

        # Attempt to import each module in turn so we can access its classes
        for module in modules:
            module_references.append(importlib.import_module(module))

        # Now loop through each module, looking at the classes within it -
        # and then append each class to a list of valid classes.
        for module in module_references:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    classes.append((obj.__name__, obj))

        return classes

    def print_list(self):
        """
        Proof that it works, iterates over each instantiate metric class and calls whoami().
        """
        print("Displaying each metric:")
        print("======")
        for metric in self.metrics:
            metric.whoami()
        print("======")
        print(self.metrics)
        print("END")
        print()

    def save_bibtex(self, bib_file):

        eval_tool_bibtex = """
        @inproceedings{azzopardi2019cwl,
        author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair}
        title = {cwl\_eval: An Evaluation Tool for Information Retrieval},
        booktitle = {Proc. of the 42nd International ACM SIGIR Conference},
        series = {SIGIR '19},
        year = {2019} 
        }
        """

        bib_list = [eval_tool_bibtex]

        for m in self.metrics:
            if m.bibtex not in bib_list:
                bib_list.append(m.bibtex)

        with open(bib_file, "w") as bf:
            for bib in bib_list:
                bf.write(bib)
                bf.write("\n")
