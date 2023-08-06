/*
 * Iterator32.cpp
 *
 *  Created on: 21 Dec 2017
 *      Author: julianporter
 */
 #include "Iterator32.hpp"

namespace pylame { namespace pcm {

	Converter32 Iterator32::convertNext() {
		Converter32 c;
		for(auto i=0;i<4;i++) {
			if(it==end) throw MP3Error("Overrun end of file");
			c.bytes[i]=*it;
			it++;
		}
		return c;
	}
	Converter64 Iterator32::convertNext64() {
		Converter64 c;
		for(auto i=0;i<8;i++) {
			if(it==end) throw MP3Error("Overrun end of file");
			c.bytes[i]=*it;
			it++;
		}
		return c;
	}
	std::string Iterator32::nextString() {
			char c[5]={0,0,0,0,0};
			for(auto i=0;i<4;i++) {
				if(it==end) throw MP3Error("Overrun end of file");
				c[i]=char(*it++);
			}
			return std::string(c,4);
	}
	long double Iterator32::nextLongDouble() {
			Float80 f(it);
			return (long double)f;
		}
	pair_t Iterator32::nextPair() {
			uint32_t u=convertNext().u32;
			uint16_t a=(u>>16);
			uint16_t b=u&0xffff;
			return wrap(std::make_pair(b,a));
		}
	void Iterator32::getN(const unsigned n,char *data) {
			for(unsigned i=0;i<n;i++) {
				if(it==end) throw MP3Error("Overrun end of file");
				data[i]=*it;
				it++;
			}
	}
	data_t Iterator32::getN(const unsigned n) {
		data_t d(it,it+n);
		it+=n;
		return std::move(d);
	}
		char Iterator32::get() {
			if(it==end) throw MP3Error("Overrun end of file");
			return *it++;
		}


}}
