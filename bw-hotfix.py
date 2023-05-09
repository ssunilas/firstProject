from datetime import datetime,date
import xml.etree.ElementTree as ET
import os
import os.path
import pdb
del pdb
# from jproperties import Properties
# configs = Properties()
import configparser
from configparser import ConfigParser
# config = configparser.RawConfigParser() 
from jproperties import Properties
configs = Properties()
import git



#eb_number
# workArea = "C:\bw-dev\"
# baseLineRelativePath = "product\installer\local\baseline\"
# bwIniFile = workArea+baseLineRelativePath+"tibco.home\bw\system\hotfix\bw\lib\bw.ini" 
bwIniFile = "'C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini"

isEbBuild = False

# def my_function(hii):
#   print(hii)

workArea = ''

def readFile():
      with open(r'C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini', 'r') as file:
       line =  file.read()
      #  print(line)
       return line

def writeFileContents(file,contents):
  file.write(contents)
  file.close()
  line = file.read()
  return line

#

def updateBwIniFile():
    contents = [readFile()]
    print("*****************************8")
    print(contents[0])
    print(len(contents[0]))
    print("*****************************8")

    localtime = datetime.now();
    
    counter=0;
    tHfVer = " ";
    
    if(isEbBuild == True):
        tHfVer="EB$eb_number"
    else:
        tHfVer="$hotfix_no";
        print("eb build number should be valid")
    while(counter < len(contents)):
        contents[counter] = contents[counter].replace("product.hf.version= ", "product.hf.version="+tHfVer)
        contents[counter] = contents[counter].replace("product.build= ", "product.build=V$build_no")
        contents[counter] = contents[counter].replace("product.build.date= ", "product.build.date="+str(localtime.date()))
        counter=counter+1

    print('updated bw.ini file:')
    # contents.append("()())()()()()()()()()()()()()()()()")
   

    for line in contents:
        print(line);
    # push the changes i.e write the contents changes into BW INI File
    # eg :writeFileContents('C:\bw-dev\product\installer\local\baseline\tibco.home\bw\system\hotfix\bw\lib\bw.ini',contents)



def updateFeatureXml(xmlFilePath,feature,version):
    
    path = repr(xmlFilePath)[1:-1]   #taking xmlFilePath as a raw string to open it
    #opening file and parsing it using XML parser 
    with open(path,'r') as fil:       
      content = fil.read()
      tree = ET.parse(fil.name)
      myroot = tree.getroot()
      #iterarting over the XML file and finding the given feature and returning its version
      for impor in myroot.iter('import'):          
          if(impor.attrib.get('feature') == feature):
            impor.set('version',version)
            print(impor.attrib.get('version'))
    #   tree.write(file.name)
    #  fil.close()

def optimizeRus(listOfRus):
    myFeatures = listOfRus.split(',')
    feature = myFeatures[0]
    print(feature)


def validateParamter(product_id, version, src_url, hotfix_no, workarea, build_no, is_eb_build, list_of_rus, eb_number, cleanup_target_files):
    productId = productId.strip()  
    version = version.strip()
    srcUrl = srcUrl.strip()
    hotfixNo = hotfixNo.strip()
    workArea = workArea.strip()
    buildNo = buildNo.strip()
    isBuildTrim = isBuildTrim.strip()
    listOfRus = listOfRus.strip()
    ebNumber = ebNumber.strip()
    cleanupTargetFiles = cleanupTargetFiles.strip()
    
    if(not hotfixNo.isdigit()):
        print("Please check value of hotfix number" + hotfixNo +" . It should be valid integer number")
        return
    elif(buildNo.isdigit()):
        print("Please check value of hotfix number" + buildNo +" . It should be valid integer number")
        return
    elif(isEbBuild.casefold() != 'true' or isEbBuild.casefold() != 'false'):
        print("Illegal choice for parameter " + isEbBuild + ", It should be either true or false.")
        return
    elif(not os.path.exists(workArea)):
         print("Please check value of workarea "+ workArea + ". It must be an existing directory")
         return
    elif(listOfRus):
        optimizeRus(listOfRus)

    pkg_path="/tsi/pkg/"+productId+"/"+version
    pkg_url="http://reldist.na.tibco.com/package/"+productId+"/"+version


 
def updateProductXmlFile(prodXmlPath,build,track):
    ceProdXml = repr(prodXmlPath)[1:-1]
    # adding current date
    localtime = date.today()
    #opens the file and parse it
    with open(ceProdXml,'r') as file:
        tree = ET.parse(file.name)
        myroot = tree.getroot()
        productTrack = myroot.attrib
        #updating the date,build abd track values
        myroot.set('date',localtime)
        myroot.set('build' , build)
        myroot.set('track',track)
        print(productTrack.get('version'))
        print(productTrack.get('build'))
        print(productTrack.get('track'))
    # tree.write(file.name)


def ifFeatureExists(featurePath):
    feature = repr(featurePath)[1:-1]
    print(feature)
    #check if feature exists if yes then return the version
    print(os.path.exists(feature))
    if(os.path.exists(feature)):
        print("yes")
        with open(feature,'r') as file:
          tree = ET.parse(file.name)
          myroot = tree.getroot() 
          productTrack = myroot.attrib
          return productTrack.get('version')
    else:
        print("no")
        return ''
    
 

