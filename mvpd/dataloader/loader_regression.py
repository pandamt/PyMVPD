"""
Load input to MVPD regression model.
""" 
import sys
sys.path.append("..")
import numpy as np
import itertools as it
from analysis_spec import sub, roidata_save_dir, roi_1_name, roi_2_name, filepath_func, filepath_mask1, filepath_mask2


# Implement the data loader.
class ROI_Dataset(object):
    """cope1(face) dataset."""
    def __init__(self, ROIs_1=[], ROIs_2=[]):
        'Initialization'
        self.ROIs_1 = []
        self.ROIs_2 = []

    def get_train(self, this_run=0, total_run=0):
        NULL = True # dataset is empty
        for run in it.chain(range(1,this_run), range(this_run+1,total_run+1)):
                roidata_save_dir_run = roidata_save_dir+'roi_run_'+str(run)+'/'
                roi_1_data_run = np.load(roidata_save_dir_run+roi_1_name+'_data_run_'+str(run)+'.npy')
                roi_2_data_run = np.load(roidata_save_dir_run+roi_2_name+'_data_run_'+str(run)+'.npy')
               
                # Concatenate data from each run for training
                if NULL:
                     roi_1_data = roi_1_data_run
                     roi_2_data = roi_2_data_run
                     NULL = False
                else: 
                     roi_1_data = np.concatenate([roi_1_data, roi_1_data_run], 0) 
                     roi_2_data = np.concatenate([roi_2_data, roi_2_data_run], 0)

        self.ROIs_1 = np.float32(roi_1_data)
        self.ROIs_2 = np.float32(roi_2_data)
      
    def get_test(self, this_run=0, total_run=0): 
        roidata_save_dir_run = roidata_save_dir+'roi_run_'+str(this_run)+'/'  
        roi_1_data = np.load(roidata_save_dir_run+roi_1_name+'_data_run_'+str(this_run)+'.npy')
        roi_2_data = np.load(roidata_save_dir_run+roi_2_name+'_data_run_'+str(this_run)+'.npy') 
  
        self.ROIs_1 = np.float32(roi_1_data)
        self.ROIs_2 = np.float32(roi_2_data)

    def __len__(self):
        'Denotes the total number of predictor samples'
        return len(self.ROIs_1)
    
    def __getitem__(self, idx):
        'Generates one sample of data'
        ROI_1 = self.ROIs_1[idx]
        ROI_2 = self.ROIs_2[idx]
        sample = {'ROI_1': ROI_1, 'ROI_2': ROI_2}
        return sample

