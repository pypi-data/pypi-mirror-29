Hazard Calculation for end-to-end hazard+risk
=============================================

============== ===================
checksum32     2,783,587,006      
date           2018-02-19T09:58:09
engine_version 2.9.0-gitb536198   
============== ===================

num_sites = 1, num_levels = 50

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 300.0}
investigation_time              15.0              
ses_per_logic_tree_path         1                 
truncation_level                4.0               
rupture_mesh_spacing            20.0              
complex_fault_mesh_spacing      20.0              
width_of_mfd_bin                0.2               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     1024              
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job_h.ini <job_h.ini>`_                                    
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ====== =============== ================
smlt_path weight gsim_logic_tree num_realizations
========= ====== =============== ================
b1        1.000  simple(1,4)     4/4             
========= ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ======================================================================================== ========== ========== ==============
grp_id gsims                                                                                    distances  siteparams ruptparams    
====== ======================================================================================== ========== ========== ==============
0      AkkarBommer2010()                                                                        rjb        vs30       mag rake      
1      AtkinsonBoore2003SInter() LinLee2008SInter() YoungsEtAl1997SInter() ZhaoEtAl2006SInter() rhypo rrup vs30       hypo_depth mag
====== ======================================================================================== ========== ========== ==============

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=5, rlzs=4)
  0,AkkarBommer2010(): [0 1 2 3]
  1,AtkinsonBoore2003SInter(): [1]
  1,LinLee2008SInter(): [3]
  1,YoungsEtAl1997SInter(): [2]
  1,ZhaoEtAl2006SInter(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 23           23          
source_model.xml 1      Subduction Interface 23           23          
================ ====== ==================== ============ ============

============= ==
#TRT models   2 
#eff_ruptures 46
#tot_ruptures 46
#tot_weight   11
============= ==

Informational data
------------------
======================= =============================================================================
count_ruptures.received tot 1.59 KB, max_per_task 814 B                                              
count_ruptures.sent     sources 2.32 KB, param 1.57 KB, srcfilter 1.41 KB, monitor 638 B, gsims 519 B
hazard.input_weight     4.6000000000000005                                                           
hazard.n_imts           1                                                                            
hazard.n_levels         50                                                                           
hazard.n_realizations   4                                                                            
hazard.n_sites          1                                                                            
hazard.n_sources        2                                                                            
hazard.output_weight    50.0                                                                         
hostname                tstation.gem.lan                                                             
require_epsilons        False                                                                        
======================= =============================================================================

Slowest sources
---------------
========= ============ ============ ========= ========= =========
source_id source_class num_ruptures calc_time num_sites num_split
========= ============ ============ ========= ========= =========
A         PointSource  23           3.080E-04 2         1        
B         PointSource  23           2.549E-04 2         1        
========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
PointSource  5.629E-04 2     
============ ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ========= ===== ===== =========
operation-duration mean  stddev    min   max   num_tasks
count_ruptures     0.001 1.212E-04 0.001 0.001 2        
================== ===== ========= ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
store source_info              0.004     0.0       1     
managing sources               0.004     0.0       1     
reading composite source model 0.002     0.0       1     
total count_ruptures           0.002     0.070     2     
reading site collection        6.175E-05 0.0       1     
aggregate curves               4.125E-05 0.0       2     
saving probability maps        2.956E-05 0.0       1     
============================== ========= ========= ======