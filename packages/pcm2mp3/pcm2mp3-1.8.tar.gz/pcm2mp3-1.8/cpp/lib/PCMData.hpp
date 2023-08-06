/*
 * PCXMData.hpp
 *
 *  Created on: 16 Jan 2018
 *      Author: julianporter
 */

#ifndef PCMDATA_HPP_
#define PCMDATA_HPP_

#include "base.hpp"
#include "Iterator32.hpp"
#include <utility>
#include <type_traits>

namespace pylame { namespace pcm {



template <typename T>
	struct Channels {
		std::shared_ptr<T> left;
		std::shared_ptr<T> right;

		Channels() : left(), right() {};
		Channels(std::shared_ptr<T> left_,std::shared_ptr<T> right_) :left(left_), right(right_) {};
		Channels(T* left_, T* right_) : left(left_), right(right_) {};
		virtual ~Channels() = default;


	};

struct PCMData {
	pylame::SampleFormat format;
	unsigned nChannels;
	unsigned nSamples;
	Iterator32 it;

	PCMData() : format(pylame::SampleFormat::Unknown), nChannels(), nSamples(), it() {};
	PCMData(const pylame::SampleFormat &format_, const unsigned nChannels_,const unsigned nSamples_,Iterator32 &it_) : format(format_), nChannels(nChannels_), nSamples(nSamples_), it(it_) {};
	virtual ~PCMData() = default;

	void normaliseArray(float * array);

	template<typename T, class = typename std::enable_if<std::is_same<T,float>::value || std::is_same<T,int32_t>::value || std::is_same<T,int16_t>::value >::type>
	Channels<T> channels() {

		if(nChannels<1 || nChannels>2) throw MP3Error("Invalid number of channels");

		T *lBuffer=new T[nSamples];
		T *rBuffer=new T[nSamples];

		unsigned index=0;

		if(nChannels==1) {
			while(!it.finished()) {
				try {
					std::pair<T,T> d=it.nextPairOf<T>();
					lBuffer[index]=d.first;
					rBuffer[index]=0;
					index++;
					rBuffer[index]=d.second;
					rBuffer[index]=0;
					index++;
				}
				catch(...) {
					lBuffer[index]=0;
					rBuffer[index]=0;
					index++;
				}
			}
		} else { 	/// Stereo
			while(!it.finished()) {
				try {
					std::pair<T,T> d=it.nextPairOf<T>();
					lBuffer[index]=d.first;
					rBuffer[index]=d.second;
					index++;
				}
				catch(...) {
					lBuffer[index]=0;
					rBuffer[index]=0;
					index++;
				}
			}
		}
		if(std::is_floating_point<T>::value) {
			normaliseArray((float *)lBuffer);
			if(nChannels>1) normaliseArray((float *)rBuffer);
		}

		return Channels<T>(lBuffer,rBuffer);
	};
};
}}

#endif /* PCMDATA_HPP_ */
