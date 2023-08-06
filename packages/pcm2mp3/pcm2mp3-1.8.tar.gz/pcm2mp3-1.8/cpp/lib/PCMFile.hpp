/*
 * PCMFile.hpp
 *
 *  Created on: 30 Nov 2017
 *      Author: julianporter
 */

#ifndef PCMFILE_HPP_
#define PCMFILE_HPP_


#include "Form.hpp"
#include "Iterator32.hpp"
#include <lame/lame.h>
#include "base.hpp"
#include "PCMData.hpp"


namespace pylame { namespace pcm {




class PCMFile {

protected:

	unsigned short nChannels=0;
	unsigned sampleRate=0;
	unsigned bytesPerSample=0;
	unsigned nSamples=0;	// per channel
	unsigned nBytesInFile=0;
	unsigned dataSize=0;
	unsigned bitsPerSample=0;
	DataFormat format;
	FormMetaData metadata;
	data_t file;
	Form form;

	virtual void infoChunk(const std::shared_ptr<DataChunk> &chunk) { throw MP3Error("Not implemented"); };
	virtual void soundChunk(const std::shared_ptr<DataChunk> &chunk) { throw MP3Error("Not implemented"); };
	virtual void parse(Iterator32 &it,const std::string &info,const std::string &sound);

	virtual std::string FormHeader() const { throw MP3Error("Not implemented"); };
	virtual FormMetaData::TypeMap FormTypes() const { throw MP3Error("Not implemented"); };



public:

	PCMFile() : format(DataFormat::PCM), file(), form()  {};
	PCMFile(const data_t &file_) : format(DataFormat::PCM), file(file_), form()  {};
	PCMFile(std::istream &stream);
	virtual ~PCMFile() = default;


	virtual int bitRate() { return nChannels*sampleRate*bytesPerSample*8; };
	MPEG_mode mp3Mode() { return nChannels==1 ? MONO : JOINT_STEREO; };
	virtual unsigned samplesPerSecond() const { return sampleRate; };
	
	virtual PCMData bytes() { throw MP3Error("Not implemented"); };
	virtual unsigned samplesPerChannel() const { return nSamples; };
	virtual unsigned short nChans() const { return nChannels; };
	virtual unsigned size() const { return nBytesInFile; };
	virtual unsigned dSize() const { return dataSize; };
	virtual unsigned sampleSize() const { return bitsPerSample; };
	virtual unsigned sampleSizeInBytes() const { return bytesPerSample; };
	bool isWAV() const { return metadata.type==FileType::WAV; };
	bool isAIFC() const { return metadata.type==FileType::AIFC; };
	bool isAIFF() const { return metadata.type==FileType::AIFF; };
	virtual FileType fileType() const { return metadata.type; };

	pylame::SampleFormat sampleFormat() const;



};

using file_t = std::shared_ptr<PCMFile>;


}}


std::ostream & operator<<(std::ostream &o,const pylame::pcm::PCMFile &w);





#endif /* PCMFILE_HPP_ */
