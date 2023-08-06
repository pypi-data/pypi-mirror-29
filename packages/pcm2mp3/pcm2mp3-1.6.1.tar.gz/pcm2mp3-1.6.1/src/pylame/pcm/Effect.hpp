/*
 * Effect.hpp
 *
 *  Created on: 8 Feb 2018
 *      Author: julianporter
 */

#ifndef EFFECT_HPP_
#define EFFECT_HPP_

#include <base.hpp>
#include <Parameters.hpp>

namespace pylame {
namespace pcm {

class Effect {
protected:
	pylame::Parameters parameters;

public:
	Effect() : parameters() {};
	Effect(const Parameters &p) : parameters(p) {};
	virtual ~Effect() = default;

	virtual void operator()(const unsigned nChannels,const unsigned length,float *buffers[]) = 0;
};

class Normalise : public Effect {

private:

public:
	Normalise() : Effect() {};
	Normalise(const Parameters &p) : Effect(p) {};
	virtual ~Normalise() = default;

	virtual void operator()(const unsigned nChannels,const unsigned length,float *buffers[]);
};

class Compress : public Effect {

private:

public:
	Compress() : Effect() {};
	Compress(const Parameters &p) : Effect(p) {};
	virtual ~Compress() = default;

	virtual void operator()(const unsigned nChannels,const unsigned length,float *buffers[]);
};

} /* namespace pcm */
} /* namespace pylame */

#endif /* EFFECT_HPP_ */
