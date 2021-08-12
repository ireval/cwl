# C/W/L Evaluation Script
An evaluation script based on the C/W/L framework
that is TREC Compatible and provides a replacement
for INST_EVAL, RBP_EVAL, TBG_EVAL, UMeasure, TREC_EVAL.


## Install

Install either via `pip install cwl-eval` or ``git clone https://github.com/ireval/cwl.git``.
`cwl-eval` requires Python 3 and Numpy.


## Usage

Once you have installed the C/W/L Evaluation Framework using `pip install`, you should be able to use the `cwl-eval` as shown below.
If you have used `git clone` to install the framework, then you will need to run `cwl_eval.py` directly.

    Usage: cwl-eval <gain_file> <result_file> -c <cost_file> -m <metrics_file> -b <bibtex_file>

    Usage: cwl-eval <gain_file> <result_file> -c <cost_file> -m <metrics_file>

    Usage: cwl-eval <gain_file> <result_file>

    Usage: cwl-eval -h

- <gain_file>   : A TREC Formatted Qrel File with relevance scores used as gains (float)
                Four column tab/space sep file with fields: topic_id unused doc_id gain

- <cost_file>   : Costs associated with element type

- <cost_file>   : If not specified, costs default to one for all elements
                Two column tab/space sep file with fields: element_type element_cost

- <result_file> : A TREC Formatted Result File
                Six column tab/space sep file with fields: topic_id element_type doc_id rank score run_id

- <metrics_file>: The list of metrics that are to be reported
                If not specified, a set of default metrics will be reported
                Tab/space sep file with fields: metric_name params

- <bibtex_file>: Specify this file if you would like the BibTeX associated with the measures specified to be
               output to a file called <bibtex_file>

- -n: Add -n flag to output column names (e.g. Topic, Metric, EU, ETU, EC, ETC, ED)

- -r: Add -r flag to also output residuals for each measurement.

- --max_n <value>: Specify the depth of the calculation of the metrics (default=1000). 

- --max_gain <value>: Specify the maximum value of the gain (default=1.0). Note some metrics have restrictions on the maximum allowable value. This is also used when computing the residuals.

- --min_gain <value>: Specify the minimum value of the gain (default=0.0). Note some metrics have restrictions on the minimum allowable value.



**Example without using a cost file**
When no costs are specified the cost per item is assumed to be 1.0, and EC and I will be equal.

    cwl-eval qrel_file result_file


**Example with using a cost file**

    cwl-eval qrel_file result_file -c cost_file



**Output**
A seven column tab/space separated file that contains:

- Topic ID
- Metric Name
- Expected Utility Per Item (EU)
- Expected Utility (ETU)
- Expected Cost per Item (EC)
- Expected Cost (ETC)
- Expected Depth (ED)

If the `-r` flag is included, then another five columns will be included: ResEU, ResETU, ResEC, ResETC, ResED. 
These report the residual values for each of the measures (i.e. the difference between the best case and worse case for un-judged items).



CWL Citation
------------
Please consider citing the following paper when using our code for your evaluations:

        @inproceedings{azzopardi2019cwl,
            author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair},
            title = {cwl\_eval: An Evaluation Tool for Information Retrieval},
            booktitle = {Proc. of the 42nd International ACM SIGIR Conference},
            series = {SIGIR '19},
            year = {2019}
        } 



Metrics within CWL EVAL
-----------------------
For each of the metrics provided in cwl_eval.py, the user model for each
measure has been extracted and encoded within the C/W/L framework.

All weightings have been converted to probabilities.

As a result, all metrics report a series of values (not a single value):
 - Expected Utility per item examined (EU),
 - Expected Total Utility (ETU),
 - Expected Cost per item examined (EC),
 - Expected Total Cost (ETC)
 - Expected number of items to be examined i.e expected depth (ED)

All the values are related, such that:

ETU = EU * ED

and

ETC = EC * ED

If the cost per item is 1.0, then the expected cost per item is 1.0,
and the expected cost EC will be equal to I.

Costs can be specified in whatever unit is desired. i.e seconds, characters, words, etc.


**List of Metrics**

