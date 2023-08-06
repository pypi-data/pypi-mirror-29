#! /usr/bin/env python

import sys
import utils_bk 

weight_vector = [5.2935, 2.5843, 4.6718, 6.7032, 6.3449, 4.8819, 3.2902, 11.6925, 9.7603, 4.4712, 5.8023, 7.3304, 6.6022,
                 6.8118, 8.0286, 5.5164, 6.7205, 6.3547, 6.5036, 4.2754, 6.989, 5.63, 7.514, 6.6156, 4.1002, 6.0268]

# alpha0=1.0, alpha1=1.0, beta0=1.0, beta1=0.01, chimera_num_thres=2, chimera_overhang_thres=30, chimera_pooled_control_file=None, debug=True, donor_size='3,6', effect_size_thres=3.0, genome_id='hg19', grc=True, keep_annotated=False, log_BF_thres=3.0

# weight_vector = [1] * 26

input_file = sys.argv[1]
output_file = sys.argv[2]

utils_bk.check_significance(input_file, output_file, weight_vector, log_BF_thres=3.0, alpha0=1.0, alpha1=1.0, beta0=1.0, beta1=0.01)


