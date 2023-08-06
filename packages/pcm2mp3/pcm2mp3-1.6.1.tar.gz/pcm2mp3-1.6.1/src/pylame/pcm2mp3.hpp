/*
 * pcm2mp3.hpp
 *
 *  Created on: 10 Feb 2018
 *      Author: julianporter
 */

#ifndef PCM2MP3_HPP_
#define PCM2MP3_HPP_

#include <string>
#include <exception>
#include <vector>
#include <iostream>

namespace pylame {

class MP3Error : public std::exception {
	private:
		std::string message;
	public:
		MP3Error(const std::string &message_) noexcept : std::exception(), message(message_) {} ;
		template<typename ...Terms>
		MP3Error(Terms ...params) noexcept : std::exception(), message(StringMaker(params...).str()) {};
		MP3Error(const MP3Error &) = default;
		MP3Error & operator=(const MP3Error &) = default;
		virtual ~MP3Error() = default;

		virtual const char *what() const noexcept { return message.c_str(); };


	};

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

#endif /* PCM2MP3_HPP_ */
