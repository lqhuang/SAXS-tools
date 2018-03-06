'''
Created on Jul 16, 2010

@author: Soren Nielsen

#******************************************************************************
# This file is part of RAW.
#
#    RAW is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RAW is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RAW.  If not, see <http://www.gnu.org/licenses/>.
#
#******************************************************************************
'''
import wx, cPickle, copy, os
import RAWGlobals, SASFileIO

class RawGuiSettings:
    '''
    This object contains all the settings nessecary for the GUI.

    '''
    def __init__(self, settings = None):
        '''
        Accepts a dictionary argument for the parameters. Uses default is no settings are given.
        '''

        self._params = settings

        if settings == None:
            self._params = {
                            #'NormalizeConst'    : [1.0,   wx.NewId(), 'float'],
                            #'NormalizeConstChk' : [False, wx.NewId(),  'bool'],
                            #'NormalizeM2'       : [False, wx.NewId(),  'bool'],
                            #'NormalizeTime'     : [False, wx.NewId(),  'bool'],
                            #'NormalizeM1'       : [False, wx.NewId(),  'bool'],

							'NormFlatfieldEnabled'	: [False,   wx.NewId(),  'bool'],

                            'NormAbsWater'      	: [False,   wx.NewId(),  'bool'],
                            'NormAbsWaterI0'    	: [0.01632, wx.NewId(),  'float'],
                            'NormAbsWaterTemp'  	: ['25',    wx.NewId(),  'choice'],
                            'NormAbsWaterConst' 	: [1.0,     wx.NewId(),  'float'],

                            'NormalizeTrans'    : [False, wx.NewId(),  'bool'],
                            'Calibrate'         : [False, wx.NewId(),  'bool'],  # Calibrate AgBe
                            'CalibrateMan'      : [True, wx.NewId(),  'bool'],  # Calibrate manual (wavelength / distance)
                            'AutoBgSubtract'    : [False, wx.NewId(),  'bool'],
                            'CountNormalize'    : [1.0,   wx.NewId(), 'float'],

                            'AutoBIFT'          : [False, wx.NewId(), 'bool'],
                            'AutoAvg'           : [False, wx.NewId(), 'bool'],
                            'AutoAvgRemovePlots': [False, wx.NewId(), 'bool'],

                            'AutoAvgRegExp'     : ['', wx.NewId(), 'text'],
                            'AutoAvgNameRegExp' : ['', wx.NewId(), 'text'],
                            'AutoAvgNoOfFrames' : [1,  wx.NewId(),  'int'],
                            'AutoBgSubRegExp'   : ['', wx.NewId(), 'text'],

                            'UseHeaderForMask': [False, wx.NewId(), 'bool'],
                            'DetectorFlipped90':[False, wx.NewId(), 'bool'],

                            #CORRECTIONS
                            'DoSolidAngleCorrection' : [True, wx.NewId(), 'bool'],


                            #CENTER / BINNING
                            'Binsize'    : [1,     wx.NewId(), 'int'],
                            'Xcenter'    : [512.0, wx.NewId(), 'float'],
                            'Ycenter'    : [512.0, wx.NewId(), 'float'],
                            'QrangeLow'  : [25,    wx.NewId(), 'int'],
                            'QrangeHigh' : [9999,  wx.NewId(), 'int'],
                            'StartPoint' : [0,     wx.NewId(), 'int'],
                            'EndPoint'   : [0,     wx.NewId(), 'int'],
                            'ImageDim'   : [[1024,1024]],

                            #MASKING
                            'SampleFile'              : [None, wx.NewId(), 'text'],
                            'BackgroundSASM'          : [None, wx.NewId(), 'text'],

                            'DataSECM'                : [None, wx.NewId(), 'text'],

                            'NormAbsWaterFile'        : [None, wx.NewId(), 'text'],
                            'NormAbsWaterEmptyFile'   : [None, wx.NewId(), 'text'],
							'NormFlatfieldFile'		  : [None, wx.NewId(), 'text'],

                            'TransparentBSMask'       : [None],
                            'TransparentBSMaskParams' : [None],
                            'BeamStopMask'            : [None],
                            'BeamStopMaskParams'      : [None],
                            'ReadOutNoiseMask'        : [None],
                            'ReadOutNoiseMaskParams'  : [None],
                                                                                #mask, mask_patches
                            'Masks'                   : [{'BeamStopMask'     : [None, None],
                                                          'ReadOutNoiseMask' : [None, None],
                                                          'TransparentBSMask': [None, None],
                                                         }],

                            'MaskDimension'          : [1024,1024],

                            #Q-CALIBRATION
                            'WaveLength'          : [1.0,  wx.NewId(), 'float'],
                            'SampleDistance'      : [1000, wx.NewId(), 'float'],
                            'SampleThickness'     : [0.0, wx.NewId(), 'float'],
                            'ReferenceQ'          : [0.0, wx.NewId(), 'float'],
                            'ReferenceDistPixel'  : [0,   wx.NewId(), 'int'],
                            'ReferenceDistMm'     : [0.0, wx.NewId(), 'float'],
                            'DetectorPixelSize'   : [70.5, wx.NewId(), 'float'],
                            'SmpDetectOffsetDist' : [0.0, wx.NewId(), 'float'],


							#SANS Parameters
							'SampleThickness'		: [0.1,  wx.NewId(), 'float'],
							'DarkCorrEnabled'		: [False,   wx.NewId(),  'bool'],
							'DarkCorrFilename'		: [None, wx.NewId(), 'text'],


                            #DEFAULT BIFT PARAMETERS
                            'maxDmax'     : [400.0,  wx.NewId(), 'float'],
                            'minDmax'     : [10.0,   wx.NewId(), 'float'],
                            'DmaxPoints'  : [10,     wx.NewId(), 'int'],
                            'maxAlpha'    : [1e10,   wx.NewId(), 'float'],
                            'minAlpha'    : [150.0,  wx.NewId(), 'float'],
                            'AlphaPoints' : [16,     wx.NewId(), 'int'],
                            'PrPoints'    : [50,     wx.NewId(), 'int'],

                            #DEFAULT pyGNOM PARAMETERS
                            'pygnomMaxAlpha'    : [60,   wx.NewId(), 'float'],
                            'pygnomMinAlpha'    : [0.01, wx.NewId(), 'float'],
                            'pygnomAlphaPoints' : [100,  wx.NewId(), 'int'],
                            'pygnomPrPoints'    : [50,   wx.NewId(), 'int'],
                            'pygnomFixInitZero' : [True, wx.NewId(), 'bool'],

                            'pyOSCILLweight'    : [3.0, wx.NewId(), 'float'],
                            'pyVALCENweight'    : [1.0, wx.NewId(), 'float'],
                            'pyPOSITVweight'    : [1.0, wx.NewId(), 'float'],
                            'pySYSDEVweight'    : [3.0, wx.NewId(), 'float'],
                            'pySTABILweight'    : [3.0, wx.NewId(), 'float'],
                            'pyDISCRPweight'    : [1.0, wx.NewId(), 'float'],

                            #DEFAULT IFT PARAMETERS:
                            'IFTAlgoList'        : [['BIFT', 'pyGNOM']],
                            'IFTAlgoChoice'      : [['BIFT']],

                            #ARTIFACT REMOVAL:
                            'ZingerRemovalRadAvg'    : [False, wx.NewId(), 'bool'],
                            'ZingerRemovalRadAvgStd' : [4.0,     wx.NewId(), 'float'],

                            'ZingerRemoval'     : [False, wx.NewId(), 'bool'],
                            'ZingerRemoveSTD'   : [4,     wx.NewId(), 'int'],
                            'ZingerRemoveWinLen': [10,    wx.NewId(), 'int'],
                            'ZingerRemoveIdx'   : [10,    wx.NewId(), 'int'],

                            'ZingerRemovalAvgStd'  : [8,     wx.NewId(), 'int'],
                            'ZingerRemovalAvg'     : [False, wx.NewId(), 'bool'],

                            #SAVE DIRECTORIES
                            'ProcessedFilePath'    : [None,  wx.NewId(), 'text'],
                            'AveragedFilePath'     : [None,  wx.NewId(), 'text'],
                            'SubtractedFilePath'   : [None,  wx.NewId(), 'text'],
                            'BiftFilePath'         : [None,  wx.NewId(), 'text'],
                            'GnomFilePath'         : [None,  wx.NewId(), 'text'],
                            'AutoSaveOnImageFiles' : [False, wx.NewId(), 'bool'],
                            'AutoSaveOnAvgFiles'   : [False, wx.NewId(), 'bool'],
                            'AutoSaveOnSub'        : [False, wx.NewId(), 'bool'],
                            'AutoSaveOnBift'       : [False, wx.NewId(), 'bool'],
                            'AutoSaveOnGnom'       : [False, wx.NewId(), 'bool'],

                            #IMAGE FORMATS
                            'ImageFormatList'      : [SASFileIO.all_image_types],
                            'ImageFormat'          : ['Pilatus', wx.NewId(), 'choice'],

                            #HEADER FORMATS
                            'ImageHdrFormatList'   : [SASFileIO.all_header_types],
                            'ImageHdrFormat'       : ['None', wx.NewId(), 'choice'],

                            'ImageHdrList'         : [None],
                            'FileHdrList'          : [None],

                            'UseHeaderForCalib'    : [False, wx.NewId(), 'bool'],

                            # Header bind list with [(Description : parameter key, header_key)]
                            'HeaderBindList'       : [{'Beam X Center'            : ['Xcenter',           None, ''],
                                                       'Beam Y Center'            : ['Ycenter',           None, ''],
                                                       'Sample Detector Distance' : ['SampleDistance',    None, ''],
                                                       'Wavelength'               : ['WaveLength',        None, ''],
                                                       'Detector Pixel Size'      : ['DetectorPixelSize', None, '']}],
                                                       # 'Number of Frames'         : ['NumberOfFrames',    None, '']}],

                            'NormalizationList'    : [None, wx.NewId(), 'text'],
                            'EnableNormalization'  : [True, wx.NewId(), 'bool'],

                            'OnlineFilterList'     : [None, wx.NewId(), 'text'],
                            'EnableOnlineFiltering': [False, wx.NewId(), 'bool'],
                            'OnlineModeOnStartup'  : [False, wx.NewId(), 'bool'],
	                        'OnlineStartupDir'     : [None, wx.NewId(), 'text'],

                            'MWStandardMW'         : [0, wx.NewId(), 'float'],
                            'MWStandardI0'         : [0, wx.NewId(), 'float'],
                            'MWStandardConc'       : [0, wx.NewId(), 'float'],
                            'MWStandardFile'       : ['', wx.NewId(), 'text'],

                            #Initialize volume of correlation molecular mass values.
                            #Values from Rambo, R. P. & Tainer, J. A. (2013). Nature. 496, 477-481.
                            'MWVcType'             : ['Protein', wx.NewId(), 'choice'],
                            'MWVcAProtein'         : [1.0, wx.NewId(), 'float'], #The 'A' coefficient for proteins
                            'MWVcBProtein'         : [0.1231, wx.NewId(), 'float'], #The 'B' coefficient for proteins
                            'MWVcARna'             : [0.808, wx.NewId(), 'float'], #The 'A' coefficient for proteins
                            'MWVcBRna'             : [0.00934, wx.NewId(), 'float'], #The 'B' coefficient for proteins

                            #Initialize porod volume molecularm ass values.
                            'MWVpRho'              : [0.83*10**(-3), wx.NewId(), 'float'], #The density in kDa/A^3

                            #Initialize Absolute scattering calibration values.
                            #Default values from Mylonas & Svergun, J. App. Crys. 2007.
                            'MWAbsRhoMprot'         : [3.22*10**23, wx.NewId(), 'float'], #e-/g, # electrons per dry mass of protein
                            'MWAbsRhoSolv'          : [3.34*10**23, wx.NewId(), 'float'], #e-/cm^-3, # electrons per volume of aqueous solvent
                            'MWAbsNuBar'            : [0.7425, wx.NewId(), 'float'], #cm^3/g, # partial specific volume of the protein
                            'MWAbsR0'               : [2.8179*10**-13, wx.NewId(), 'float'], #cm, scattering lenght of an electron

                            'CurrentCfg'         : [None],
                            'CompatibleFormats'  : [['.rad', '.tiff', '.tif', '.img', '.csv', '.dat', '.txt', '.sfrm', '.dm3', '.edf',
                                                     '.xml', '.cbf', '.kccd', '.msk', '.spr', '.h5', '.mccd', '.mar3450', '.npy', '.pnm',
                                                      '.No', '.imx_0', '.dkx_0', '.dkx_1', '.png', '.mpa', '.ift', '.sub', '.fit', '.fir',
                                                      '.out', '.mar1200', '.mar2400', '.mar2300', '.mar3600', '.int', '.ccdraw'], None],


                            #SEC Settings:
                            'secCalcThreshold'      : [1.02, wx.NewId(), 'float'],

                            #GUI Settings:
                            'csvIncludeData'      : [None],
                            'ManipItemCollapsed'  : [False, wx.NewId(), 'bool'] ,
                            'CurrentFilePath'     : [None],


                            'DatHeaderOnTop'      : [False, wx.NewId(), 'bool'],
                            'PromptConfigLoad'    : [True, wx.NewId(), 'bool'],

                            #ATSAS settings:
                            'autoFindATSAS'       : [True, wx.NewId(), 'bool'],
                            'ATSASDir'            : ['', wx.NewId(), 'bool'],

                            #GNOM settings
                            'gnomExpertFile'        : ['', wx.NewId(), 'text'],
                            'gnomForceRminZero'     : ['Y', wx.NewId(), 'choice'],
                            'gnomForceRmaxZero'     : ['Y', wx.NewId(), 'choice'],
                            'gnomNPoints'           : [171, wx.NewId(), 'int'],
                            'gnomInitialAlpha'      : [0.0, wx.NewId(), 'float'],
                            'gnomAngularScale'      : [1, wx.NewId(), 'int'],
                            'gnomSystem'            : [0, wx.NewId(), 'int'],
                            'gnomFormFactor'        : ['', wx.NewId(), 'text'],
                            'gnomRadius56'          : [-1, wx.NewId(), 'float'],
                            'gnomRmin'              : [-1, wx.NewId(), 'float'],
                            'gnomFWHM'              : [-1, wx.NewId(), 'float'],
                            'gnomAH'                : [-1, wx.NewId(), 'float'],
                            'gnomLH'                : [-1, wx.NewId(), 'float'],
                            'gnomAW'                : [-1, wx.NewId(), 'float'],
                            'gnomLW'                : [-1, wx.NewId(), 'float'],
                            'gnomSpot'              : ['', wx.NewId(), 'text'],
                            'gnomExpt'              : [0, wx.NewId(), 'int'],

                            #DAMMIF settings
                            'dammifMode'            : ['Fast', wx.NewId(), 'choice'],
                            'dammifSymmetry'        : ['P1', wx.NewId(), 'choice'],
                            'dammifAnisometry'      : ['Unknown', wx.NewId(), 'choice'],
                            'dammifUnit'            : ['Unknown', wx.NewId(), 'choice'],
                            'dammifChained'         : [False, wx.NewId(), 'bool'],
                            'dammifConstant'        : ['', wx.NewId(), 'text'],
                            'dammifOmitSolvent'     : [True, wx.NewId(), 'bool'],
                            'dammifDummyRadius'     : [-1, wx.NewId(), 'float'],
                            'dammifSH'              : [-1, wx.NewId(), 'int'],
                            'dammifPropToFit'       : [-1, wx.NewId(), 'float'],
                            'dammifKnots'           : [-1, wx.NewId(), 'int'],
                            'dammifCurveWeight'     : ['e', wx.NewId(), 'choice'],
                            'dammifRandomSeed'      : ['', wx.NewId(), 'text'],
                            'dammifMaxSteps'        : [-1, wx.NewId(), 'int'],
                            'dammifMaxIters'        : [-1, wx.NewId(), 'int'],
                            'dammifMaxStepSuccess'  : [-1, wx.NewId(), 'int'],
                            'dammifMinStepSuccess'  : [-1, wx.NewId(), 'int'],
                            'dammifTFactor'         : [-1, wx.NewId(), 'float'],
                            'dammifRgPen'           : [-1, wx.NewId(), 'float'],
                            'dammifCenPen'          : [-1, wx.NewId(), 'float'],
                            'dammifLoosePen'        : [-1, wx.NewId(), 'float'],
                            'dammifAnisPen'         : [-1, wx.NewId(), 'float'],
                            'dammifMaxBeadCount'    : [-1, wx.NewId(), 'int'],
                            'dammifReconstruct'     : [15, wx.NewId(), 'int'],
                            'dammifDamaver'         : [True, wx.NewId(), 'bool'],
                            'dammifDamclust'        : [False, wx.NewId(), 'bool'],
                            'dammifRefine'          : [True, wx.NewId(), 'bool'],
                            'dammifProgram'         : ['DAMMIF', wx.NewId(), 'choice'],

                            #DAMMIN settings that are not included in DAMMIF settings
                            'damminInitial'         : ['S', wx.NewId(), 'choice'], #Initial DAM
                            'damminKnots'           : [20, wx.NewId(), 'int'],
                            'damminConstant'        : [0, wx.NewId(), 'float'],
                            'damminDiameter'        : [-1, wx.NewId(), 'float'],
                            'damminPacking'         : [-1, wx.NewId(), 'float'],
                            'damminCoordination'    : [-1, wx.NewId(), 'float'],
                            'damminDisconPen'       : [-1, wx.NewId(), 'float'],
                            'damminPeriphPen'       : [-1, wx.NewId(), 'float'],
                            'damminCurveWeight'     : ['1', wx.NewId(), 'choice'],
                            'damminAnealSched'      : [-1, wx.NewId(), 'float'],

                            #Weighted Average Settings
                            'weightCounter'         : ['', wx.NewId(), 'choice'],
                            'weightByError'         : [True, wx.NewId(), 'bool'],
                            }

    def get(self, key):
        return self._params[key][0]

    def set(self, key, value):
        self._params[key][0] = value

    def getId(self, key):
        return self._params[key][1]

    def getType(self, key):
        return self._params[key][2]

    def getIdAndType(self, key):
        return (self._params[key][1], self._params[key][2])

    def getAllParams(self):
        return self._params



