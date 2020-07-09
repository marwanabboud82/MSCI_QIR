# -*- coding: utf-8 -*-
"""
@author: mabboud
"""
import pandas as pd
import numpy as np

def SizeSegmentAssignment(OutputUpdateSegmNbComp,All_CompanyData,All_SecurityData):
    
    OutputSizeSegmentAssignment={}
    
    for mkt in OutputUpdateSegmNbComp.keys():
        print(mkt)
        
        Market_SecurityData = All_SecurityData.loc[All_SecurityData['Market']==mkt]
        Market_CompanyData = All_CompanyData.loc[All_CompanyData['Market']==mkt]
        
        MIEU = OutputUpdateSegmNbComp[mkt]['MIEU']
        
        MIEU= MIEU.sort_values('company_full_mktcap', ascending=False)
        
        MIEU['QIR_Rank'] = [i for i in range(1,MIEU.shape[0]+1)] 
            
        
        
        QIR_MSSC = OutputUpdateSegmNbComp[mkt]['InterimData'].loc['InterimMSSC'].iloc[0]*1e+6
        QIR_MSnbC = OutputUpdateSegmNbComp[mkt]['InterimData'].loc['InterimMSnbC'].iloc[0]
        
        MIEU['QIR_MSSC']=QIR_MSSC
        MIEU['QIR_MSnbC']=QIR_MSnbC
        MIEU['Iter']=float("NaN")
        MIEU['Dist_1']=float("NaN")
        MIEU['Dist_2']=float("NaN")
    
     
        # Step1: STD & NEITHER > 100%  x QIR MSSC
        Iter1_List = (((MIEU['Status']=='STD') | (MIEU['Status']=='STD_SHADOW')) & (MIEU['company_full_mktcap']>=QIR_MSSC)).tolist()
        MIEU.loc[Iter1_List,'Iter']=1
        Iter1b_List = ((MIEU['Status']=='STD') | (MIEU['Status']=='STD_SHADOW')).tolist()
        MIEU.loc[Iter1b_List ,'Dist_1']= QIR_MSSC / MIEU.loc[Iter1b_List,'company_full_mktcap']-1
              
        # Step2: SC  > 180%  x QIR MSSC
        Iter2_List = ( (MIEU['Status']=='SML')  & (MIEU['company_full_mktcap']>= 1.8 * QIR_MSSC) ).tolist()
        MIEU.loc[Iter2_List,'Iter']=2
        Iter2b_List = ((MIEU['Status']=='SML') ).tolist()
        MIEU.loc[Iter2b_List ,'Dist_1'] = ((1.8 * QIR_MSSC) / MIEU.loc[Iter2b_List,'company_full_mktcap']) -1
        
        # Step3: STD & NEITHER > 50%  x QIR MSSC
        Iter3_List = (((MIEU['Status']=='STD') | (MIEU['Status']=='STD_SHADOW')) & (MIEU['company_full_mktcap']>= 0.5 * QIR_MSSC) & (MIEU['company_full_mktcap'] <  QIR_MSSC) ).tolist()
        MIEU.loc[Iter3_List,'Iter']=4
        Iter3b_List = ((MIEU['Status']=='STD') | (MIEU['Status']=='STD_SHADOW')).tolist()
        MIEU.loc[Iter3b_List ,'Dist_2'] = ((0.5 * QIR_MSSC) / MIEU.loc[Iter3b_List,'company_full_mktcap']) -1
            
        # Step4: SC > 100%  x QIR MSSC
        Iter4_List = ( (MIEU['Status']=='SML')  & (MIEU['company_full_mktcap']>= QIR_MSSC) & (MIEU['company_full_mktcap'] < 1.8 * QIR_MSSC) ).tolist()
        MIEU.loc[Iter4_List,'Iter']=5
        Iter4b_List = ((MIEU['Status']=='SML') ).tolist()
        MIEU.loc[Iter4b_List ,'Dist_2'] = (QIR_MSSC / MIEU.loc[Iter4b_List,'company_full_mktcap']) -1
        
        MIEU= MIEU.sort_values(['Iter', 'company_full_mktcap'], ascending=[True, False])
        
        
        MIEU['Iter_Rank'] = [i for i in range(1,MIEU.shape[0]+1)] 
        MIEU.loc[MIEU['Iter'].isna(),'Iter_Rank']=float("NAN")
        
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','QIR_MSSC']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','QIR_MSSC']],on='msci_issuer_code',how='left')

        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','QIR_MSnbC']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','QIR_MSnbC']],on='msci_issuer_code',how='left')

        
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','QIR_Rank']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','QIR_Rank']],on='msci_issuer_code',how='left')

        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','CoverageFFMktCap']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','CoverageFFMktCap']],on='msci_issuer_code',how='left')
        
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','Iter']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','Iter']],on='msci_issuer_code',how='left')
                
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','Iter_Rank']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','Iter_Rank']],on='msci_issuer_code',how='left')
        
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','Dist_1']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','Dist_1']],on='msci_issuer_code',how='left')
        
        Market_SecurityData = pd.merge(Market_SecurityData,MIEU[['msci_issuer_code','Dist_2']],on='msci_issuer_code',how='left')
        Market_CompanyData = pd.merge(Market_CompanyData,MIEU[['msci_issuer_code','Dist_2']],on='msci_issuer_code',how='left')
        
        # Restructure the Output Dictionaries
        OutputSizeSegmentAssignment[mkt]={}
        OutputSizeSegmentAssignment[mkt]['MIEU']= MIEU
        OutputSizeSegmentAssignment[mkt]['Market_CompanyData']=Market_CompanyData
        OutputSizeSegmentAssignment[mkt]['Market_SecurityData']=Market_SecurityData
        
              
   
    return OutputSizeSegmentAssignment

