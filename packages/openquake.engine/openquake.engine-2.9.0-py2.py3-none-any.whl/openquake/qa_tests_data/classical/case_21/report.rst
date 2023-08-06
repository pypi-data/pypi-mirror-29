Classical Hazard QA Test, Case 21
=================================

============== ===================
checksum32     124,630,436        
date           2018-02-19T09:59:01
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 4

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     106               
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
====================== ====== =============== ================
smlt_path              weight gsim_logic_tree num_realizations
====================== ====== =============== ================
b1_mfd1_high_dip_dip30 0.013  trivial(1)      1/1             
b1_mfd1_high_dip_dip45 0.040  trivial(1)      1/1             
b1_mfd1_high_dip_dip60 0.013  trivial(1)      1/1             
b1_mfd1_low_dip_dip30  0.013  trivial(1)      1/1             
b1_mfd1_low_dip_dip45  0.040  trivial(1)      1/1             
b1_mfd1_low_dip_dip60  0.013  trivial(1)      1/1             
b1_mfd1_mid_dip_dip30  0.040  trivial(1)      1/1             
b1_mfd1_mid_dip_dip45  0.119  trivial(1)      1/1             
b1_mfd1_mid_dip_dip60  0.040  trivial(1)      1/1             
b1_mfd2_high_dip_dip30 0.014  trivial(1)      1/1             
b1_mfd2_high_dip_dip45 0.041  trivial(1)      1/1             
b1_mfd2_high_dip_dip60 0.014  trivial(1)      1/1             
b1_mfd2_low_dip_dip30  0.014  trivial(1)      1/1             
b1_mfd2_low_dip_dip45  0.041  trivial(1)      1/1             
b1_mfd2_low_dip_dip60  0.014  trivial(1)      1/1             
b1_mfd2_mid_dip_dip30  0.041  trivial(1)      1/1             
b1_mfd2_mid_dip_dip45  0.122  trivial(1)      1/1             
b1_mfd2_mid_dip_dip60  0.041  trivial(1)      1/1             
b1_mfd3_high_dip_dip30 0.013  trivial(1)      1/1             
b1_mfd3_high_dip_dip45 0.040  trivial(1)      1/1             
b1_mfd3_high_dip_dip60 0.013  trivial(1)      1/1             
b1_mfd3_low_dip_dip30  0.013  trivial(1)      1/1             
b1_mfd3_low_dip_dip45  0.040  trivial(1)      1/1             
b1_mfd3_low_dip_dip60  0.013  trivial(1)      1/1             
b1_mfd3_mid_dip_dip30  0.040  trivial(1)      1/1             
b1_mfd3_mid_dip_dip45  0.119  trivial(1)      1/1             
b1_mfd3_mid_dip_dip60  0.040  trivial(1)      1/1             
====================== ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
1      SadighEtAl1997() rrup      vs30       mag rake  
2      SadighEtAl1997() rrup      vs30       mag rake  
3      SadighEtAl1997() rrup      vs30       mag rake  
4      SadighEtAl1997() rrup      vs30       mag rake  
5      SadighEtAl1997() rrup      vs30       mag rake  
6      SadighEtAl1997() rrup      vs30       mag rake  
7      SadighEtAl1997() rrup      vs30       mag rake  
8      SadighEtAl1997() rrup      vs30       mag rake  
9      SadighEtAl1997() rrup      vs30       mag rake  
10     SadighEtAl1997() rrup      vs30       mag rake  
11     SadighEtAl1997() rrup      vs30       mag rake  
12     SadighEtAl1997() rrup      vs30       mag rake  
13     SadighEtAl1997() rrup      vs30       mag rake  
14     SadighEtAl1997() rrup      vs30       mag rake  
15     SadighEtAl1997() rrup      vs30       mag rake  
16     SadighEtAl1997() rrup      vs30       mag rake  
17     SadighEtAl1997() rrup      vs30       mag rake  
18     SadighEtAl1997() rrup      vs30       mag rake  
19     SadighEtAl1997() rrup      vs30       mag rake  
20     SadighEtAl1997() rrup      vs30       mag rake  
21     SadighEtAl1997() rrup      vs30       mag rake  
22     SadighEtAl1997() rrup      vs30       mag rake  
23     SadighEtAl1997() rrup      vs30       mag rake  
24     SadighEtAl1997() rrup      vs30       mag rake  
25     SadighEtAl1997() rrup      vs30       mag rake  
26     SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=27, rlzs=27)
  0,SadighEtAl1997(): [0]
  1,SadighEtAl1997(): [1]
  2,SadighEtAl1997(): [2]
  3,SadighEtAl1997(): [3]
  4,SadighEtAl1997(): [4]
  5,SadighEtAl1997(): [5]
  6,SadighEtAl1997(): [6]
  7,SadighEtAl1997(): [7]
  8,SadighEtAl1997(): [8]
  9,SadighEtAl1997(): [9]
  10,SadighEtAl1997(): [10]
  11,SadighEtAl1997(): [11]
  12,SadighEtAl1997(): [12]
  13,SadighEtAl1997(): [13]
  14,SadighEtAl1997(): [14]
  15,SadighEtAl1997(): [15]
  16,SadighEtAl1997(): [16]
  17,SadighEtAl1997(): [17]
  18,SadighEtAl1997(): [18]
  19,SadighEtAl1997(): [19]
  20,SadighEtAl1997(): [20]
  21,SadighEtAl1997(): [21]
  22,SadighEtAl1997(): [22]
  23,SadighEtAl1997(): [23]
  24,SadighEtAl1997(): [24]
  25,SadighEtAl1997(): [25]
  26,SadighEtAl1997(): [26]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 471          296         