def updateBuildPropertiesFile(buildFilePath):
    filePath = repr(buildFilePath)[1:-1]
    print(filePath)
    # config.add_section('[Section2]')
    # config.read(filePath)
    # print(config.sections)
    # parser = ConfigParser()
    # with open(filePath , 'r') as stream:
    #  parser.read_string("[top]\n" + stream.read())
    #  config.add_section('Section')
    #  user=config.get("Section", "bw.track.name")
    with open(filePath, 'rb') as config_file:
       configs.load(config_file)  
       items_view = configs.items()
       value = items_view.get('bw.track.shortName')
       print("*****" + value)
       for item in items_view:
         print(item[1].data) 
    # with open(filePath,'r') as fh:
    #  config.read_file(fh)
    # with open(buildFilePath, 'r') as file:
    #  content = file.read() 
    #  print(content)
    #  lin = file.readline()
 
    # config.add_section('Section')
    # value = config.get('','bw.track.shortName')
    # print(value)
    
    # with open(filePath, 'rb') as config_file:
        # configs.load(config_file)
        # print(configs.get("bw.track.name").data)
    #     config.set('bw.track.shortName', '6.9.1')
    #     print(configs.get("bw.track.shortName").data)
        # config.write(config_file)

def getFeatureVersion(featurePath) :
    feature = repr(featurePath)[1:-1]
    print(feature)
    print(os.path.exists(feature))
    if(os.path.exists(feature)):
        print("yes")
        with open(feature,'r') as file:
          tree = ET.parse(file.name)
          myroot = tree.getroot() 
          productTrack = myroot.attrib
          return productTrack.get('version')
    else:
        print("No Feature Exists")
        return ''

def setGlobalVariables():
     global workArea
     workArea = 'C:\\bw-dev'+"\\"

def updateXpdInFeactureConfig(filePath,featureName,version) :
     featurePath = repr(filePath)[1:-1]
     localtime = date.today()
     #open the xpd file and parse it and update the version of given feature
     with open(featurePath,'r') as file:
        tree = ET.parse(file.name)
        myroot = tree.getroot()
        for x in myroot.iter('assembly'):
         if(x.attrib.get('uid') == featureName ):
          if(x.attrib.get('version') == version):
              print("version of product assembly is same don't need to update")
          else :
              x.set('version',version)
              print(x.attrib.get('version'))
              print('version of the product assembly changes')
            
             
def setEcProperties(propertyName , value):
     if(value):
     #creates a command using arguments propertyName and Value
         command = "ectool" + " " + "setProperty"+ " "+ "/myJob/"+ propertyName + " " + value 
         print(command)
         #runs command from terminal
         os.system(command)
     else :
         print("noValue")
         

def build(filePath1):
    filePath = 'C:\\ec-projects\\python\\src\\BW\\conf\\rus_list_6.9.1.properties'
    featurePath = repr(filePath)[1:-1] 
 ### open the file and read it line by line 
    with open(featurePath,'r') as file:
         lin = file.readline() 
         # iterate through each line and checks whether line contains '=' and if it contains then we split it to get path
         for lin in file:
          if lin.__contains__("="):
            my_list = lin.split('=')
            runame = my_list[1]
         #create absolute path 
            absolultePath = workArea.strip()+runame.strip()
        #checks whether the absolute path exists or not
            if(os.path.exists(absolultePath)):
                print(my_list[0] + "   ***   " + "yes")
            else :
                print(my_list[0] + "   ***   " + "no")


def githubCheck():
    repo = git.Repo('bw-hotfix')
    print(repo.head.commit.parents)
    previous_commit = repo.head.commit.parents[0]
    diff = previous_commit.diff()
    if(diff):
        print("there are changes in prev commit");
    else:
        print('no commit')

githubCheck() 
#build('C:\\bw-dev\\build\\build_automation\\conf\\final_ru_list.txt')
#setEcProperties("nameOfProperty" , "valueofproperty")
#updateXpdInFeactureConfig('C:\\bw-dev\\pkg_info\\bom\\base\\featureConfigs\\contrib_bstudio_4.0.0_FeatureConfig.xml' , 'assembly_tibco_com_tibco_xpd_core_feature_p2' , '4.0.3301')
# updateBuildPropertiesFile('C:\\\bw-dev\\pkg_info\\bom\\hf1\\assemblies\\common\\build.properties')
#print(ifFeatureExists('C:\\bw-dev\\palettes\\design\\features\\com.tibco.bw.palette.design.feature\\feature.xml'))
#updateProductXmlFile('C:\\bw-dev\\palettes\\design\\features\\com.tibco.bw.palette.design.feature\\feature.xml','40','track')   
#validateParamter("1", "2", "url.com", "1", "c://", "2", "5", "rus", "eb_number", "cleanup_target_files") 
#validateParameter("1", "2", "url.com", "1", "c://", "2", "5", "rus", "eb_number", "cleanup_target_files")
#updateFeatureXml("C:\bw-dev\palettes\design\features\com.tibco.bw.palette.design.feature\feature.xml","com.tibco.zion.feature","1.3.3001")    

  
