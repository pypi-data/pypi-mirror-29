/*
 * Form.hpp
 *
 *  Created on: 21 Dec 2017
 *      Author: julianporter
 */

#ifndef FORM_HPP_
#define FORM_HPP_

#include "base.hpp"
#include "Iterator32.hpp"
#include "DataChunk.hpp"
#include <map>
#include <list>


namespace pylame {
namespace pcm {

	struct FormMetaData {
		using TypeMap = std::map<std::string,FileType>;
		std::string header;
		std::string format;
		unsigned length;
		FileType type;

		FormMetaData() : header(), format(), length(), type(FileType::Other) {};
		FormMetaData(const std::string &h,const std::string &f,const unsigned l) : header(h), format(f), length(l), type(FileType::Other) {};
		virtual ~FormMetaData() = default;

		bool verify(const std::string &head,const TypeMap &formats);
	};



	class Form {
	private:
		Iterator32 it;
		FileType type;
		std::multimap<std::string,std::shared_ptr<DataChunk>> chunks;
		unsigned len;
		Endianness endian;

		bool nextChunk();

	public:

		Form() : it(), type(FileType::Other), chunks(), len(), endian(Endianness::LittleEndian) {};
		Form(const data_t &data,const Endianness &e) : it(data,e), type(FileType::Other), chunks(), len(), endian(e) {};
		Form(Iterator32 &ptr) : it(ptr), type(FileType::Other), chunks(), len(),endian(ptr.endianness()) {};
		virtual ~Form() = default;

		FormMetaData typeCheck();

		void walk();

		FileType fileType() const { return type; };
		unsigned size() const { return chunks.size(); };
		unsigned bytesInFile() const { return len; };
		bool has(const std::string &key) const { return chunks.count(key)>0; };
		unsigned hasOne(const std::string &key) const { return chunks.count(key)==1; };
		std::shared_ptr<DataChunk> operator[](const std::string &ID);

	};




} /* namespace pcm */
} /* namespace pylame */

std::ostream & operator<<(std::ostream &,const pylame::pcm::FormMetaData&);

#endif /* FORM_HPP_ */
