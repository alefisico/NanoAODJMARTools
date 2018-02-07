#ifndef PhysicsTools_NanoAODToolsJMAR_Recluster_h
#define PhysicsTools_NanoAODToolsJMAR_Recluster_h

#include "fastjet/contrib/SoftDrop.hh"
#include "TLorentzVector.h"

#include <string>
#include <vector>

class SoftDropWrapper : fastjet::contrib::SoftDrop {
 public:
  SoftDropWrapper(float beta, float zcut, float R, float ptmin);
  SoftDropWrapper();

  std::vector<fastjet::PseudoJet> result( std::vector<TLorentzVector> const & jet );

 protected :
  float R_;
  float ptmin_;
};

#endif
