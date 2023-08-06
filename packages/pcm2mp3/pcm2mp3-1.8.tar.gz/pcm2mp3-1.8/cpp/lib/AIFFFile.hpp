/*
 * AIFFFile.hpp
 *
 *  Created on: 5 Dec 2017
 *      Author: julianporter
 */

#ifndef AIFFFILE_HPP_
#define AIFFFILE_HPP_

#include "base.hpp"
#include "PCMFile.hpp"


namespace pylame { namespace pcm {

class AIFFFile: public PCMFile {
private:
	unsigned offset = 0;
	unsigned blocksize = 0;


protected:
	static DataFormat convertFormat(const std::string &);
	virtual std::string FormHeader() const;
	virtual FormMetaData::TypeMap FormTypes() const;

	virtual void infoChunk(const std::shared_ptr<DataChunk> &);
	virtual void soundChunk(const std::shared_ptr<DataChunk> &);

	
public:
	AIFFFile(const data_t &file_);
	AIFFFile(std::istream &);
	virtual ~AIFFFile() = default;

	virtual PCMData bytes();
	static bool isInstance(const data_t &d);
	static bool isInstance(std::istream &stream) ;
};

}}




#endif /* AIFFFILE_HPP_ */
