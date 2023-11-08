from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '10090_unpacked'
config.General.workArea = 'crab_projects'
config.General.transferLogs=False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qc8Unpack.py'

config.section_("Data")
config.Data.userInputFiles = ['./10090.list'] #open('10090.list').readlines()
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/toakhter/QC8'
config.Data.outputDatasetTag = config.General.requestName

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
