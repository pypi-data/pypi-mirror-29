/*
 * Parameters.hpp
 *
 *  Created on: 31 Jan 2018
 *      Author: julianporter
 */

#ifndef PARAMETERS_HPP_
#define PARAMETERS_HPP_


#include <vector>
#include <iostream>

namespace pylame {

class Parameters {
private:
	const static std::vector<int> rates;
	const static std::vector<int> qualities;
	int rate;
	int quality;
	bool boost;
	bool compress;
	float sigmas;
	float range;
	float boostLimit;
public:

	Parameters(int rate_=32, int quality_=5, bool boost_=true,bool compress = false,float sigmas=1.0,float range=0.8);
	virtual ~Parameters() = default;


	int sampleRate() { return rate; };
	int conversionQuality() { return quality; };
	bool doBoost() { return boost; };
	float boostFactor(const float factor);
	bool doCompression() { return compress; };
	float compressionSigmas() { return sigmas; };
	float compressionRange() { return range; };

};




} /* namespace pylame */

std::ostream & operator<<(std::ostream &o, pylame::Parameters &p);

#endif /* PARAMETERS_HPP_ */
