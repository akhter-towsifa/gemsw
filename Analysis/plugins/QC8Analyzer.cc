//system include files
#include <assert.h>
#include <memory>
#include <cmath>
#include <iostream>
#include <sstream>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH

//user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"

#include "TrackingTools/TrajectoryState/interface/TrajectoryStateTransform.h"
#include "TrackingTools/PatternTools/interface/Trajectory.h"

//GEM
#include "DataFormats/GEMDigi/interface/GEMDigiCollection.h"
#include "DataFormats/GEMRecHit/interface/GEMRecHitCollection.h"
#include "DataFormats/GEMRecHit/interface/GEMSegmentCollection.h"
#include "DataFormats/MuonDetId/interface/GEMDetId.h"

#include "Geometry/GEMGeometry/interface/GEMGeometry.h"
#include "Geometry/GEMGeometry/interface/GEMEtaPartition.h"
#include "Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h"
#include "Geometry/CommonTopologies/interface/GEMStripTopology.h"

//Muon
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"
#include "DataFormats/TrackingRecHit/interface/KfComponentsHolder.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"

//Root
#include "TH1D.h"
#include "TH2D.h"
#include "TProfile.h"
#include "TString.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "TTree.h"

using namespace std;
using namespace edm;

struct QC8Data
{
  void init();
  TTree* book(TTree *t);//, int branch_type);
  //branch names and their type will be declared here 
};

void QC8Data::init()
{//branch default values to be initiated here
}

TTree* QC8Data::book(TTree *t){//, int branch_type){
  edm::Service< TFileService > fs;
  //if (branch_type==1){
  t = fs->make<TTree>("analyzer", "analyzer");
  //}
  /*else if (branch_type==2){
    t = fs->make<TTree>("plots", "plots");
  }
  else {std::cout << "branch number not one of the two listed ones" << std::endl;}
  */

  //tree and branches to be listed here
  return t;
}


class QC8Analyzer : public edm::one::EDAnalyzer<> {
public:
  explicit QC8Analyzer(const edm::ParameterSet&);
  ~QC8Analyzer(){};

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginJob();
  virtual void endJob();

  //functions

  //member data
  edm::EDGetTokenT<reco::TrackCollection> tracks_;
  edm::EDGetTokenT<vector<Trajectory>> trajs_;
  edm::EDGetTokenT<GEMRecHitCollection> gemRecHits_;
  edm::ESGetToken<GEMGeometry, MuonGeometryRecord> GEMGeom_;
  edm::ESGetToken<GEMGeomtery, MuonGeometryRecord> GEMGeomBeginRun_;

  edm::Service<TFileService> fs;
  
  bool debug;

  QC8Data data_;
  TTree* analyzer;
};

QC8Analyzer::QC8Analyzer(const edm::ParameterSet& iConfig)
  : GEMGeom_(esConsumes()),
    GEMGeomBeginRun_(esConsumes<edm::Transition::BeginRun>())
{
  if (debug) {std::cout << "Begin QC8Analyzer" <<std::endl;}
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");

  tracks_ = consumes<reco::TrackCollection(iConfig.getParameter<edm::InputTag>("tracks"));
  trajs_ = consumes<vector<Trajectory>>(iConfig.getParameter<edm::InputTag>("trajs"));
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHitLabel"));
  debug = iConfig.getParameter<bool>("debug");
}

void QC8TrackValidation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::ESHandle<GEMGeometry> GEMGeom = iSetup.getHandle(GEMGeom_);
  const GEMGeometry* GEMGeometry_ = &*GEMGeom;

  edm::Handle<vector<reco::Track>> tracks;
  iEvent.getByToken(tracks_, tracks);

  edm::Handle<vector<Trajectory>> trajs;
  iEvent.getByToken(trajs_, trajs);

  edm::Handle<GEMRecHitCollection> gemRecHits;
  iEvent.getByToken(gemRecHits_, gemRecHits);

  std::map<GEMDetId, TrajectoryStateOnSurface> tsosMap;
  for (std::vector<reco::Track>::const_iterator track = tracks->begin(); track != tracks->end(); ++track){

  }

}
