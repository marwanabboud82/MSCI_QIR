# -*- coding: utf-8 -*-
"""
@author: mabboud
"""
import pandas as pd
import numpy as np

def AssessFinalInvestability(OutputUpdateSegmNbComp,OutputSizeSegmentAssignment):
        
    
    OutputFinalInvestability= OutputSizeSegmentAssignment 
    
    for mkt in OutputFinalInvestability.keys():
    
        Market_SecurityData =  OutputFinalInvestability[mkt]['Market_SecurityData']
        QIR_MSSC = OutputUpdateSegmNbComp[mkt]['InterimData'].loc['InterimMSSC'].iloc[0]*1e+6
        Market_SecurityData['Final_FFmktCap']=Market_SecurityData['FF_MktCap_usd']*0
        Market_SecurityData['Final_FullmktCap']=Market_SecurityData['FF_MktCap_usd']*0
        Market_SecurityData['Final_FF_Dist']=Market_SecurityData['FF_MktCap_usd']*0
        Market_SecurityData['Final_Full_Dist']=Market_SecurityData['FF_MktCap_usd']*0
        Market_SecurityData['Final_Test']=Market_SecurityData['FF_MktCap_usd']*0
        
        
        # Minimum Free Float Market Cap: 
        # SML: FFMktCap > 50% x QIR MSSC, Existing: No FFMktCap 
        # NEW: FFMktCap > 90% x QIR MSSC, FullMktCap > 1.8 x QIR MSSC
        
        #idxNewSec = ( (Market_SecurityData['Status']!='STD') & (Market_SecurityData['Status']!='SML') ).tolist()
        #idxExistingSec  = ( (Market_SecurityData['Status']=='STD') | (Market_SecurityData['Status']=='SML') ).tolist()
        
        idxNewSec = ( (Market_SecurityData['Status']!='STD') & (Market_SecurityData['Status']!='SML') ).tolist()
        idxSMLSec  = ( (Market_SecurityData['Status']=='SML') ).tolist()
        idxExistingSec  = ( (Market_SecurityData['Status']=='STD') ).tolist()
        
        #STD
        Market_SecurityData.loc[((Market_SecurityData['FF_MktCap_usd'] >=0) & idxExistingSec), 'Final_FFmktCap'] = 1
        Market_SecurityData.loc[idxExistingSec, 'Final_FF_Dist'] = 0 / Market_SecurityData.loc[idxExistingSec,'FF_MktCap_usd'] -1
        Market_SecurityData.loc[((Market_SecurityData['company_full_mktcap'] >=0) & idxExistingSec), 'Final_FullmktCap'] = 1
        Market_SecurityData.loc[idxExistingSec, 'Final_Full_Dist'] = 0 / Market_SecurityData.loc[idxExistingSec,'company_full_mktcap'] -1
        
        
        #SML
        Market_SecurityData.loc[((Market_SecurityData['FF_MktCap_usd'] >= 0.5* QIR_MSSC) & idxSMLSec), 'Final_FFmktCap'] = 1
        Market_SecurityData.loc[idxSMLSec, 'Final_FF_Dist'] = (0.5* QIR_MSSC) / Market_SecurityData.loc[idxSMLSec,'FF_MktCap_usd'] -1
        Market_SecurityData.loc[((Market_SecurityData['company_full_mktcap'] >=0) & idxSMLSec), 'Final_FullmktCap'] = 1
        Market_SecurityData.loc[idxSMLSec, 'Final_Full_Dist'] = 0 / Market_SecurityData.loc[idxSMLSec,'company_full_mktcap'] -1
        
        
        #New
        Market_SecurityData.loc[((Market_SecurityData['FF_MktCap_usd'] >= 0.5* (1.8)* QIR_MSSC) & idxNewSec), 'Final_FFmktCap'] = 1
        Market_SecurityData.loc[idxNewSec, 'Final_FF_Dist'] = (0.5* (1.8)* QIR_MSSC) / Market_SecurityData.loc[idxNewSec,'FF_MktCap_usd'] -1
        
        Market_SecurityData.loc[((Market_SecurityData['company_full_mktcap'] >= (1.8)* QIR_MSSC) & idxNewSec), 'Final_FullmktCap'] = 1
        Market_SecurityData.loc[idxNewSec, 'Final_Full_Dist'] = ((1.8)* QIR_MSSC) / Market_SecurityData.loc[idxNewSec,'company_full_mktcap'] -1
    
        
        
        # Minimum FIF: 
        # TO BE DONE
        
        # Minimum Foreign Room Requirement
        # TO BE DONE
        
        Market_SecurityData['Final_Test'] = Market_SecurityData['Final_FFmktCap'] * Market_SecurityData['Final_FullmktCap']
    
        OutputFinalInvestability[mkt]['Market_SecurityData'] = Market_SecurityData
        
        print(mkt)
    
   
    return OutputFinalInvestability

