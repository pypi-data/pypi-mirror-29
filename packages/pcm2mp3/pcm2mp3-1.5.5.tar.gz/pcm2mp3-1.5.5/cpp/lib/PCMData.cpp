/*
 * PCMData.cpp
 *
 *  Created on: 16 Jan 2018
 *      Author: julianporter
 */



#include "PCMData.hpp"
#include <cmath>

using namespace pylame::pcm;

void PCMData::normaliseArray(float * ptr) {
	auto bounds=std::minmax_element(ptr,ptr+nSamples);
	auto min=*bounds.first;
	auto max=*bounds.second;
	auto bound=std::max(fabs(min),fabs(max));
	if(bound==0.0) return;
	auto scale=1.0/bound;
	for(unsigned i=0;i<nSamples;i++) ptr[i]*=scale;
}
