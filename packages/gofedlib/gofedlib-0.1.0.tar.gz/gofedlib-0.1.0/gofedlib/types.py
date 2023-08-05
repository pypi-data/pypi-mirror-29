# TODO(jchaloup): move the definitions to corresponding classes

class CommitNotRetrieved(Exception):
	pass

class TagsNotRetrieved(Exception):
	pass

class UnsupportedImportPathError(Exception):
	pass

class ExtractionError(Exception):
	pass
