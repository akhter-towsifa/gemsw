import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process("QC8Analyzer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('MagneticField.Engine.uniformMagneticField_cfi')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('Configuration.StandardSequences.Services_cff')
#process.load('Configuration.EventContent.EventContent_cff')
process.load('gemsw.Geometry.GeometryQC8GE21_back_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi')
'''
process.gemGeometry.applyAlignment = cms.bool(True)
from Configuration.AlCa.GlobalTag import GlobalTag
print(process.GlobalTag)
process.GlobalTag.toGet = cms.VPSet(cms.PSet(record=cms.string("GEMChMapRcd"),
                                             tag=cms.string("GEMChMapRcd"),
                                             connect=cms.string("sqlite_fip:gemsw/EventFilter/data/GEMChMap_QC8.db")),
                                    cms.PSet(record = cms.string('GEMAlignmentRcd'),
                                             tag = cms.string("QC8GEMAlignment_test"),
                                             connect = cms.string("sqlite_fip:gemsw/Geometry/data/QC8GE21/QC8_GE21_FakeAlign.db")),
                                    cms.PSet(record = cms.string('GEMAlignmentErrorExtendedRcd'),
                                             tag = cms.string("QC8GEMAlignmentErrorExtended_test"),
                                             connect = cms.string("sqlite_fip:gemsw/Geometry/data/QC8GE21/QC8_GE21_FakeAlign.db")),
                                    cms.PSet(record=cms.string('GlobalPositionRcd'), tag = cms.string('IdealGeometry'))
)
'''
#process.SteppingHelixPropagatorAny.useMagVolumes = cms.bool(False)
#process.MuonServiceProxy.ServiceParameters.Propagators.append('StraightLinePropagator')

process.MessageLogger.cerr.FwkReport.reportEvery = 500

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource", 
                fileNames = cms.untracked.vstring(options.inputFiles),
                labelRawDataLikeMC = cms.untracked.bool(False)
)


process.options = cms.untracked.PSet(
                        SkipEvent = cms.untracked.vstring('ProductNotFound')
                        )

outfile = "output_qc8analyzer_10086.root"
process.source.fileNames.append('file:../../EventFilter/test/output_unpacker_10086.root')
#process.source.fileNames.append('file:/eos/user/t/toakhter/QC8/output_step1.root')


process.TFileService = cms.Service("TFileService", fileName = cms.string(outfile))


process.QC8Analyzer = cms.EDAnalyzer("QC8Analyzer",
                                     process.MuonServiceProxy,
                                     gemRecHitLabel = cms.InputTag("gemRecHits"),
                                     tracks = cms.InputTag("GEMTrackFinder"),
                                     trajs = cms.InputTag("GEMTrackFinder"),
                                     debug = cms.bool(True)
)

process.p = cms.Path(process.QC8Analyzer)