def fixBackwardsCompatibility(raw_settings):

    #Backwards compatibility for BindList:
    bind_list = raw_settings.get('HeaderBindList')
    for each_key in bind_list.keys():
        if len(bind_list[each_key]) == 2:
            bind_list[each_key] = [bind_list[each_key][0], bind_list[each_key][1], '']


def loadSettings(raw_settings, loadpath):

    file_obj = open(loadpath, 'rb')
    try:
        loaded_param = cPickle.load(file_obj)
    except (KeyError, EOFError, ImportError, IndexError, AttributeError, cPickle.UnpicklingError) as e:
        print 'Error type: %s, error: %s' %(type(e).__name__, e)
        file_obj.close()
        return False
    file_obj.close()

    keys = loaded_param.keys()
    all_params = raw_settings.getAllParams()

    for each_key in keys:
        if each_key in all_params:
            all_params[each_key][0] = copy.copy(loaded_param[each_key])
        else:
            print 'WARNING: ' + str(each_key) + " not found in RAWSettings."

    main_frame = wx.FindWindowByName('MainFrame')
    main_frame.queueTaskInWorkerThread('recreate_all_masks', None)

    postProcess(raw_settings)

    return True

def postProcess(raw_settings):
    fixBackwardsCompatibility(raw_settings)

    dir_check_list = [('AutoSaveOnImageFiles', 'ProcessedFilePath'), ('AutoSaveOnAvgFiles', 'AveragedFilePath'),
                    ('AutoSaveOnSub', 'SubtractedFilePath'), ('AutoSaveOnBift', 'BiftFilePath'),
                    ('AutoSaveOnGnom', 'GnomFilePath'), ('OnlineModeOnStartup', 'OnlineStartupDir')
                    ]

    file_check_list = [('NormFlatfieldEnabled', 'NormFlatfieldFile')]

    change_list = []

    message_dir = {'AutoSaveOnImageFiles'   : '- AutoSave processed image files',
                    'AutoSaveOnAvgFiles'    : '- AutoSave averaged files',
                    'AutoSaveOnSub'         : '- AutoSave subtracted files',
                    'AutoSaveOnBift'        : '- AutoSave BIFT files',
                    'AutoSaveOnGnom'        : '- AutoSave GNOM files',
                    'OnlineModeOnStartup'   : '- Start online mode when RAW starts',
                    'NormFlatfieldEnabled'  : '- Apply a flatfield correction'
                    }

    for item in dir_check_list:
        if raw_settings.get(item[0]):
            if not os.path.isdir(raw_settings.get(item[1])):
                raw_settings.set(item[0], False)
                change_list.append(item[0])

    for item in file_check_list:
        if raw_settings.get(item[0]):
            if not os.path.isfile(raw_settings.get(item[1])):
                raw_settings.set(item[0], False)
                change_list.append(item[0])

    text = ''
    for item in change_list:
        text = text + message_dir[item] +'\n'

    if len(change_list) > 0:
        wx.CallAfter(wx.MessageBox, 'The following settings have been disabled because the appropriate directory/file could not be found:\n'+text+'\nIf you are using a config file from a different computer please go into Advanced Options to change the settings, or save you config file to avoid this message next time.', 'Load Settings Warning', style = wx.ICON_ERROR | wx.OK | wx.STAY_ON_TOP)

    if raw_settings.get('autoFindATSAS'):
        main_frame = wx.FindWindowByName('MainFrame')
        main_frame.findAtsas()

    return

