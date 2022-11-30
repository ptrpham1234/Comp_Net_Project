class Files:
	def __init__(self):
		self.files = {
			"files": [{
				"id": 1,
				"filename": "test.txt",
				"filetype": "text",
				"description": "the test file to be read"
			},
				{
					"id": 2,
					"filename": "notReal.txt",
					"filetype": "text",
					"description": "not a real file"
				},
				{
					"id": 3,
					"filename": "aLie.txt",
					"filetype": "text",
					"description": "also not a real file"
				}
			]
		}

	def getList(self):
		return self.files

	def getFileDict(self, ID):
		for file in self.files.get("files"):
			if file["id"] == ID:
				return file
		return None
