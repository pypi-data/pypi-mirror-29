/*
 * WAVFile.hpp
 *
 *  Created on: 30 Nov 2017
 *      Author: julianporter
 */

#ifndef DEBUG_WAVFILE_HPP_
#define DEBUG_WAVFILE_HPP_

#include "base.hpp"
#include "PCMFile.hpp"
#include "Iterator32.hpp"
#include "DataChunk.hpp"

namespace pylame { namespace pcm {

class WAVFile : public PCMFile {
friend std::ostream & operator << (std::ostream &o,const WAVFile &w);

private:
	std::pair<long,long> clip();
	
protected:
	static DataFormat convertFormat(const uint16_t);
	virtual std::string FormHeader() const;
	virtual FormMetaData::TypeMap FormTypes() const;
	virtual void infoChunk(const std::shared_ptr<DataChunk> &);
	virtual void soundChunk(const std::shared_ptr<DataChunk> &);

public:
	
	WAVFile(const data_t &file_);
	WAVFile(std::istream & stream);
	virtual ~WAVFile() = default;

	
	virtual PCMData bytes(); // Gives interleaved data
	static bool isInstance(const data_t &d);
	static bool isInstance(std::istream &stream);

};
}}

std::istream & operator >> (std::istream &i,pylame::pcm::WAVFile &w);

#endif /* DEBUG_WAVFILE_HPP_ */
