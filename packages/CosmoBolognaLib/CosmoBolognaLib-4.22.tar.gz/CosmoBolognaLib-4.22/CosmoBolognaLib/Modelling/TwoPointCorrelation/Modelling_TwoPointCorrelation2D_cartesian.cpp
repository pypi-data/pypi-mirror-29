/********************************************************************
 *  Copyright (C) 2016 by Federico Marulli and Alfonso Veropalumbo  *
 *  federico.marulli3@unibo.it                                      *
 *                                                                  *
 *  This program is free software; you can redistribute it and/or   * 
 *  modify it under the terms of the GNU General Public License as  *
 *  published by the Free Software Foundation; either version 2 of  *
 *  the License, or (at your option) any later version.             *
 *                                                                  *
 *  This program is distributed in the hope that it will be useful, *
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of  *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   *
 *  GNU General Public License for more details.                    *
 *                                                                  *
 *  You should have received a copy of the GNU General Public       *
 *  License along with this program; if not, write to the Free      *
 *  Software Foundation, Inc.,                                      *
 *  59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.       *
 ********************************************************************/

/**
 *  @file
 *  Modelling/TwoPointCorrelation/Modelling_TwoPointCorrelation_cartesian.cpp
 *
 *  @brief Methods of the class Modelling_TwoPointCorrelation_cartesian
 *
 *  This file contains the implementation of the methods of the class
 *  Modelling_TwoPointCorrelation_cartesian, used to model the 2D
 *  two-point correlation function in Cartesian coordinates
 *
 *  @authors Federico Marulli, Alfonso Veropalumbo
 *
 *  @authors federico.marulli3@unbo.it, alfonso.veropalumbo@unibo.it
 */


#include "Modelling_TwoPointCorrelation2D_cartesian.h"

using namespace cosmobl;


// ============================================================================================


void cosmobl::modelling::twopt::Modelling_TwoPointCorrelation2D_cartesian::set_fiducial_xiDM ()
{
  cout << endl; coutCBL << "Setting up the fiducial dark matter two-point correlation function model" << endl;

  const vector<double> rad = logarithmic_bin_vector(m_data_model.step, max(m_data_model.r_min, 1.e-4), min(m_data_model.r_max, 100.));
  vector<double> xiDM(m_data_model.step);
  
  if (m_data_model.sigmaNL==0) {  
    for (size_t i=0; i<(size_t)m_data_model.step; i++)
      xiDM[i] = m_data_model.cosmology->xi_DM(rad[i], m_data_model.method_Pk, m_data_model.redshift, m_data_model.output_root, m_data_model.NL, m_data_model.norm, m_data_model.k_min, m_data_model.k_max, m_data_model.aa, m_data_model.GSL, m_data_model.prec, m_data_model.file_par);
  }

  else {
    const vector<double> kk = logarithmic_bin_vector(m_data_model.step, max(m_data_model.k_min, 1.e-4), min(m_data_model.k_max, 500.));
    vector<double> Pk(m_data_model.step);
    for (size_t i=0; i<(size_t)m_data_model.step; i++)
      Pk[i] = m_data_model.cosmology->Pk_DeWiggle (kk[i], m_data_model.redshift, m_data_model.sigmaNL, m_data_model.output_root, m_data_model.norm, m_data_model.k_min, m_data_model.k_max, m_data_model.aa, m_data_model.prec);
    xiDM = Xi0(rad, kk, Pk);
  }

  m_data_model.func_xi = make_shared<glob::FuncGrid>(glob::FuncGrid(rad, xiDM, "Spline"));

  vector<double> xiDM_(m_data_model.step), xiDM__(m_data_model.step);

  auto integrand_ = [&] (const double rr) { 
    return m_data_model.func_xi->operator()(rr)*rr*rr;
  };

  auto integrand__ = [&] (const double rr) { 
    return m_data_model.func_xi->operator()(rr)*rr*rr*rr*rr;
  };

  for (size_t i=0; i<(size_t)m_data_model.step; i++) {
    xiDM_[i] = 3.*gsl::GSL_integrate_qag(integrand_, 0., rad[i])*pow(rad[i], -3);
    xiDM__[i] = 5.*gsl::GSL_integrate_qag(integrand__, 0., rad[i])*pow(rad[i], -5);
  }

  m_data_model.func_xi_ = make_shared<glob::FuncGrid>(glob::FuncGrid(rad, xiDM_, "Spline"));
  m_data_model.func_xi__ = make_shared<glob::FuncGrid>(glob::FuncGrid(rad, xiDM__, "Spline"));  
}


// ============================================================================================


void cosmobl::modelling::twopt::Modelling_TwoPointCorrelation2D_cartesian::set_model_dispersionModel (const double alpha_perp_value, const statistics::Prior alpha_perp_prior, const double alpha_par_value, const statistics::Prior alpha_par_prior, const double fsigma8_value, const statistics::Prior fsigma8_prior, const double bsigma8_value, const statistics::Prior bsigma8_prior, const double sigma12_value, const statistics::Prior sigma12_prior)
{
  // compute the fiducial dark matter two-point correlation function and associated quantities
  set_fiducial_xiDM();

  
  // ----- set the parameter of the model xi0_linear (implemented in ModelFunction.cpp) -----

  m_alpha_perp = make_shared<statistics::BaseParameter>(statistics::BaseParameter(alpha_perp_prior, "alpha_perp"));
  if (alpha_perp_value != par::defaultDouble)
    m_alpha_perp->fix(alpha_perp_value);

  m_alpha_par = make_shared<statistics::BaseParameter>(statistics::BaseParameter(alpha_par_prior, "alpha_par"));
  if (alpha_par_value != par::defaultDouble)
    m_alpha_par->fix(alpha_par_value);

  m_fsigma8 = make_shared<statistics::BaseParameter>(statistics::BaseParameter(fsigma8_prior, "f*sigma8"));
  if (fsigma8_value != par::defaultDouble)
    m_fsigma8->fix(fsigma8_value);

  m_bsigma8 = make_shared<statistics::BaseParameter>(statistics::BaseParameter(bsigma8_prior, "b*sigma8"));
  if (bsigma8_value != par::defaultDouble)
    m_bsigma8->fix(bsigma8_value);

  m_sigma12 = make_shared<statistics::BaseParameter>(statistics::BaseParameter(sigma12_prior, "sigma12"));
  if (sigma12_value != par::defaultDouble)
    m_sigma12->fix(sigma12_value);

  set_parameters({m_alpha_perp, m_alpha_par, m_fsigma8, m_bsigma8, m_sigma12});
  

  // input data used to construct the model
  auto inputs = make_shared<STR_data_model>(m_data_model);

  // construct the model
  m_model = make_shared<statistics::Model2D>(statistics::Model2D(&xi2D_dispersionModel, inputs)); 

}
