import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process("analyzer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = 500

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
#    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

#inputFiles = 'file:../../EventFilter/test/output_10076.root'
#print(inputFiles)

process.source = cms.Source("PoolSource", 
                fileNames = cms.untracked.vstring(options.inputFiles)                )


process.options = cms.untracked.PSet(
                        SkipEvent = cms.untracked.vstring('ProductNotFound')
                        )

outfile = "output_qc8analyzer_10076.root"
process.source.fileNames.append('file:../../EventFilter/test/output_10076.root')
#process.source.fileNames.append('file:/eos/user/t/toakhter/QC8/output_step1.root')

process.TFileService = cms.Service("TFileService", fileName = cms.string(outfile))


process.analyzer = cms.EDAnalyzer("QC8Analyzer",
                                     process.MuonServiceProxy,
                                     gemRecHitLabel = cms.InputTag("gemRecHits"),
                                     tracks = cms.InputTag("GEMTrackFinder"),
                                     trajs = cms.InputTag("GEMTrackFinder"),
                                     debug = cms.bool(True)
)

process.output = cms.OutputModule("PoolOutputModule",
                                  dataset = cms.untracked.PSet(
                                      dataTier = cms.untracked.string('RECO'),
                                      filterName = cms.untracked.string('')
                                  ),
                                  outputCommands=cms.untracked.vstring(
                                      "keep *",
                                      "drop FEDRawDataCollection_*_*_*"
                                  ),
                                  fileName=cms.untracked.string('output_10076.root'),
                                  splitLevel = cms.untracked.int32(0)
)


process.p = cms.Path(process.analyzer)
process.outpath = cms.EndPath(process.output)
