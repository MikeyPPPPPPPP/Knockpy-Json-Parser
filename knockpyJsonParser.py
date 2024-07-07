
import sys
import os
import json



class fileParser:
	class parseStatusCodesError(Exception):
		def __init__(self, message="Codes Must be Integers and be Seperated with ,"):
			self.message = message
			super().__init__(self.message)


	def __init__(self, inFile: str, status_codes: str = None) -> None:
		self.inFile: str = inFile
		self.status_codes: str = status_codes
		self.domains: list[str] = []
		self.codes: list[str] = []#status codes 

		if self.status_codes != None:
			self.codes = self.parseStatusCodes()
			self._extract_domains()
		else:
			self._extract_domains()

		

	def parseStatusCodes(self) -> list[str]:
		codes: list[str] = []

		#multipule codes
		if ',' in self.status_codes:
			for code in self.status_codes.split(','):
				if not code.isdigit():
					raise self.parseStatusCodesError()
				codes.append(code)

		#one code
		else:
			if not self.status_codes.isdigit():
				raise Exception("Code Must Integer")
			codes.append(self.status_codes)

		return codes

			

	def _extract_domains(self) -> list[str]:
		'''This will parse the file'''
		with open(self.inFile, 'r') as file:

			#parse file to json format
			data = json.loads(file.read())

		for domain, _ in data.items():
			#are surce codes specified
			if self.status_codes == None:#self.status_codes != None:
				self.domains.append(domain)
				continue
			else:
				try:
					if str(data[domain]["code"]).strip() in self.codes:
						self.domains.append(domain)

				#the domain didnt return a code
				except KeyError:
					pass

			#else:
			#	self.domains.append(domain)
			

	def writeToFile(self):
		with open("knockpy-hosts.txt", 'w+') as file:

			#get all except last domain; just making the outfile look nice
			for domain in self.domains[0:-1]:

				#check if theres a . in it
				if "." in domain.strip():
					file.write(str(domain.strip())+"\n")

			#add last domain with no newline cherector and check if theres a . in it
			if "." in self.domains[-1].strip():
				file.write(str(self.domains[-1].strip()))
		

def scriptHelp(choise):
	match choise:
		case 1:
			print("File path wrong or dose not exist")
		case 0:
			print("./knockpyJsonParser.py <infile> <status codes>\n\n")
			print("<infile>              Must be from Knockpy.py's output, file ends with .json")
			print("<status codes>        200,404,301")

	

def main():
	#check for user input
	try:
		knockpy_file = sys.argv[1]
		#check if file exists
		if not os.path.exists(knockpy_file):
			#scriptHelp(1)
			sys.exit(0)

		# status codes specified
		elif len(sys.argv) == 3:

			parserObject = fileParser(knockpy_file, sys.argv[2])

			parserObject.parseStatusCodes()
			parserObject.writeToFile()
			sys.exit(0)
		elif len(sys.argv) == 2:
			parserObject = fileParser(knockpy_file)

			parserObject.writeToFile()
			sys.exit(0)

	except:
		scriptHelp(0)

	

if __name__ == "__main__":
	main()

