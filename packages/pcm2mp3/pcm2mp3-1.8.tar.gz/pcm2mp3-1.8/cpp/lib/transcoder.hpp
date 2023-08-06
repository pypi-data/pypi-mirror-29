/*
 * transcoder.hpp
 *
 *  Created on: 4 Dec 2017
 *      Author: julianporter
 */

#ifndef TRANSCODER_HPP_
#define TRANSCODER_HPP_

#include <iostream>

#include "base.hpp"
#include "MP3Encoder.hpp"
#include "WAVFile.hpp"
#include "AIFFFile.hpp"
#include "PCMFile.hpp"

namespace pylame {



data_t load(std::istream &stream);

class Transcode {
private:
	cdata_t out;

	
public:
	Transcode(const data_t &in,const unsigned quality,const unsigned rate) ;
	Transcode(std::istream &in,const unsigned quality,const unsigned rate) :
		Transcode(load(in),quality,rate) {};
	virtual ~Transcode() = default;
	
	cdata_t::const_iterator cbegin() const { return out.cbegin(); };
	cdata_t::const_iterator cend() const { return out.cend(); };
	const char *ptr() const;
	unsigned size() const { return out.size(); };
	std::ostream & output(std::ostream &o) const;
};



}

std::ostream & operator<<(std::ostream &o,const pylame::Transcode &t);
std::istream & operator>>(std::istream &i,pylame::Transcode &t);

#endif /* TRANSCODER_HPP_ */
