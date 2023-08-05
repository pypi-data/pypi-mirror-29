/*
 * DataChunk.hpp
 *
 *  Created on: 20 Dec 2017
 *      Author: julianporter
 */

#ifndef DATACHUNK_HPP_
#define DATACHUNK_HPP_

#include "base.hpp"
#include "Iterator32.hpp"


namespace pylame {
namespace pcm {


	class DataChunk {
private:
	std::string ID;
	data_t data;
	Endianness endian;
		
public:

	DataChunk() : ID(), data(), endian(Endianness::LittleEndian) {};
	DataChunk(const std::string &name,const data_t &data_,const Endianness &e) : ID(name), data(data_), endian(e) {};
	DataChunk(const std::string &name,data_t &&data_,const Endianness &e) : ID(name), data(data_), endian(e) {};
	DataChunk(const DataChunk &) = default;
	virtual ~DataChunk() = default;
	DataChunk & operator=(const DataChunk &) = default;
	
	unsigned size() const { return data.size(); };
	Iterator32 iterator() const { return Iterator32(data,endian); };
	std::string kind() const { return ID; };

	void print() const;
};







} /* namespace pcm */
} /* namespace pylame */

std::ostream & operator<<(std::ostream &,const pylame::pcm::DataChunk &);


#endif /* DATACHUNK_HPP_ */