def saveSettings(raw_settings, savepath):
    param_dict = raw_settings.getAllParams()
    keys = param_dict.keys()

    exclude_keys = ['ImageFormatList', 'ImageHdrFormatList', 'BackgroundSASM', 'CurrentCfg', 'csvIncludeData', 'CompatibleFormats', 'DataSECM']

    save_dict = {}

    for each_key in keys:
        if each_key not in exclude_keys:
            save_dict[each_key] = param_dict[each_key][0]

    save_dict = copy.deepcopy(save_dict)

    #remove big mask arrays from the cfg file
    masks = save_dict['Masks']

    for key in masks.keys():
        masks[key][0] = None

    file_obj = open(savepath, 'wb')
    try:
        cPickle.dump(save_dict, file_obj, cPickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print '<Error> type: %s, message: %s' %(type(e).__name__, e)
        file_obj.close()
        return False

    file_obj.close()

    ## Make a backup of the config file in case of crash:
    backup_file = os.path.join(RAWGlobals.RAWWorkDir, 'backup.cfg')

    FileObj = open(backup_file, 'wb')
    try:
        cPickle.dump(save_dict, FileObj, cPickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print 'Error type: %s, error: %s' %(type(e).__name__, e)
        FileObj.close()
        return False
    FileObj.close()

    dummy_settings = RawGuiSettings()

    test_load = loadSettings(dummy_settings, savepath)

    if not test_load:
        os.remove(savepath)

    return test_load



# Table from http://physchem.kfunigraz.ac.at/sm/Services.htm
water_scattering_table = {0 : 0.01692,
                        1 : 0.01686,
                        2 : 0.01680,
                        3 : 0.01675,
                        4 : 0.01670,
                        5 : 0.01665,
                        6 : 0.01661,
                        7 : 0.01657,
                        8 : 0.01653,
                        9 : 0.01650,
                        10 : 0.01647,
                        11 : 0.01645,
                        12 : 0.01642,
                        13 : 0.01640,
                        14 : 0.01638,
                        15 : 0.01637,
                        16 : 0.01635,
                        17 : 0.01634,
                        18 : 0.01633,
                        19 : 0.01633,
                        20 : 0.01632,
                        21 : 0.01632,
                        22 : 0.01632,
                        23 : 0.01632,
                        24 : 0.01632,
                        25 : 0.01633,
                        26 : 0.01634,
                        27 : 0.01635,
                        28 : 0.01636,
                        29 : 0.01637,
                        30 : 0.01638,
                        31 : 0.01640,
                        32 : 0.01641,
                        33 : 0.01643,
                        34 : 0.01645,
                        35 : 0.01647,
                        36 : 0.01650,
                        37 : 0.01652,
                        38 : 0.01655,
                        39 : 0.01658,
                        40 : 0.01660,
                        41 : 0.01663,
                        42 : 0.01666,
                        43 : 0.01670,
                        44 : 0.01673,
                        45 : 0.01677,
                        46 : 0.01680,
                        47 : 0.01684,
                        48 : 0.01688,
                        49 : 0.01692,
                        50 : 0.01696,
                        51 : 0.01700,
                        52 : 0.01704,
                        53 : 0.01709,
                        54 : 0.01713,
                        55 : 0.01718,
                        56 : 0.01723,
                        57 : 0.01728,
                        58 : 0.01732,
                        59 : 0.01738,
                        60 : 0.01743,
                        61 : 0.01748,
                        62 : 0.01753,
                        63 : 0.01759,
                        64 : 0.01764,
                        65 : 0.01770,
                        66 : 0.01776,
                        67 : 0.01781,
                        68 : 0.01787,
                        69 : 0.01793,
                        70 : 0.01800,
                        71 : 0.01806,
                        72 : 0.01812,
                        73 : 0.01818,
                        74 : 0.01825,
                        75 : 0.01831,
                        76 : 0.01838,
                        77 : 0.01845,
                        78 : 0.01852,
                        79 : 0.01859,
                        80 : 0.01866,
                        81 : 0.01873,
                        82 : 0.01880,
                        83 : 0.01887,
                        84 : 0.01895,
                        85 : 0.01902,
                        86 : 0.01909,
                        87 : 0.01917,
                        88 : 0.01925,
                        89 : 0.01932,
                        90 : 0.01940,
                        91 : 0.01948,
                        92 : 0.01956,
                        93 : 0.01964,
                        94 : 0.01973,
                        95 : 0.01981,
                        96 : 0.01989,
                        97 : 0.01998,
                        98 : 0.02006,
                        99 : 0.02015,
                        100 : 0.02023}