- RR - (Expected) Reciprocal Rank
- P@k - Precision At k
- AP - Average Precision
- RBP - Rank Biased Precision
- INST T
- INSQ T
- NDCG@k - Normalized Discounted Cumulative Gain at k
- BPM-Static - Bejewelled Player Model  - Static
- BPM-Dynamic - Bejewelled Player Model - Dynamic
- UMeasure - U-Measure
- TBG - Time Biased Gain
- IFT-C1 - Information Foraging Theory (Goal)
- IFT-C2 - Information Foraging Theory (Rate)
- IFT-C1-C2 - Information Foraging Theory (Goal and Rate)
- NERREq8 - Not/Nearly ERR(Eq8)@k using gain based stopping with truncation k
- NERREq9 - Not/Nearly ERR(Eq9)@k using gain based stopping and discount with truncation k
- NERREq10 - Not/Nearly ERR(Eq10)@phi using gain based stopping and RBP patience (phi)
- NERREq11 - Not/Nearly ERR(Eq11)@T using gain based stopping and INST Goal (T)



**Sample Output from cwl_eval.py where costs per item = 1.0**

    cwl-eval qrel_file result_file

| Topic| Metric                                             | EU | ETU | EC | ETC | ED |
|------|---------------------------------------------------|-------|-------|-------|--------|--------|
| T1   | P@20                                              | 0.150 | 3.000 | 1.000 | 20.000 | 20.000 |
| T1   | P@10                                              | 0.300 | 3.000 | 1.000 | 10.000 | 10.000 |
| T1   | P@5                                               | 0.360 | 1.800 | 1.000 | 5.000  | 5.000  |
| T1   | P@1                                               | 1.000 | 1.000 | 1.000 | 1.000  | 1.000  |
| T1   | RBP@0.5                                           | 0.566 | 1.132 | 1.000 | 2.000  | 2.000  |
| T1   | RBP@0.9                                           | 0.214 | 2.136 | 1.000 | 10.000 | 10.000 |
| T1   | SDCG-k@10                                         | 0.380 | 1.726 | 1.000 | 4.544  | 4.544  |
| T1   | SDCG-k@5                                          | 0.461 | 1.358 | 1.000 | 2.948  | 2.948  |
| T1   | RR                                                | 1.000 | 1.000 | 1.000 | 1.000  | 1.000  |
| T1   | AP                                                | 0.397 | 1.907 | 1.000 | 4.800  | 4.800  |
| T1   | INST-T=2                                          | 0.401 | 1.303 | 1.000 | 3.242  | 3.247  |
| T1   | INST-T=1                                          | 0.680 | 1.071 | 1.000 | 1.574  | 1.575  |
| T1   | INSQ-T=2                                          | 0.316 | 1.428 | 1.000 | 4.509  | 4.525  |
| T1   | INSQ-T=1                                          | 0.465 | 1.198 | 1.000 | 2.572  | 2.576  |
| T1   | BPM-Static-T=1-K=1000                             | 1.000 | 1.000 | 1.000 | 1.000  | 1.000  |
| T1   | BPM-Static-T=1000-K=10                            | 0.300 | 3.000 | 1.000 | 10.000 | 10.000 |
| T1   | BPM-Static-T=1.2-K=10                             | 0.400 | 1.200 | 1.000 | 3.000  | 3.000  |
| T1   | BPM-Dynamic-T=1-K=1000-hb=1.0-hc=1.0              | 1.000 | 1.000 | 1.000 | 1.000  | 1.000  |
| T1   | BPM-Dynamic-T=1000-K=10-hb=1.0-hc=1.0             | 0.300 | 3.000 | 1.000 | 10.000 | 10.000 |
| T1   | BPM-Dynamic-T=1.2-K=10-hb=1.0-hc=1.0              | 0.400 | 1.200 | 1.000 | 3.000  | 3.000  |
| T1   | U-L@50                                            | 0.109 | 2.772 | 1.000 | 25.500 | 25.500 |
| T1   | U-L@10                                            | 0.338 | 1.860 | 1.000 | 5.500  | 5.500  |
| T1   | TBG-H@22                                          | 0.083 | 2.676 | 1.000 | 32.242 | 32.242 |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@1                          | 0.456 | 1.323 | 1.000 | 2.903  | 2.903  |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@10                         | 0.308 | 2.078 | 1.000 | 6.738  | 6.738  |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@100                        | 0.289 | 2.224 | 1.000 | 7.698  | 7.698  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@1                          | 0.463 | 1.255 | 1.000 | 2.711  | 2.711  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@10                         | 0.293 | 2.040 | 1.000 | 6.965  | 6.965  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@100                        | 0.197 | 2.994 | 1.000 | 15.208 | 15.208 |
| T1   | IFT-C1-C2-T@2.0-b1@0.9-R1@10-A@2.0-b2@0.9-R2@10   | 0.329 | 1.804 | 1.000 | 5.487  | 5.487  |
| T1   | IFT-C1-C2-T@2.0-b1@0.9-R1@100-A@2.0-b2@0.9-R2@100 | 0.289 | 2.223 | 1.000 | 7.697  | 7.697  |


