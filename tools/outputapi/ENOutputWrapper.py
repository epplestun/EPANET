'''Wrapper for EPANET Output API.Author: Bryant E. McDonnellDate: 12/7/2015Language: Anglais'''from ctypes import *from _ENOutputToolkit import *#Used just to pull the Pointer of the ENResultsAPI structclass _Opaque(Structure):    '''    Used soley for passing the pointer to the enrapi struct to API    '''    passclass OutputObject:    def __init__(self, dllLoc):        '''        Instantiate python Wrapper Object and build Wrapper functions.        '''        try:            self.DLL = CDLL(dllLoc)        except:            raise Exception('Failed to Open Linked Library')        ###ENResultsAPI* DLLEXPORT ENR_alloc(void);        self._enrapiFunc = self.DLL.ENR_alloc        self._enrapiFunc.restype = POINTER(_Opaque)        ###int DLLEXPORT ENR_open(ENResultsAPI* enrapi, const char* path);        self._OpenFunc = self.DLL.ENR_open        self._OpenFunc.argtypes = [POINTER(_Opaque),POINTER(c_char)]        self._OpenFunc.restype = c_int                ###int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count);        self._GetNetSize = self.DLL.ENR_getNetSize        self._GetNetSize.argtypes = [POINTER(_Opaque), c_int, POINTER(c_int)]        self._GetNetSize.restype = c_int        ###int DLLEXPORT ENR_getUnits(ENResultsAPI* enrapi, ENR_Unit code, int* unitFlag);        self._GetUnits = self.DLL.ENR_getUnits        self._GetUnits.argtypes = [POINTER(_Opaque), c_int, POINTER(c_int)]        self._GetUnits.restype = c_int                ###int DLLEXPORT ENR_getTimes(ENResultsAPI* enrapi, ENR_Time code, int* time)        self._getTimes = self.DLL.ENR_getTimes        self._getTimes.argtypes = [POINTER(_Opaque), c_int, POINTER(c_int)]        self._getTimes.restype = c_int                ###float* ENR_newOutValueSeries(ENResultsAPI* enrapi, int seriesStart,        ###        int seriesLength, int* length, int* errcode);        self._newOutValueSeries = self.DLL.ENR_newOutValueSeries        self._newOutValueSeries.argtypes = [POINTER(_Opaque), c_int, c_int, POINTER(c_int), POINTER(c_int)]        self._newOutValueSeries.restype = POINTER(c_float)                ###float* ENR_newOutValueArray(ENResultsAPI* enrapi, ENR_ApiFunction func,        ###        ENR_ElementType type, int* length, int* errcode);        self._newOutValueArray = self.DLL.ENR_newOutValueArray        self._newOutValueArray.argtypes = [POINTER(_Opaque), c_int, c_int, POINTER(c_int), POINTER(c_int)]        self._newOutValueArray.restype = POINTER(c_float)        ###int DLLEXPORT ENR_getNodeSeries(ENResultsAPI* enrapi, int nodeIndex, ENR_NodeAttribute attr,        ###        int timeIndex, int length, float* outValueSeries, int* len);        self._getNodeSeries = self.DLL.ENR_getNodeSeries        self._getNodeSeries.argtypes = [POINTER(_Opaque), c_int, c_int, c_int, c_int, POINTER(c_float)]        self._getNodeSeries.restype = c_int                ###int DLLEXPORT ENR_getLinkSeries(ENResultsAPI* enrapi, int linkIndex, ENR_LinkAttribute attr,        ###        int timeIndex, int length, float* outValueSeries);        self._getLinkSeries = self.DLL.ENR_getLinkSeries        self._getLinkSeries.argtypes = [POINTER(_Opaque), c_int, c_int, c_int, c_int, POINTER(c_float)]        self._getLinkSeries.restype = c_int        ###int DLLEXPORT ENR_getNodeAttribute(ENResultsAPI* enrapi, int timeIndex,        ###        ENR_NodeAttribute attr, float* outValueArray);        self._getNodeAttribute = self.DLL.ENR_getNodeAttribute        self._getNodeAttribute.argtypes = [POINTER(_Opaque), c_int, c_int, POINTER(c_float)]        self._getNodeAttribute.restype = c_int        ###int DLLEXPORT ENT_getLinkAttribute(ENResultsAPI* enrapi, int timeIndex,        ###        ENR_LinkAttribute attr, float* outValueArray);        self._getLinkAttribute = self.DLL.ENR_getLinkAttribute        self._getLinkAttribute.argtypes = [POINTER(_Opaque), c_int, c_int, POINTER(c_float)]        self._getLinkAttribute.restype = c_int        ###int DLLEXPORT ENR_getNodeResult(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,        ###        float* outValueArray);        self._getNodeResult = self.DLL.ENR_getNodeResult        self._getNodeResult.argtypes = [POINTER(_Opaque), c_int, c_int,\                                          POINTER(c_float)]        self._getNodeResult.restype = c_int        ###int DLLEXPORT ENR_getLinkResult(ENResultsAPI* enrapi, int timeIndex, int linkIndex,        ###        float* outValueArray);        self._getLinkResult = self.DLL.ENR_getLinkResult        self._getLinkResult.argtypes = [POINTER(_Opaque), c_int, c_int,\                                          POINTER(c_float)]        self._getLinkResult.restype = c_int        ###int DLLEXPORT ENR_free(float *array);        self._free = self.DLL.ENR_free        self._free.argtypes = [POINTER(c_float)]        self._free.restype = c_int                ###int DLLEXPORT ENR_close(ENResultsAPI* enrapi);        self._CloseOut = self.DLL.ENR_close        self._CloseOut.argtypes = [POINTER(_Opaque)]        self._CloseOut.restype = c_int                ###int DLLEXPORT ENR_errMessage(int errcode, char* errmsg, int n);        self._RetErrMessage = self.DLL.ENR_errMessage        self._RetErrMessage.argtypes = [c_int, POINTER(c_char_p), c_int]        self._RetErrMessage.restype = c_int    def OpenOutputFile(self, binfile):        '''        1) Initializes the opaque pointer to enrapi struct.        2) Opens the output file.        '''        self.enrapi = self._enrapiFunc()        ret = self._OpenFunc(self.enrapi, binfile)        if ret != 0:            self.CloseOutputFile(self.enrapi)            raise Exception('Failed to open OutputFile')##Update Function at a later date##    def RaiseError(self, ErrNo):##        ErMsg = c_char_p(256)##        ##        self._RetErrMessage(ErrNo , ErMsg, 256)####        print ErMsg    def get_Units(self):        '''        Purpose: Returns pressure and flow units        '''        unit = c_int()        self._GetUnits(self.enrapi, ENR_flowUnits, unit)        self.flowUnits = unit.value        unit = c_int()        self._GetUnits(self.enrapi, ENR_pressUnits, unit)        self.pressUnits = unit.value                    def get_NetSize(self):        '''        Populates object attributes with the water object counts        '''        count = c_int()        self._GetNetSize(self.enrapi, ENR_nodeCount, byref(count))        self.nodeCount = count.value        count = c_int()        self._GetNetSize(self.enrapi, ENR_tankCount, byref(count))        self.tankCount = count.value        count = c_int()        self._GetNetSize(self.enrapi, ENR_linkCount, byref(count))        self.linkCount = count.value        count = c_int()        self._GetNetSize(self.enrapi, ENR_pumpCount, byref(count))        self.pumpCount = count.value        count = c_int()        self._GetNetSize(self.enrapi, ENR_valveCount, byref(count))        self.valveCount = count.value            def get_Times(self):        '''        Purpose: Returns report and simulation time related parameters.        '''        temp = c_int()        self._getTimes(self.enrapi, ENR_reportStart, byref(temp))        self.reportStart = temp.value        temp = c_int()        self._getTimes(self.enrapi, ENR_reportStep, byref(temp))        self.reportStep = temp.value                temp = c_int()        self._getTimes(self.enrapi, ENR_simDuration, byref(temp))        self.simDuration = temp.value        temp = c_int()        self._getTimes(self.enrapi, ENR_numPeriods, byref(temp))        self.numPeriods = temp.value    def get_NodeSeries(self, NodeInd, NodeAttr, SeriesStartInd = 0, SeriesLen = -1):        '''        Purpose: Get time series results for particular attribute. Specify series        start and length using seriesStart and seriesLength respectively.        SeriesLen = -1 Default input: Gets data from Series Start Ind to end                '''        if not hasattr(self, 'numPeriods'): self.get_Times()        if SeriesLen > self.numPeriods :            raise Exception("Outside Number of TimeSteps")        elif SeriesLen == -1:            SeriesLen = self.numPeriods                    sLength = c_int()        ErrNo1 = c_int()                    SeriesPtr = self._newOutValueSeries(self.enrapi, SeriesStartInd,\                                            SeriesLen, byref(sLength), byref(ErrNo1))        ErrNo2 = self._getNodeSeries(self.enrapi, NodeInd, NodeAttr, \                                  SeriesStartInd, sLength.value, SeriesPtr)        BldArray = [SeriesPtr[i] for i in range(sLength.value)]        self._free(SeriesPtr)        return BldArray    def get_LinkSeries(self, LinkInd, LinkAttr, SeriesStartInd = 0, SeriesLen = -1):        '''        Purpose: Get time series results for particular attribute. Specify series        start and length using seriesStart and seriesLength respectively.        SeriesLen = -1 Default input: Gets data from Series Start Ind to end                '''        if not hasattr(self, 'numPeriods'): self.get_Times()        if SeriesLen > self.numPeriods :            raise Exception("Outside Number of TimeSteps")        elif SeriesLen == -1:            SeriesLen = self.numPeriods                    sLength = c_int()        ErrNo1 = c_int()                    SeriesPtr = self._newOutValueSeries(self.enrapi, SeriesStartInd,\                                            SeriesLen, byref(sLength), byref(ErrNo1))        ErrNo2 = self._getLinkSeries(self.enrapi, LinkInd, LinkAttr, \                                  SeriesStartInd, sLength.value, SeriesPtr)        BldArray = [SeriesPtr[i] for i in range(sLength.value)]        ret = self._free(SeriesPtr)        return BldArray    def get_NodeAttribute(self, NodeAttr, TimeInd):        '''        Purpose: For all nodes at given time, get a particular attribute        '''        if not hasattr(self, 'nodeCount'): self.get_NetSize()        alength = c_int()        ErrNo1 = c_int()        ValArrayPtr = self._newOutValueArray(self.enrapi, ENR_getAttribute,\                                             ENR_node, byref(alength), byref(ErrNo1))        ErrNo2 = self._getNodeAttribute(self.enrapi, TimeInd, NodeAttr, ValArrayPtr)        BldArray = [ValArrayPtr[i] for i in range(alength.value)]        self._free(ValArrayPtr)        return BldArray    def get_LinkAttribute(self, LinkAttr, TimeInd):        '''        Purpose: For all links at given time, get a particular attribute        '''        if not hasattr(self, 'linkCount'): self.get_NetSize()        alength = c_int()        ErrNo1 = c_int()        ValArrayPtr = self._newOutValueArray(self.enrapi, ENR_getAttribute,\                                             ENR_link, byref(alength), byref(ErrNo1))        ErrNo2 = self._getLinkAttribute(self.enrapi, TimeInd, LinkAttr, ValArrayPtr)        BldArray = [ValArrayPtr[i] for i in range(alength.value)]        self._free(ValArrayPtr)        return BldArray    def get_NodeResult(self, NodeInd, TimeInd):        '''        Purpose: For a node at given time, get all attributes        '''        alength = c_int()        ErrNo1 = c_int()        ValArrayPtr = self._newOutValueArray(self.enrapi, ENR_getResult,\                                             ENR_node, byref(alength), byref(ErrNo1))        ErrNo2 = self._getNodeResult(self.enrapi, TimeInd, NodeInd, ValArrayPtr)        BldArray = [ValArrayPtr[i] for i in range(alength.value)]        self._free(ValArrayPtr)        return BldArray    def get_LinkResult(self, LinkInd, TimeInd):        '''        Purpose: For a link at given time, get all attributes        '''        alength = c_int()        ErrNo1 = c_int()        ValArrayPtr = self._newOutValueArray(self.enrapi, ENR_getResult,\                                             ENR_link, byref(alength), byref(ErrNo1))        ErrNo2 = self._getLinkResult(self.enrapi, TimeInd, LinkInd, ValArrayPtr)        BldArray = [ValArrayPtr[i] for i in range(alength.value)]        self._free(ValArrayPtr)        return BldArray           def CloseOutputFile(self):        '''        Call to close binary file.        '''        ret = self._CloseOut(self.enrapi)        if ret != 0:            raise Exception('Failed to Close *.out file')        if __name__ in "__main__":    dllLoc = 'outputAPI.dll'    binfile = 'C:\\PROJECTCODE\\EPANEToutputAPI\\Net3.out'        print("Testing Wrapper...")    print("Test Network 3...")    print("-->Instantiating DLL Object / Opening DLL")    self = OutputObject(dllLoc)    print("...Opened DLL")    print("\n-->Reading Binary File")    self.OpenOutputFile(binfile)    print("...Opened Bin File")    print("\n-->get_NodeSeries")    LENTest = -1    demands = self.get_NodeSeries(0,ENR_demand, 0, LENTest)    head = self.get_NodeSeries(0,ENR_head, 0, LENTest)    pressure = self.get_NodeSeries(0,ENR_pressure, 0, LENTest)    quality = self.get_NodeSeries(0,ENR_quality, 0, LENTest)    print('\t'.join(["ind","demand","head","pressure","quality"]))    for ind, val in enumerate(demands):        print ind, val, head[ind], pressure[ind], quality[ind]    print("\n-->get_LinkSeries")    flow = self.get_LinkSeries(0,ENR_flow)    velocity =self.get_LinkSeries(0,ENR_velocity)    headloss =self.get_LinkSeries(0,ENR_headloss)    avgQuality=self.get_LinkSeries(0,ENR_avgQuality)    status=self.get_LinkSeries(0,ENR_status)    setting=self.get_LinkSeries(0,ENR_setting)    rxRate=self.get_LinkSeries(0,ENR_rxRate)    frctnFctr =self.get_LinkSeries(0,ENT_frctnFctr)    print('\t'.join(["ind","flow","velocity","headloss","avgQuality",\                     "status","setting","rxRate","frctnFctr"]))    for ind, val in enumerate(flow):        print ind, val, velocity[ind],headloss[ind],avgQuality[ind],status[ind],setting[ind],rxRate[ind],frctnFctr[ind]    print("\n-->get_NodeAttribute")    demand_1 = self.get_NodeAttribute(ENR_demand,0)    head_1 = self.get_NodeAttribute(ENR_head,0)    pressure_1 = self.get_NodeAttribute(ENR_pressure,0)    quality_1 = self.get_NodeAttribute(ENR_quality,0)    print('\t'.join(["ind","demand","head","pressure","quality"]))    for ind, val in enumerate(demand_1):        print ind, val, head_1[ind], pressure_1[ind], quality_1[ind]    print("\n-->get_LinkAttribute")    flow1 = self.get_LinkAttribute(ENR_flow,0)    velocity1 =self.get_LinkAttribute(ENR_velocity,0)    headloss1 =self.get_LinkAttribute(ENR_headloss,0)    avgQuality1=self.get_LinkAttribute(ENR_avgQuality,0)    status1=self.get_LinkAttribute(ENR_status,0)    setting1=self.get_LinkAttribute(ENR_setting,0)    rxRate1=self.get_LinkAttribute(ENR_rxRate,0)    frctnFctr1 =self.get_LinkAttribute(ENT_frctnFctr,0)    print('\t'.join(["ind","flow","velocity","headloss","avgQuality",\                     "status","setting","rxRate","frctnFctr"]))    for ind, val in enumerate(flow1):        print ind, val, velocity1[ind],headloss1[ind],avgQuality1[ind],status1[ind],setting1[ind],rxRate1[ind],frctnFctr1[ind]    print("\n-->Object Counts")    print("Nodes")    print(self.nodeCount)    print("Nodes")    print(self.nodeCount)        print("Tanks")    print(self.tankCount)    print("Links")    print(self.linkCount)    print("Pumps")    print(self.pumpCount)    print("Values")    print(self.valveCount)             print("\n-->get_NodeResult")    print(self.get_NodeResult(96,24))    print("\n-->get_LinkResult")    print(self.get_LinkResult(0,0))        print("\n-->get_Units")    self.get_Units()    print("...flow unit code")    print(self.flowUnits)    print("...pressure unit code")    print(self.pressUnits)        print("\n-->Closing Binary File")    self.CloseOutputFile()    print("...Closed Binary File")                