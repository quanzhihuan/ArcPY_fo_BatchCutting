# -*- coding: cp936 -*-
#
#�����ֶΣ��ӡ�����Ҫ�ء��������������������Ҫ�أ�����Ҫ��ЩҪ�زü���ԴҪ�ء���
# ���������ӣ��Խ������ͳ�Ʒ���
#
import os
import sys
import arcpy
import shutil
import traceback
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#�����ļ���
def mkdir(path):
    print(path)
    folder = os.path.exists(path)
    if not folder:  # �ж��Ƿ�����ļ�������������򴴽�Ϊ�ļ���
        os.makedirs(path)  # makedirs �����ļ�ʱ���·�������ڻᴴ�����·��

#ͨ���ļ����ƻ�ȡ�ļ�������׺
#def getNameAndEXName(filename):

if __name__=='__main__':
    try:
        #print('========�ű�����=========')
        #p = sys.argv[1]  # cmd ִ�д���Ľṹ�ǣ�python test.py 2 ���ԣ�argv[0]=test.py��argv[1]=2
        #ԴҪ��
        sc_Input=arcpy.GetParameterAsText(0)
        #����Ҫ�أ����������Ҫ��
        cf_Input=arcpy.GetParameterAsText(1)

        now = datetime.datetime.now()
        ts = now.strftime('%m-%d-%H-%M-%S')

        #������Ŀ¼
        envPath = os.path.dirname(os.path.dirname(cf_Input))
        arcpy.env.workspace = envPath
        outputClipLayerDirPath=envPath+"\\"+ts+"re\\clipLayer"
        #outputExcelDirPath=envPath+"\\"+ts+"re\\excel"
        mkdir(outputClipLayerDirPath)
        #mkdir(outputExcelDirPath)
        #print(inpath)

        #maindir:Ŀ¼ subdir:Ŀ¼�µ���Ŀ¼  file_name_list:�ļ���
        fileArr=[]
        for maindir, subdir, file_name_list in os.walk(envPath):
            # print(maindir)
            # print(subdir)
            # print(file_name_list)
            for fn in file_name_list:
                getfn = fn.split(".")
                if len(getfn) == 2 and "shp" in getfn:
                   fileArr.append(fn)
        arcpy.AddMessage('========��ȡ�ü�Ҫ��...=========')
        clipFeature_mainDir=envPath + "\\"+ts+"re\\clipLayer"
        clip_mainDir=arcpy.GetParameterAsText(3)
        #clip_mainDir = envPath + "\\" + ts + "re"
        # �ü�Ҫ���ֶ�����
        # theFields = arcpy.ListFields(sc_Input)
        # FieldsArray = []  # ȫ���ֶ���
        # for Field in theFields:
        #     FieldsArray.append(Field.name)
        # if "FID" in FieldsArray:
        #     clipFieldName = ["FID"]
        # else:
        #     clipFieldName = ["OBJECTID"]
        FieldsName=arcpy.GetParameterAsText(2)
        clipFieldName=[]
        clipFieldName.append(FieldsName)
        with arcpy.da.SearchCursor(cf_Input,clipFieldName) as cursor:
            for row in cursor:
                clip_layerName=r"�ü���Χ_"+str(row[0])
                clip_OutPath = clipFeature_mainDir+"\\"+ clip_layerName+ r".shp"
                # ������ʱͼ��,��һ����Ϊ��ʱͼ��·�����ڶ�������Ϊ��ʱͼ������
                featureLayer=arcpy.MakeFeatureLayer_management(cf_Input,"temp_"+clip_layerName)
                sql=clipFieldName[0]+r" = "+"'"+str(row[0])+"'"
                #print sql
                arcpy.SelectLayerByAttribute_management(featureLayer, "NEW_SELECTION",sql )
                #�����ü�Ҫ��
                arcpy.CopyFeatures_management(featureLayer, clip_OutPath)
            #�رգ�����shutil����
            del cursor, row

            arcpy.AddMessage('========���вü�...=========')
        for maindir, subdir, file_name_list in os.walk(clipFeature_mainDir):
            for fn in file_name_list:
                getfn = fn.split(".")
                if len(getfn) == 2 and "shp" in getfn:
                    # �ü�
                    arcpy.Clip_analysis(sc_Input, maindir+'\\'+fn, clip_mainDir+"\\��ɵ�"+fn)
        shutil.rmtree(envPath+"\\"+ts+"re")
    except:
        arcpy.AddError(traceback.format_exc())
        shutil.rmtree(envPath+"\\"+ts+"re")