**Sample Output from cwl-eval where costs are set based on cost_file**

    cwl-eval qrel_file result_file -c cost_file

| Topic| Metric                                             | EU   | ETU   | EC     | ETC   | ED     |
|------|---------------------------------------------------|-------|-------|-------|--------|--------|
| T1   | P@20                                              | 0.150 | 3.000 | 1.650 | 33.000 | 20.000 |
| T1   | P@10                                              | 0.300 | 3.000 | 2.300 | 23.000 | 10.000 |
| T1   | P@5                                               | 0.360 | 1.800 | 2.400 | 12.000 | 5.000  |
| T1   | P@1                                               | 1.000 | 1.000 | 2.000 | 2.000  | 1.000  |
| T1   | RBP@0.5                                           | 0.566 | 1.132 | 1.951 | 3.902  | 2.000  |
| T1   | RBP@0.9                                           | 0.214 | 2.136 | 1.776 | 17.765 | 10.000 |
| T1   | SDCG-k@10                                         | 0.380 | 1.726 | 2.188 | 9.943  | 4.544  |
| T1   | SDCG-k@5                                          | 0.461 | 1.358 | 2.224 | 6.557  | 2.948  |
| T1   | RR                                                | 1.000 | 1.000 | 2.000 | 2.000  | 1.000  |
| T1   | AP                                                | 0.397 | 1.907 | 1.958 | 9.400  | 4.800  |
| T1   | INST-T=2                                          | 0.401 | 1.303 | 1.884 | 6.113  | 3.247  |
| T1   | INST-T=1                                          | 0.680 | 1.071 | 1.955 | 3.077  | 1.575  |
| T1   | INSQ-T=2                                          | 0.316 | 1.428 | 1.799 | 8.125  | 4.525  |
| T1   | INSQ-T=1                                          | 0.465 | 1.198 | 1.887 | 4.855  | 2.576  |
| T1   | BPM-Static-T=1-K=1000                             | 1.000 | 1.000 | 2.000 | 2.000  | 1.000  |
| T1   | BPM-Static-T=1000-K=10                            | 0.360 | 1.800 | 2.400 | 12.000 | 5.000  |
| T1   | BPM-Static-T=1.2-K=10                             | 0.400 | 1.200 | 1.667 | 5.000  | 3.000  |
| T1   | BPM-Dynamic-T=1-K=1000-hb=1.0-hc=1.0              | 1.000 | 1.000 | 2.000 | 2.000  | 1.000  |
| T1   | BPM-Dynamic-T=1000-K=10-hb=1.0-hc=1.0             | 0.360 | 1.800 | 2.400 | 12.000 | 5.000  |
| T1   | BPM-Dynamic-T=1.2-K=10-hb=1.0-hc=1.0              | 0.400 | 1.200 | 1.667 | 5.000  | 3.000  |
| T1   | U-L@50                                            | 0.162 | 2.552 | 1.654 | 26.000 | 15.720 |
| T1   | U-L@10                                            | 0.444 | 1.420 | 2.094 | 6.700  | 3.200  |
| T1   | TBG-H@22                                          | 0.143 | 2.339 | 2.046 | 33.508 | 16.375 |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@1                          | 0.456 | 1.323 | 1.971 | 5.723  | 2.903  |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@10                         | 0.308 | 2.078 | 2.080 | 14.017 | 6.738  |
| T1   | IFT-C1-T@2.0-b1@0.9-R1@100                        | 0.289 | 2.224 | 2.068 | 15.922 | 7.698  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@1                          | 0.516 | 1.180 | 1.958 | 4.481  | 2.289  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@10                         | 0.404 | 1.368 | 2.011 | 6.802  | 3.382  |
| T1   | IFT-C2-A@0.2-b2@0.9-R2@100                        | 0.360 | 1.786 | 2.388 | 11.832 | 4.954  |
| T1   | IFT-C1-C2-T@2.0-b1@0.9-R1@10-A@2.0-b2@0.9-R2@10   | 0.413 | 1.361 | 1.990 | 6.552  | 3.293  |
| T1   | IFT-C1-C2-T@2.0-b1@0.9-R1@100-A@2.0-b2@0.9-R2@100 | 0.360 | 1.786 | 2.388 | 11.832 | 4.954  |