source_model.xml 1      Active Shallow Crust 268          296         
source_model.xml 2      Active Shallow Crust 209          296         
source_model.xml 3      Active Shallow Crust 534          296         
source_model.xml 4      Active Shallow Crust 298          296         
source_model.xml 5      Active Shallow Crust 239          296         
source_model.xml 6      Active Shallow Crust 474          296         
source_model.xml 7      Active Shallow Crust 238          296         
source_model.xml 8      Active Shallow Crust 179          296         
source_model.xml 9      Active Shallow Crust 513          296         
source_model.xml 10     Active Shallow Crust 277          296         
source_model.xml 11     Active Shallow Crust 218          296         
source_model.xml 12     Active Shallow Crust 465          296         
source_model.xml 13     Active Shallow Crust 229          296         
source_model.xml 14     Active Shallow Crust 170          296         
source_model.xml 15     Active Shallow Crust 513          296         
source_model.xml 16     Active Shallow Crust 277          296         
source_model.xml 17     Active Shallow Crust 176          296         
source_model.xml 18     Active Shallow Crust 483          296         
source_model.xml 19     Active Shallow Crust 247          296         
source_model.xml 20     Active Shallow Crust 188          296         
source_model.xml 21     Active Shallow Crust 582          296         
source_model.xml 22     Active Shallow Crust 346          296         
source_model.xml 23     Active Shallow Crust 287          296         
source_model.xml 24     Active Shallow Crust 516          296         
source_model.xml 25     Active Shallow Crust 280          296         
source_model.xml 26     Active Shallow Crust 221          296         
================ ====== ==================== ============ ============

============= =====
#TRT models   27   
#eff_ruptures 8,898
#tot_ruptures 7,992
#tot_weight   8,175
============= =====

Informational data
------------------
======================= =====================================================================================
count_ruptures.received tot 52.58 KB, max_per_task 849 B                                                     
count_ruptures.sent     sources 71.16 KB, srcfilter 46.54 KB, param 27.46 KB, monitor 20.56 KB, gsims 7.73 KB
hazard.input_weight     8175.0                                                                               
hazard.n_imts           1                                                                                    
hazard.n_levels         4                                                                                    
hazard.n_realizations   27                                                                                   
hazard.n_sites          1                                                                                    
hazard.n_sources        54                                                                                   
hazard.output_weight    4.0                                                                                  
hostname                tstation.gem.lan                                                                     
require_epsilons        False                                                                                
======================= =====================================================================================

Slowest sources
---------------
========= ================= ============ ========= ========= =========
source_id source_class      num_ruptures calc_time num_sites num_split
========= ================= ============ ========= ========= =========
SFLT2     SimpleFaultSource 89           0.083     46        45       
SFLT1     SimpleFaultSource 132          0.081     52        51       
========= ================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
================= ========= ======
source_class      calc_time counts
================= ========= ======
SimpleFaultSource 0.165     2     
================= ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_ruptures     0.003 0.004  0.002 0.036 66       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
managing sources               0.443     0.0       1     
reading composite source model 0.357     0.0       1     
total count_ruptures           0.204     0.0       66    
store source_info              0.005     0.0       1     
aggregate curves               9.160E-04 0.0       66    
reading site collection        5.746E-05 0.0       1     
saving probability maps        2.551E-05 0.0       1     
============================== ========= ========= ======