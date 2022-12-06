class Dilution:
    def __init__(self):
        self._dilution_scheme = None
        self._analogue = ""
        self._assay_name = ""
        self._eln_num = ""
        self._stock_concentration = float(0)
        self._dil_factor_max = int(0)
        self._diluent_type = None
        self._diluent_species = "N/A"
        self._target_concentration = float(0)
        self._cal_dil_factor = float(0)
        self._aliquot_vol = float(0)
        self._aliquot_num = int(0)
        self._comment = None
        self._pre_dil_deadvol = None
        self._vol_pip_min = None
        self._max_vial_vol = None
        self._initials = ""
        self._labelDate = None
        self._predilPlasma_num = int(0)
        self._predilBuffer_num = int(0)
        self._cals_num = int(0)
        self._calsInBuffer = None
        self._diltype = None
        self._calsQCType = None
        
        
    @property
    def dilution_scheme(self):
        return self._dilution_scheme
        
    @dilution_scheme.setter    
    def dilution_scheme(self, value):
        self._dilution_scheme = value    
        
    @property
    def analogue(self):
         return self._analogue
        
    @analogue.setter    
    def analogue(self, value):
         self._analogue = value   
    
    @property
    def assay_name(self):
         return self._assay_name
    
    @assay_name.setter     
    def assay_name(self, value):
         self._assay_name = value   
    
    @property
    def eln_num(self):
         return self._eln_num
    
    @eln_num.setter     
    def eln_num(self, value):
         self._eln_num = value   
    
    @property
    def stock_concentration(self):
         return self._stock_concentration
    
    @stock_concentration.setter
    def stock_concentration(self, value):
         self._stock_concentration = value
   
    @property
    def dil_factor_max(self):
         return self._dil_factor_max

    @dil_factor_max.setter
    def dil_factor_max(self, value):
         self._dil_factor_max = value
    
    @property
    def diluent_type(self):
         return self._diluent_type
    
    @diluent_type.setter
    def diluent_type(self, value):
         self._diluent_type = value
    
    @property
    def diluent_species(self):
         return self._diluent_species
    
    @diluent_species.setter
    def diluent_species(self, value):
         self._diluent_species = value
    
    @property
    def target_concentration(self):
         return self._target_concentration
     
    @target_concentration.setter
    def target_concentration(self, value):
         self._target_concentration = value
    
    @property
    def cal_dil_factor(self):
         return self._cal_dil_factor
    
    @cal_dil_factor.setter
    def cal_dil_factor(self, value):
         self._cal_dil_factor = value
    
    @property
    def aliquot_vol(self):
         return self._aliquot_vol
    
    @aliquot_vol.setter
    def aliquot_vol(self, value):
         self._aliquot_vol = value
    
    @property
    def aliquot_num(self):
         return self._aliquot_num
   
    @aliquot_num.setter
    def aliquot_num(self, value):
         self._aliquot_num = value
    
    @property
    def comment(self):
         return self._comment

    @comment.setter
    def comment(self, value):
         self._comment = value.splitlines()
    
    @property
    def pre_dil_deadvol(self):
         return self._pre_dil_deadvol

    @pre_dil_deadvol.setter
    def pre_dil_deadvol(self, value):
         self._pre_dil_deadvol = value
    
    @property
    def vol_pip_min(self):
         return self._vol_pip_min

    @vol_pip_min.setter
    def vol_pip_min(self, value):
         self._vol_pip_min = value
    
    @property
    def max_vial_vol(self):
         return self._max_vial_vol

    @max_vial_vol.setter
    def max_vial_vol(self, value):
         self._max_vial_vol = value
            
    @property
    def initials(self):
         return self._initials
    @initials.setter
    def initials(self, value):
         self._initials = value
    
    @property
    def labelDate(self):
         return self._labelDate
    @labelDate.setter
    def labelDate(self, value):
         self._labelDate = value
            
    @property
    def predilPlasma_num(self):
         return self._predilPlasma_num
        
    @predilPlasma_num.setter
    def predilPlasma_num(self, value):
         self._predilPlasma_num = value
            
    @property
    def predilBuffer_num(self):
         return self._predilBuffer_num
    @predilBuffer_num.setter
    def predilBuffer_num(self, value):
         self._predilBuffer_num = value
    
    @property
    def calsInBuffer(self):
         return self._calsInBuffer
    @calsInBuffer.setter
    def calsInBuffer(self, value):
         self._calsInBuffer = value 
            
    @property
    def cals_num(self):
         return self._cals_num
        
    @cals_num.setter
    def cals_num(self, value):
         self._cals_num = value 
            
    @property
    def diltype(self):
         return self._diltype
        
    @diltype.setter
    def diltype(self, value):
         self._diltype = value 
            
    @property
    def calsQCType(self):
         return self._calsQCType
        
    @calsQCType.setter
    def calsQCType(self, value):
         self._calsQCType = value 
       
    def get_total_vol(self):
        if self._aliquot_vol and self._aliquot_num:
            return self._aliquot_vol*self._aliquot_num
        else:
            return 0
        
    #Removes s in 'Calibrators'    
    def get_calsQCType_in_singular(self):
        if self._calsQCType == 'Calibrators':
            return 'Calibrator'
        else:
            return _calsQCType

        
    def clear(self):
        self._dilution_scheme = None
        self._analogue = ""
        self._assay_name = ""
        self._eln_num = ""
        self._stock_concentration = float(0)
        self._dil_factor_max = int(0)
        self._diluent_type = None
        self._diluent_species = "N/A"
        self._target_concentration = float(0)
        self._cal_dil_factor = float(0)
        self._aliquot_vol = float(0)
        self._aliquot_num = int(0)
        self._comment = None
        self._pre_dil_deadvol = None
        self._vol_pip_min = None
        self._max_vial_vol = None
        self._initials = ""
        self._labelDate = None
        self._predilPlasma_num = int(0)
        self._predilBuffer_num = int(0)
        self._cals_num = int(0)
        self._calsInBuffer = None
        self._diltype = None
        self._calsQCType = None