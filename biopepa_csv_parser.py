class BioPepaCsvParser():
    
    def parseResults(self):
        data = self.contents[8:]
            
        for row in data:
            row = row.split(',')
            for i in range(0,len(row)):
                self.results_dict[self.keys[i]] += [row[i].strip()]
        
        
    def openCsv(self,csv):
        with open(csv, 'r') as f:
            self.contents = f.readlines()
            self.results_dict = {}
            self.keys = self.contents[7].split(',')
            self.keys[0] = self.keys[0][2:]
            self.results_dict[self.keys[0]] = []
            
            for i in range(1,len(self.keys)):
                self.keys[i] = self.keys[i].strip()[1:-1]
                self.results_dict[self.keys[i]] = []
