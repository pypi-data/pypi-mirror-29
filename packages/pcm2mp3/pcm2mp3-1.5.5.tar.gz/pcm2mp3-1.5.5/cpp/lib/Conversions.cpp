/*
 * Conversions.cpp
 *
 *  Created on: 5 Dec 2017
 *      Author: julianporter
 */

#include "Conversions.hpp"
#include "Iterator32.hpp"
#include <algorithm>

namespace pylame { namespace pcm {

Converter80::Converter80() {
	std::fill_n(bytes,10,0);
}

Converter80::Converter80(data_t::const_iterator &it) {
	for(auto i=0;i<10;i++) bytes[9-i]=*it++;
}



Converter80::Converter80(char *p) {
	for(auto i=0;i<10;i++) bytes[9-i]=p[i];
}

uint16_t swap(uint16_t in) {
	return (in<<8)|(in>>8);
}

std::pair<uint16_t,uint16_t> swap(std::pair<uint16_t,uint16_t> in) {
	auto o= std::make_pair(swap(in.first),swap(in.second));
	return o;
}

uint32_t swap(uint32_t in) {
	uint32_t top=uint32_t(swap(uint16_t(in)))<<16;
	uint32_t bot=uint32_t(swap(uint16_t(in>>16)));
	return (top|bot);
	
}

uint32_t swap(uint16_t u1,uint16_t u2) {
	uint32_t top=uint32_t(u1)<<16;
	uint32_t bot=uint32_t(u2);
	return top|bot;
	
}

}}
