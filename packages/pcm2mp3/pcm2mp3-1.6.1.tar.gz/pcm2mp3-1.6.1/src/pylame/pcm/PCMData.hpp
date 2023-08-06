/*
 * PCXMData.hpp
 *
 *  Created on: 16 Jan 2018
 *      Author: julianporter
 */

#ifndef PCMDATA_HPP_
#define PCMDATA_HPP_

#include <base.hpp>
#include <Parameters.hpp>
#include "Effect.hpp"
#include "Iterator32.hpp"
#include <utility>
#include <type_traits>

namespace pylame { namespace pcm {


enum class Channel {
	Left, Right
};



class PCMData {
private:
	pylame::Parameters parameters;
	pylame::SampleFormat format;
	unsigned nChannels;
	unsigned nSamples;
	Iterator32 it;
	std::shared_ptr<float> left;
	std::shared_ptr<float> right;

	template<typename T, class = typename std::enable_if<std::is_same<T,float>::value || std::is_same<T,int32_t>::value || std::is_same<T,int16_t>::value >::type>
	void build() {

			if(nChannels<1 || nChannels>2) throw MP3Error("Invalid number of channels");

			float *lBuffer=new float[nSamples];
			float *rBuffer=new float[nSamples];

			unsigned index=0;

			if(nChannels==1) {
				while(!it.finished()) {
					try {
						std::pair<float,float> d=it.nextFloatPair<T>();
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
						std::pair<float,float> d=it.nextFloatPair<T>();
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
			float *buffers[] = {lBuffer,rBuffer};
			Normalise n(parameters);
			n(nChannels,nSamples,buffers);

			Compress c(parameters);
			c(nChannels,nSamples,buffers);

			left=std::shared_ptr<float>(lBuffer);
			right=std::shared_ptr<float>(rBuffer);
		};



public:

	PCMData() : parameters(), format(pylame::SampleFormat::Unknown), nChannels(), nSamples(), it(), left(), right() {};
	PCMData(const pylame::Parameters &parameters_,const pylame::SampleFormat &format_, const unsigned nChannels_,const unsigned nSamples_,Iterator32 &it_) : parameters(parameters_), format(format_), nChannels(nChannels_), nSamples(nSamples_), it(it_) {
		switch(format) {
			case pylame::SampleFormat::Float32:
				build<float>();
					break;
			case pylame::SampleFormat::Int16:
				build<int16_t>();
					break;
			case pylame::SampleFormat::Int32:
				build<int32_t>();
					break;
				default:
					throw MP3Error("Invalid data format");
			}
	};
	virtual ~PCMData() = default;

	float *operator[](const Channel &channel) {
		return (channel==Channel::Left) ? left.get() : right.get() ;
	};
};


}}

#endif /* PCMDATA_HPP_ */
