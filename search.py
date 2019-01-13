#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script sends the given command-line arguments as a query to the running
DocFetcher instance. The results returned by the latter are printed as filename-
filepath pairs on the standard output.

For more advanced processing of the results, call the search function below
directly. In principle, you can also reuse the code in the search function for
arbitrarily scripting the DocFetcher instance.

By default, DocFetcher's scripting support is disabled due to security reasons
and must be enabled by setting the variable "PythonApiEnabled" in the advanced
settings file (program-conf.txt) to "true".

Running this script requires Py4J (https://www.py4j.org/). DocFetcher already
ships with a Py4J distribution, but it only works if the py4j folder is in the
same folder as this script. To script DocFetcher from a different location, move
the py4j folder there, or install Py4J separately.

Note that only the main DocFetcher program instance supports scripting, not the
DocFetcher daemon.
"""

def main():
	import sys
	if len(sys.argv) <= 1:
		print("No query specified.")
		return
	query = " ".join(sys.argv[1:])
	try:
		result_docs = search(query, 28834)
		for doc in result_docs:
			print(doc.getFilename() + "\t" + doc.getPathStr())
	except:
		print("ERROR: " + str(sys.exc_info()[1]))

# string, int -> [ResultDocument]
def search(query, port):
	"""Sends the given query string to the running DocFetcher instance at the
	given port and returns a list of result objects.
	
	The result objects provide the following getter methods for accessing their
	attributes:
	- getAuthors
	- getDateStr - e-mail send date
	- getFilename
	- getLastModifiedStr - last-modified date on files
	- getPathStr - file path
	- getScore - result score as int
	- getSender - e-mail sender
	- getSizeInKB - file size as int
	- getTitle
	- getType
	- isEmail - boolean indicating whether result object is e-mail or file
	
	This method will throw an error if communication with the DocFetcher
	instance fails.
	"""
	from py4j.java_gateway import JavaGateway, GatewayParameters
	from py4j.java_gateway import java_import
	
	gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
	java_import(gateway.jvm, "net.sourceforge.docfetcher.gui.Application")
	application = gateway.jvm.net.sourceforge.docfetcher.gui.Application
	
	indexRegistry = application.getIndexRegistry()
	searcher = indexRegistry.getSearcher()
	results = searcher.search(query)
	return results

if __name__ == "__main__":
	main()
