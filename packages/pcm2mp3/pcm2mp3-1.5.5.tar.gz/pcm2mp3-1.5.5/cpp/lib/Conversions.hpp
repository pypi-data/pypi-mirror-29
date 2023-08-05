/*
 * Conversions.hpp
 *
 *  Created on: 5 Dec 2017
 *      Author: julianporter
 */

#ifndef CONVERSIONS_HPP_
#define CONVERSIONS_HPP_

#include "base.hpp"

namespace pylame { namespace pcm {



union Converter32 {
		uint32_t u32;
		uint16_t u16[2];
		char bytes[4];	
		float f;
	};
	union Converter64 {
			uint64_t u64;
			uint32_t u32[2];
			uint16_t u16[4];
			char bytes[8];
			double d;
	};


union Converter80 {
		char bytes[10];
		long double ld;
		uint8_t u8[10];
		
		Converter80();
		Converter80(data_t::const_iterator &);
		Converter80(char *);
		
};



struct Float80 {
private:
	
	Converter80 c;
	
public: 
	Float80() : c() {};
	Float80(data_t::const_iterator &it) : c(it) {};
	Float80(char *p) : c(p) {};
	
	operator long double() { return c.ld; };
	operator double() { return (double)c.ld; };
};

uint16_t swap(uint16_t in);
uint32_t swap(uint32_t in);
uint32_t swap(uint16_t u1,uint16_t u2);
std::pair<uint16_t,uint16_t> swap(std::pair<uint16_t,uint16_t> in);

}}


#endif /* CONVERSIONS_HPP_ */
