/*
 * Parameters.cpp
 *
 *  Created on: 31 Jan 2018
 *      Author: julianporter
 */

#include "Parameters.hpp"
#include <base.hpp>
#include <limits>


namespace pylame {

const std::vector<int> Parameters::rates{8,16,24,32,48,64,96,128,192,256};
const std::vector<int> Parameters::qualities{1,2,3,4,5,6,7};

template<typename T>
bool has(const std::vector<T> &vec,const T value) {
	return std::find(vec.begin(),vec.end(),value)!=vec.end();
}

Parameters::Parameters(int rate_, int quality_, bool boost_,bool compress_,float sigmas_,float range_) : rate(rate_), quality(quality_),boost(boost_),compress(compress_) {
	if(!has(rates,rate)) throw MP3Error("Bad rate parameter");
	if(!has(qualities,quality)) throw MP3Error("Bad quality parameter");
	if(compress) {
		sigmas=std::max<float>(0,sigmas_);
		range=std::max<float>(0,std::min<float>(1,sigmas_));
	}
	else {
		sigmas=0;
		range=0;
	}
	boostLimit=boost ? std::numeric_limits<float>::max() : 1.0;
}

float Parameters::boostFactor(const float factor) {
	return std::min<float>(factor,boostLimit);
}





} /* namespace pylame */

inline std::string b(bool x) {
	return (x) ? "on" : "off";
}

std::ostream & operator<<(std::ostream &o, pylame::Parameters &p) {
	o << "Sample rate " << p.sampleRate() << " kbps, ";
	o << "Quality " << p.conversionQuality() << " / 7, ";
	o << "Boost " << b(p.doBoost()) << ", Compression " << b(p.doCompression()) << std::endl;
	return o;
}
