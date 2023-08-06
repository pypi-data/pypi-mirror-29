/*
 * Iterator32.hpp
 *
 *  Created on: 1 Dec 2017
 *      Author: julianporter
 */

#ifndef ITERATOR32_HPP_
#define ITERATOR32_HPP_

#include "base.hpp"
#include "Conversions.hpp"
#include <iomanip>
#include <type_traits>

namespace pylame { namespace pcm {

using pair_t=std::pair<uint16_t,uint16_t>;

class Iterator32 {
private:
	const_iterator_t end;
	const_iterator_t it;
	Endianness endian;

	template <typename N>
			N wrap(N n) {
				return (endian==Endianness::LittleEndian) ? n : swap(n);
			};

protected:
	std::string nextString();
		uint32_t nextInt() { return wrap(convertNext().u32); };
			uint64_t nextInt64() { return convertNext64().u64; };
			float nextFloat() { return convertNext().f; };
			double nextDouble() { return convertNext64().d; };
			long double nextLongDouble();

			pair_t nextPair();


public:



	Iterator32() : end(), it(), endian(Endianness::LittleEndian) {};
	Iterator32(const data_t &data,const Endianness &e) : end(data.end()), it(data.begin()), endian(e) {};
	Iterator32(const Iterator32 &o) : end(o.end), it(o.it), endian(o.endian) {};
	Iterator32(const_iterator_t it_,const_iterator_t end_,Endianness endian_) : end(end_), it(it_), endian(endian_) {};
	virtual ~Iterator32() = default;
	Iterator32 & operator=(const Iterator32 & o) = default;

	Endianness endianness() const { return endian; };

	Converter32 convertNext();
	Converter64 convertNext64();

	template<typename T, class = typename std::enable_if<std::is_arithmetic<T>::value>::type>
	T next() {
		if(std::is_same<T,uint32_t>::value) { return (T)wrap(convertNext().u32); };
		if(std::is_same<T,uint64_t>::value) { return (T)convertNext64().u64; };
		if(std::is_same<T,float>::value) { return (T)convertNext().f; };
		if(std::is_same<T,double>::value) { return (T)convertNext64().d; };
		if(std::is_same<T,long double>::value) { return (T)nextLongDouble(); };
		throw MP3Error("Unknown type");
	}
	template<typename T, class = typename std::enable_if<std::is_same<T,std::string>::value>::type>
	std::string next()
	{
		return nextString();
	}
	template<typename T, class = typename std::enable_if<std::is_same<T,pair_t>::value>::type>
		pair_t next()
		{
			return nextPair();
		}
/*
	uint32_t    next_uint32_t()   { return wrap(convertNext().u32); };
	uint64_t    next_uint64_t()   { return convertNext64().u64; };
	float       next_float()      { return convertNext().f; };
	double      next_double()     { return convertNext64().d; };
	long double next_long_double(){ return nextLongDouble(); };
	std::string next_string()     { return nextString(); };
	pair_t      next_pair()       { return nextPair(); };
*/
	template<typename T, class = typename std::enable_if<std::is_same<T,float>::value>::type>
	std::pair<float,float> nextPairOf() { return std::make_pair(next<float>(),next<float>()); }
	template<typename T, class = typename std::enable_if<std::is_same<T,int32_t>::value>::type>
	std::pair<uint32_t,uint32_t> nextPairOf() { return std::make_pair(next<uint32_t>(),next<uint32_t>()); }
	template<typename T, class = typename std::enable_if<std::is_same<T,int16_t>::value>::type>
	pair_t nextPairOf() { return nextPair(); }

	Iterator32 fix(const unsigned n) const {
		return Iterator32(it,it+n,endian);
	};

	void skip(const int n) { it+=(4*n); };
	bool finished() const { return it==end; };


	void getN(const unsigned n,char *data);
	data_t getN(const unsigned n);
	char get();

	unsigned size() const { return end-it; }
};




}}



#endif /* ITERATOR32_HPP_ */
