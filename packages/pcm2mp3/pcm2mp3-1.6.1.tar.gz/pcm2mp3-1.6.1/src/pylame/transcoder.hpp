/*
 * transcoder.hpp
 *
 *  Created on: 4 Dec 2017
 *      Author: julianporter
 */

#ifndef TRANSCODER_HPP_
#define TRANSCODER_HPP_

#include <iostream>
#include <vector>




namespace pylame {

using pcm_t = std::vector<char>;
using bytes_t = std::vector<unsigned char>;

class Parameters;

pcm_t load(std::istream &stream);

class Transcode {
private:
	bytes_t out;

	
public:
	Transcode(const Parameters &parameters,const pcm_t &in) ;
	Transcode(const Parameters &parameters,std::istream &in) : Transcode(parameters,load(in)) {};
	virtual ~Transcode() = default;
	
	bytes_t::const_iterator cbegin() const { return out.cbegin(); };
	bytes_t::const_iterator cend() const { return out.cend(); };
	const char *ptr() const;
	unsigned size() const { return out.size(); };
	std::ostream & output(std::ostream &o) const;
};



}

std::ostream & operator<<(std::ostream &o,const pylame::Transcode &t);
std::istream & operator>>(std::istream &i,pylame::Transcode &t);

#endif /* TRANSCODER_HPP_ */