**Using the metrics_file to specify the metrics**

    cwl-eval qrel_file result_file -m metrics_file

if a metrics_file is not specified, CWL Eval will default to a set of metrics
defined in `ruler/measures/cwl_ruler.py`

If the metrics_file is specified, CWL Eval will instantiate and use the metrics listed.
An example test_metrics_file is provided, which includes the following:

    PrecisionCWLMetric(k=1)
    PrecisionCWLMetric(k=5)
    PrecisionCWLMetric(k=10)
    PrecisionCWLMetric(k=20)
    RBPCWLMetric(theta=0.9)
    NDCGCWLMetric(k=10)
    RRCWLMetric()
    APCWLMetric()
    INSTCWLMetric(T=1.0)
    INSQCWLMetric(T=1.0)
    BPMCWLMetric(T=1.0,K=20)
    BPMCWLMetric(T=2.0,K=10)
    BPMDCWLMetric(T=1,20)
    BPMDCWLMetric(T=2.0,K=10)
    UMeasureCWLMetric(L=50)
    UMeasureCWLMetric(L=10)
    TBGCWLMetric(halflife=22)
    IFTGoalCWLMetric(T=2.0, b1=0.9, R1=10)
    IFTGoalCWLMetric(T=2.0, b1=0.9, R1=100)
    IFTRateCWLMetric(A=0.2, b2=0.9, R2=10)
    IFTRateCWLMetric(A=0.2, b2=0.9, R2=100)
    IFTGoalRateCWLMetric(T=2.0, b1=0.9, R1=10, A=0.2, b2=0.9, R2=10)
    IFTGoalRateCWLMetric(T=2.0, b1=0.9, R1=100, A=0.2, b2=0.9, R2=100)
    NERReq8CWLMetric(k=10)
    NERReq9CWLMetric(k=10)
    NERReq10CWLMetric(phi=0.8)
    NERReq11CWLMetric(T=2.0)

To specify which metric you desire, inspect the metrics classes in `ruler/measures/`
to see what metrics are available, and how the parameterize them.

For example if you only wanted Precision Based Measures then you can list them as follows:

    PrecisionCWLMetric(1)
    PrecisionCWLMetric(2)
    PrecisionCWLMetric(3)
    PrecisionCWLMetric(4)
    PrecisionCWLMetric(5)
    PrecisionCWLMetric(6)
    PrecisionCWLMetric(7)
    PrecisionCWLMetric(8)
    PrecisionCWLMetric(9)
    PrecisionCWLMetric(10)
    PrecisionCWLMetric(11)
    PrecisionCWLMetric(12)
    PrecisionCWLMetric(13)
    PrecisionCWLMetric(14)
    PrecisionCWLMetric(15)
    PrecisionCWLMetric(16)
    PrecisionCWLMetric(17)
    PrecisionCWLMetric(18)
    PrecisionCWLMetric(19)
    PrecisionCWLMetric(20)

While if you only wanted Rank Biased Precision Measures, then you can vary the patience parameter:

    RBPCWLMetric(0.1)
    RBPCWLMetric(0.2)
    RBPCWLMetric(0.3)
    RBPCWLMetric(0.4)
    RBPCWLMetric(0.5)
    RBPCWLMetric(0.6)
    RBPCWLMetric(0.7)
    RBPCWLMetric(0.8)
    RBPCWLMetric(0.9)
    RBPCWLMetric(0.95)
    RBPCWLMetric(0.99)


