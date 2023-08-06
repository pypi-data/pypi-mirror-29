/*
 * Effect.cpp
 *
 *  Created on: 8 Feb 2018
 *      Author: julianporter
 */

#include "Effect.hpp"
#include <cmath>
#include <numeric>
#include <limits>

namespace pylame {
namespace pcm {



void Normalise::operator()(const unsigned nChannels,const unsigned length,float *buffers[]) {
	for(unsigned channel=0;channel<nChannels;channel++) {
		auto ptr=buffers[channel];
		auto bounds=std::minmax_element(ptr,ptr+length);
		auto min=*bounds.first;
		auto max=*bounds.second;
		auto bound=std::max(fabs(min),fabs(max));
		if(bound>0.0) {
			auto scale=parameters.boostFactor(1.0/bound);
			for(unsigned i=0;i<length;i++) ptr[i]*=scale;
		}
	}
}

void Compress::operator()(const unsigned nChannels,const unsigned length,float *buffers[]) {
	if(!parameters.doCompression()) return;

	for(unsigned channel=0;channel<nChannels;channel++) {
		auto array=buffers[channel];
		float mean=std::accumulate(array,array+length,0.0)/(float)length;
		float variance=std::accumulate(array,
					array+length,
					0.0,
					[mean](auto partial,auto sample) {
						return partial+(sample-mean)*(sample-mean);
					})/(float)length;
		float sigma = sqrtf(variance);

		float lower=std::max<float>(0.0,mean-parameters.compressionSigmas()*sigma);
		float upper=std::min<float>(1.0,mean+parameters.compressionSigmas()*sigma);
		float yLower=(1.0-parameters.compressionRange())/2.0;
		float yUpper=(1.0+parameters.compressionRange())/2.0;
		float gLower = (lower==0.0) ? 0 : yLower/lower;
		float gUpper = (upper==1.0) ? 0 : yLower/(1.0-upper);
		float gMid = parameters.compressionRange()/(upper-lower);

		for(unsigned i=0;i<length;i++) {
			auto a=array[i];
			float s=a>0 ? 1.0 : -1.0;
			auto d=fabs(a);
			array[i] = s*((d<lower) ? d*gLower : (
					(d>upper) ? (d-upper)*gUpper+yUpper : (d-lower)*gMid+yLower
				));
		}
	}
}


}}
