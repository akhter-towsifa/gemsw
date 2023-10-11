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
#include "TString.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "TTree.h"

using namespace std;
using namespace edm;

struct QC8Data
{
  void init();
  TTree* book(TTree *t);
  //==========Muon Info==========
  //int muon_charge;
  //float muon_pt;
  //==========Track Info=========
  float track_chi2;  
  int CSC_location[5];
  int CSC_strip;
  //========RecHit Info=========
  float rechit_LP[3];
  float rechit_GP[3];
  int rechit_CLS;
  int rechit_detId;
  int rechit_location[5];
};

void QC8Data::init()
{
  //The variables are initiated at a high value (e.g. 999999) as a default value
  //==========Muon Info==========
  //muon_charge = 9999;
  //muon_pt = 999999;
  //==========Track Info=========
  track_chi2 = 999999;
  for (int i=0; i<5; ++i){
    CSC_location[i] = 999999;
  }
  CSC_strip = 999999;
  //========RecHit Info=========
  for (int i=0; i<3; ++i){
    rechit_GP[i] = 999999;
    rechit_LP[i] = 999999;
  }
  rechit_CLS = 999999;
  rechit_detId = 999999;
  for (int i=0; i<5; ++i){
    rechit_location[i] = 999999;
  }
}

TTree* QC8Data::book(TTree *t){
  edm::Service< TFileService > fs;
  t = fs->make<TTree>("analyzer", "analyzer");

  //==========Muon Info==========
  //t->Branch("muon_charge", &muon_charge);
  //t->Branch("muon_pt", &muon_pt);
  //==========Track Info=========
  t->Branch("track_chi2", &track_chi2);
  t->Branch("CSC_location", &CSC_location, "CSC_location[5] (reg, sta, cha, lay, rol)/I");
  t->Branch("CSC_strip", &CSC_strip);
  //========RecHit Info=========
  t->Branch("rechit_LP", &rechit_LP, "rechit_LP[3] (x,y,z)/F");
  t->Branch("rechit_GP", &rechit_GP, "rechit_GP[3] (x,y,z)/F");
  t->Branch("rechit_CLS", &rechit_CLS);
  t->Branch("rechit_detId", &rechit_detId);
  t->Branch("rechit_location", &rechit_location, "rechit_location[5] (reg, sta, cha, lay, rol)/I");

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
  //edm::Handle<vector<reco::TrackCollection>> tracks;
  edm::EDGetTokenT<vector<Trajectory>> trajs_;
  edm::EDGetTokenT<GEMRecHitCollection> gemRecHits_;
  edm::ESHandle<GEMGeometry> GEMGeometry_;
  const edm::ESGetToken<GEMGeometry, MuonGeometryRecord> GEMGeom_;
  const edm::ESGetToken<GEMGeometry, MuonGeometryRecord> GEMGeomBeginRun_;

  edm::Service<TFileService> fs;
  MuonServiceProxy* theService_;
  //edm::ESHandle<vector<reco::TrackCollection>> tracks;
  
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
  theService_ = new MuonServiceProxy(serviceParameters, consumesCollector());

  tracks_ = consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("tracks"));
  trajs_ = consumes<vector<Trajectory>>(iConfig.getParameter<edm::InputTag>("trajs"));
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHitLabel"));
  debug = iConfig.getParameter<bool>("debug");

  //tracks = iConfig.getParameter<edm::InputTag>("tracks");
}

void QC8Analyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::ESHandle<GEMGeometry> GEMGeom = iSetup.getHandle(GEMGeom_);
  const GEMGeometry* GEMGeometry_ = &*GEMGeom;

  edm::Handle<vector<reco::Track>> tracks;
  iEvent.getByToken(tracks_, tracks);

  edm::Handle<vector<Trajectory>> trajs;
  iEvent.getByToken(trajs_, trajs);

  edm::Handle<GEMRecHitCollection> gemRecHits;
  iEvent.getByToken(gemRecHits_, gemRecHits);

  TTree* tree;

  std::map<GEMDetId, TrajectoryStateOnSurface> tsos_Map;
  for (std::vector<reco::Track>::const_iterator track = tracks->begin(); track != tracks->end(); ++track){
    data_.init();
    data_.track_chi2 = track->normalizedChi2();

    auto traj = trajs->begin();
    for (auto traj_measurements : traj->measurements()) {
      auto tsos = traj_measurements.predictedState();
      auto rechit = traj_measurements.recHit();
      auto GEMID = GEMDetId(rechit->geographicalId());
      tsos_Map[GEMID] = tsos;
    }

    for (auto hit : track->recHits()){
      auto etaPart = GEMGeometry_->etaPartition(hit->geographicalId());
      auto etaPartId = etaPart->id();

      if (tsos_Map.find(etaPartId) == tsos_Map.end()) continue;
      auto tsos = tsos_Map[etaPartId];

      auto track_LP = tsos.localPosition();
      //auto track_LP_x = tsos.localPosition().x();

      auto reg = etaPartId.region();
      auto st = etaPartId.station();
      auto ch = etaPartId.chamber();
      auto lay = etaPartId.layer();
      auto iEta = etaPartId.ieta();
      //int rechit_CLS;
      //rechit_CLS = hit->clusterSize();

      auto rechit_GP_x = etaPart->toGlobal((hit)->localPosition()).x();
      auto rechit_LP_x = (hit)->localPosition().x();

      if (debug) std::cout << "rechit x GP:LP " << rechit_GP_x << ":" << rechit_LP_x << endl;

      auto strip = int(etaPart->strip(track_LP));
      int module = (16 - iEta)/4 + 1 + (2 - lay)*4;
      int sector = 1 - ((16 - iEta) % 4 / 2);
      if (debug) std::cout << "GEM region:station:chamber:layer:iEta " << reg << ":" << st << ":" << ch << ":" << lay << ":" << iEta << std::endl;
      if (debug) std::cout << "strip:module:sector " << strip << ":" << module << ":" << sector <<std::endl;
    }
    
    tree->Fill();
  }

}


void QC8Analyzer::beginJob(){}
void QC8Analyzer::endJob(){}

DEFINE_FWK_MODULE(QC8Analyzer);
